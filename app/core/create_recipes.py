import asyncio

from celery import Celery
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.recipe_generator import generate_recipe as generate_single_recipe
from app.core.nutritional_calculator import calculate_nutrition
from app.core.validator import validate_recipe
from app.logging_config import logger
from sqlalchemy.orm import sessionmaker
from app.db.crud import save_recipe
from app.db.database import engine
from app.core.utils import combine, generate_random_recipe_values, convert_ingredients_to_list
from app.schemas.recipe_schemas import Recipe

celery_app = Celery("recipe_queue", broker="redis://localhost:6379/0", backend="redis://localhost:6379/0")
async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


@celery_app.task(bind=True, ignore_result=False, track_started=True)
def generate_recipe_task(self, params: dict, recipe_id: str, use_weights: bool = False):
    """
    Synchronous Celery task that wraps the async recipe generation function.
    """
    return asyncio.run(async_generate_recipe_task(self, params, recipe_id, use_weights))


async def async_generate_recipe_task(self, params: dict, recipe_id: str, use_weights: bool = False):
    """
    Asynchronous Celery task to generate a recipe and save it.
    """

    params = Recipe(**params)
    async with async_session() as session:
        try:
            while True:
                if not use_weights:
                    logger.debug("Generating with random recipe.")
                    filled_params = await generate_random_recipe_values(params)
                else:
                    logger.debug("Generating a weighted random recipe.")
                    filled_params = await generate_random_recipe_values(params, use_weights=use_weights)

                logger.info(f"Generating recipe with parameters: {filled_params}")
                generated_recipe = await generate_single_recipe(filled_params)
                logger.info(f"Recipe generated: {generated_recipe}")

                logger.debug("Calculating nutrition for the generated recipe...")
                nutritious = await calculate_nutrition(generated_recipe)

                logger.debug("Combining the recipe and nutrition information...")
                recipe = await combine(generated_recipe, nutritious)

                logger.debug("Validating the generated recipe...")
                if isinstance(recipe.get("ingredients"), dict):
                    recipe["ingredients"] = await convert_ingredients_to_list(recipe["ingredients"])
                    logger.debug("Converted ingredients to list.")

                validate = await validate_recipe(recipe)
                logger.debug(f"Validation result: {validate}")

                if "Yes" in validate:
                    logger.info("Recipe generated successfully.")
                    await save_recipe(session, recipe, recipe_id)
                    await session.commit()

                    return recipe
                else:
                    logger.info("Recipe is not realistic, retrying.")

        except Exception as e:
            self.update_state(state="FAILURE", meta=str(e))
            logger.error(f"Error in generate_recipe_task: {e}")
            return {"status": "error", "message": str(e)}
