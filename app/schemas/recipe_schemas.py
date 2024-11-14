from pydantic import BaseModel, Field
from typing import List, Dict, Any
from enum import Enum
from uuid import UUID
class RecipeStatus(str, Enum):
    ACTIVE = "ACTIVE"
    FROZEN = "FROZEN"

class Recipe(BaseModel):
    amountOfPersons: int | None = Field(default=None, example=4)
    dishType: str | None = Field(default=None, example="main")
    maxCooking: int | None = Field(default=None, example=60)
    allergiesList: List[str] | None = Field(default=None, example=["nuts", "dairy"])
    dietRequirements: List[str] | None = Field(default=None, example=["vegetarian", "gluten-free"])
    cuisineList: List[str] | None = Field(default=None, example=["Italian", "Chinese"])

class RecipeResponse(BaseModel):
    id: UUID
    name: str
    cooking_time: str
    required_tools: List[str]
    ingredients: List[Dict[str, Any]]
    steps: List[str]
    nutrition: Dict[str, Any]
    status: RecipeStatus = RecipeStatus.ACTIVE

    class Config:
        orm_mode = True

class RecipeEdit(BaseModel):
    """
    Schema for editing a recipe.
    Fields are optional to allow partial updates.
    """
    name: str | None = None
    cooking_time: str | None = None
    required_tools: List[str] | None = None
    ingredients: List[Dict[str, Any]] | None = None
    steps: List[str] | None = None
    nutrition: Dict[str, Any] | None = None
    status: RecipeStatus | None = None

class RecipeChunkParams(BaseModel):
    """
    Schema for chunk generation parameters, including randomization options.
    """
    params: Recipe
    randomization_type: str | None = None
    weights: Dict[str, float] | None = None
