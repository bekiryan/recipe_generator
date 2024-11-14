from app.core.llm import chat_completion
from app.schemas.recipe_schemas import Recipe


async def validate_recipe(recipe: Recipe):
    """
    Validates the recipe generated by the model.

    :param recipe: RecipeCreate: The recipe to validate.
    :return: str: The validation response.
    """
    prompt = f"""
    You are a professional chef. The recipe is defined between <recipe> and </recipe>.
    Check if it is realistic or not.
    Check all the recipe parameters: the ratio of ingredients;
    Step-by-step directions is clear and precise;
    combination of ingredients and flavour pairings are correct, harmonious, and enjoyable.
    You are answering only “Yes” or “No”.
    <recipe>
    {recipe}
    </recipe>
    """

    return await chat_completion(prompt)