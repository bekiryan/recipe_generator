import json
import random
from typing import List, Dict, Any
from app.logging_config import logger
from app.schemas.recipe_schemas import Recipe
from app.config import (
    WEIGHTS_DISH_TYPES,
    WEIGHTS_ALLERGIES,
    WEIGHTS_DIET_REQUIREMENTS,
    WEIGHTS_CUISINES,
    POSSIBLE_AMOUNT_OF_PERSONS,
    WEIGHTS_AMOUNT_OF_PERSONS,
    POSSIBLE_DISH_TYPES,
    POSSIBLE_CUISINES,
    POSSIBLE_DIET_REQUIREMENTS,
    POSSIBLE_ALLERGIES, POSSIBLE_MAX_COOKING_TIMES, WEIGHTS_MAX_COOKING_TIMES
)
import numpy as np


async def combine(recipe: Recipe, nutrition_info: Dict[str, Any]) -> Recipe:
    """
    Combines the generated recipe and nutritional information.
    Assumes both recipe and nutrition_info are dictionaries.

    :param recipe: dict: The generated recipe.
    :param nutrition_info: dict: The nutritional information.
    :return: dict: The combined recipe with nutritional information.
    """
    recipe["nutrition"] = nutrition_info
    return recipe


async def parse_gpt_response(content: str) -> Recipe | None:
    """
    Parses the GPT response from the API.

    :param content: str: The content of the response.
    :return: dict | None: The parsed JSON data or None if parsing fails.
    """
    if "```json" in content:
        content = content.strip("```json").strip("```").strip()
    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON: {e}")
        return None


async def generate_random_recipe_values(params: Recipe, use_weights: bool = False) -> Recipe:
    """
    Generate random values for the recipe parameters if they are not provided.

    :param params: Recipe: The recipe parameters.
    :param use_weights: bool: If True, apply weights to generate the parameters.
    :return: Recipe: The updated recipe parameters.
    """
    if params.amountOfPersons is None:
        params.amountOfPersons = random.choices(
            POSSIBLE_AMOUNT_OF_PERSONS, weights=WEIGHTS_AMOUNT_OF_PERSONS if use_weights else None, k=1)[0]

    if params.dishType is None:
        params.dishType = random.choices(
            POSSIBLE_DISH_TYPES, weights=WEIGHTS_DISH_TYPES if use_weights else None, k=1)[0]

    if params.maxCooking is None:
        params.maxCooking = random.choices(
            POSSIBLE_MAX_COOKING_TIMES, weights=WEIGHTS_MAX_COOKING_TIMES if use_weights else None, k=1)[0]

    if params.allergiesList is None:
        params.allergiesList = np.random.choice(POSSIBLE_ALLERGIES, size=random.randint(0, len(POSSIBLE_ALLERGIES)),
                                                replace=False, p=normalize_weights(WEIGHTS_ALLERGIES) if use_weights else None).tolist()

    if params.dietRequirements is None:
        params.dietRequirements = np.random.choice(POSSIBLE_DIET_REQUIREMENTS,
                                                   size=random.randint(0, len(POSSIBLE_DIET_REQUIREMENTS)),
                                                   replace=False,
                                                   p=normalize_weights(WEIGHTS_DIET_REQUIREMENTS) if use_weights else None).tolist()

    if params.cuisineList is None:
        params.cuisineList = np.random.choice(POSSIBLE_CUISINES, size=random.randint(0, len(POSSIBLE_CUISINES)),
                                              replace=False, p=normalize_weights(WEIGHTS_CUISINES) if use_weights else None).tolist()

    return params


async def convert_ingredients_to_list(ingredients_dict: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Convert ingredients from a dictionary format to a list of dictionaries,
    preserving all key-value pairs for each ingredient.

    :param ingredients_dict: dict: The ingredients in dictionary format.
    :return: List[Dict[str, Any]]: Ingredients converted to a list format.
    """
    return [{"Name": name, **details} for name, details in ingredients_dict.items()]

def normalize_weights(weights: List[int]) -> List[float]:
    """
    Normalize a list of weights so they sum up to 1.

    :param weights: List[int]: The list of weights.
    :return: List[float]: The normalized weights.
    """
    w = np.array(weights, dtype=float)
    return w / w.sum()