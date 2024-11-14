import os

POSSIBLE_AMOUNT_OF_PERSONS = [1, 2, 3, 4, 5, 6, 7]
WEIGHTS_AMOUNT_OF_PERSONS = [5, 5, 5, 2, 1, 1, 2]

POSSIBLE_DISH_TYPES = ["main", "side", "dessert", "appetizer"]
WEIGHTS_DISH_TYPES = [5, 2, 1, 1]

POSSIBLE_CUISINES = ["Italian", "Chinese", "Indian", "Mexican", "French"]
WEIGHTS_CUISINES = [5, 3, 3, 2, 1]

POSSIBLE_DIET_REQUIREMENTS = ["vegetarian", "vegan", "gluten-free", "keto"]
WEIGHTS_DIET_REQUIREMENTS = [5, 3, 2, 1]

POSSIBLE_ALLERGIES = ["nuts", "dairy", "gluten", "soy", "seafood"]
WEIGHTS_ALLERGIES = [4, 2, 2, 1, 1]

POSSIBLE_MAX_COOKING_TIMES = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120]
WEIGHTS_MAX_COOKING_TIMES = [3, 4, 5, 6, 7, 6, 5, 2, 1, 1, 1, 1]

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
API_KEY = os.getenv("API_KEY", "default_api_key")

LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "INFO")
