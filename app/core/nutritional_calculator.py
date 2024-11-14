from app.core.llm import chat_completion
from app.core.utils import parse_gpt_response
from app.logging_config import logger
from app.schemas.recipe_schemas import Recipe


async def calculate_nutrition(recipe: Recipe, retry_after_failure=10):
    """
    Calculate the nutritional values of the given recipe.

    :param recipe: RecipeCreate: The recipe to calculate nutritional values for.
    :param retry_after_failure: int: Number of retries after a failed attempt.
    :return: dict: The nutritional values.
    """
    prompt = f"""
    You are food technologist.
    The recipe is defined between <recipe> and </recipe>.
    Calculate the weight of this dish, the number of servings,
    and the nutritional values (calories, protein, fat, carbohydrates)
    Your output should be in format defined between <format> and </format>.
    You are not asking questions, just responding with JSON that contains nutritional values.
    <format>
    1. Each of your answers is a JSON, consisting of few main parameters "calories",
    "protein", "fat", "carbohydrates", "totalWeight"
    </format>
    <recipe>
    {recipe}
    </recipe>
    """

    for _ in range(retry_after_failure):
        nutrition_json = await chat_completion(prompt)
        parsed_response = await parse_gpt_response(nutrition_json)
        if parsed_response is not None:
            return parsed_response
        logger.error("Failed to calculate nutrition, retrying...")
    raise Exception("Failed to calculate nutrition after 10 attempts.")