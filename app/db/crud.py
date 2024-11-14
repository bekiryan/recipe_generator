from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models import Recipe
from fastapi import HTTPException
from uuid import UUID
from app.logging_config import logger


async def save_recipe(db: AsyncSession, recipe_data: dict | Recipe, recipe_id: str) -> Recipe | dict:
    """
    Save the recipe data to the database

    :param db: AsyncSession: The database session
    :param recipe_data: dict: The recipe data
    :param recipe_id: str: The recipe ID
    :return: Recipe: The saved recipe
    """
    logger.info(f"Creating recipe with data: {recipe_data} and ID: {recipe_id}")
    recipe = Recipe(
        id=UUID(recipe_id),
        name=recipe_data["Name"],
        cooking_time=recipe_data["CookingTime"],
        required_tools=recipe_data["RequiredTools"],
        ingredients=recipe_data["Ingredients"],
        steps=recipe_data["Step-by-step directions"],
        nutrition=recipe_data["nutrition"],
        status=recipe_data["status"]
    )
    logger.debug(f"Recipe created with ID: {recipe_id}")
    db.add(recipe)
    logger.debug(f"Recipe added to the session")
    await db.commit()
    logger.debug(f"Recipe saved to the database")
    await db.refresh(recipe)
    logger.debug(f"Recipe refreshed")
    return recipe


async def get_all_recipes(db: AsyncSession):
    """
    Get all recipes from the database

    :param db: AsyncSession: The database session
    :return: List[Recipe]: The list of recipes
    """
    result = await db.execute(select(Recipe))
    return result.scalars().all()


async def get_recipe_by_id(db: AsyncSession, recipe_id: UUID):
    """
    Get a recipe by its ID

    :param db: AsyncSession: The database session
    :param recipe_id: int: The recipe ID
    :return: Recipe: The recipe
    """
    query = select(Recipe).where(Recipe.id == recipe_id)
    result = await db.execute(query)
    recipe = result.scalar_one_or_none()

    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")

    return recipe
