import asyncio
from uuid import UUID, uuid4
from typing import List

from celery.result import AsyncResult
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.create_recipes import generate_recipe_task, celery_app
from app.db.crud import get_all_recipes, get_recipe_by_id
from app.db.models import RecipeStatus
from app.schemas.recipe_schemas import Recipe, RecipeResponse, RecipeEdit
from app.logging_config import logger
from app.db.database import get_db
router = APIRouter()


@router.post("/generate_recipe", response_model=dict)
async def generate_recipe(params: Recipe, use_weights: bool = False):
    """
    Generates a recipe based on the input parameters and processes it in a background task.
    If no parameters are provided, random values will be generated.
    The 'use_weights' parameter determines if randomization with weights should be applied.
    """
    recipe_id = str(uuid4())

    try:
        task = generate_recipe_task.apply_async(
            args=[params.model_dump(), recipe_id],
            kwargs={"use_weights": use_weights},
            task_id=recipe_id
        )
        logger.info(f"Recipe generation task {task.id} created.")
        return {"status": "Recipe generation started", "recipe_id": str(recipe_id)}
    except Exception as e:
        logger.error(f"Error creating recipe generation task: {e}")
        raise HTTPException(status_code=500, detail="Error generating recipe")


@router.patch("/recipe/{recipe_id}/status")
async def update_recipe_status(recipe_id: UUID, status: str, db: AsyncSession = Depends(get_db)):
    """
    Update the status of a recipe to FROZEN or ACTIVE.
    """
    try:
        if status not in RecipeStatus.__members__:
            raise HTTPException(status_code=400,
                                detail=f"Invalid status. Must be one of: {[s.name for s in RecipeStatus]}")

        recipe = await get_recipe_by_id(db, recipe_id)
        if not recipe:
            raise HTTPException(status_code=404, detail="Recipe not found.")

        recipe.status = RecipeStatus[status]
        await db.commit()
        logger.info(f"Recipe {recipe_id} status updated to {status}")
        return {"status": "updated"}

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Unexpected error updating recipe status: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.put("/recipe/{recipe_id}")
async def edit_recipe(recipe_id: str, recipe_data: RecipeEdit, db: AsyncSession = Depends(get_db)):
    """
    Edit the full data of a recipe.
    """
    try:
        recipe = await get_recipe_by_id(db, UUID(recipe_id))
        if not recipe:
            raise HTTPException(status_code=404, detail="Recipe not found.")

        recipe_data_dict = recipe_data.model_dump()
        for key, value in recipe_data_dict.items():
            setattr(recipe, key, value)

        await db.commit()
        await db.refresh(recipe)
        logger.info(f"Recipe {recipe_id} edited successfully.")
        return recipe
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Error editing recipe: {e}")
        raise HTTPException(status_code=500, detail="Error editing recipe")


@router.get("/recipes", response_model=List[RecipeResponse])
async def get_all_recipes_endpoint(db: AsyncSession = Depends(get_db)):
    """
    Get all recipes from the database.
    """
    try:
        recipes = await get_all_recipes(db)
        return recipes
    except Exception as e:
        logger.error(f"Error retrieving all recipes: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving recipes")


@router.get("/recipe/{recipe_id}")
async def get_recipe_with_id(recipe_id: str, db: AsyncSession = Depends(get_db)):
    """
    Get recipe by ID.
    """
    task_result = AsyncResult(id=recipe_id, app=celery_app)

    try:
        response = {
            "recipe_id": str(recipe_id),
            "status": task_result.state,
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail="Recipe not found")

    if task_result.state == "SUCCESS":
        recipe = await get_recipe_by_id(db, UUID(recipe_id))
        if recipe:
            return recipe
        else:
            response["error"] = "Recipe not found in database."
    elif task_result.state == "FAILURE":
        response["error"] = str(task_result.info)

    return response
