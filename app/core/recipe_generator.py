from app.core.llm import chat_completion
from app.core.utils import parse_gpt_response
from app.logging_config import logger
from app.schemas.recipe_schemas import Recipe


async def generate_recipe(params: Recipe, retry_after_failure = 10):
    """
    Generate a recipe based on the given parameters.

    :param params: RecipeCreate: The recipe parameters.
    :param retry_after_failure: int: Number of retries after a failed attempt.
    :return: dict: The generated recipe.
    """
    amount_of_persons = params.amountOfPersons
    dish_type = params.dishType
    max_cooking = params.maxCooking
    allergies_list = params.allergiesList
    diet_requirements = params.dietRequirements
    cuisine_list = params.cuisineList
    output_format = """
    1. Each of your answers is a JSON, consisting of few main parameters "Name",
    "CookingTime", "RequiredTools", "Ingredients", "Step-by-step directions"
    2. Each ingredient should contain main parameters "Name",
    3. For each ingredient you should display measurements in few units "grams" , "ml",
    "cups", "teaspoons", "tablespoons", "piece" 
    4. JSON should contain only one recipe
    """

    prompt = f"""
    Hey, ChatGPT, generate me a meal recipe for {amount_of_persons} and {dish_type}
    with cooking time under {max_cooking} minutes,
    good for people with allergies to {allergies_list},
    following {diet_requirements},
    preferring the {cuisine_list} given.
    Your output should look like {output_format}, You are not asking questions,
    just responding with recipe.
    """

    for _ in range(retry_after_failure):
        recipe_json = await chat_completion(prompt)
        parsed_response = await parse_gpt_response(recipe_json)
        if parsed_response is not None:
            parsed_response["status"] = "ACTIVE"
            return parsed_response
        logger.error(f"Failed to generate recipe from response {recipe_json}")
    raise Exception("Failed to generate recipe after 10 attempts.")