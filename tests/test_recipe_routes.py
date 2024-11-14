import pytest
import httpx
from uuid import uuid4
from fastapi.testclient import TestClient

from app.db import init_db
from app.main import app

client = TestClient(app)

@pytest.fixture(scope="session", autouse=True)
async def setup_database():
    await init_db()
    yield

@pytest.fixture
def sample_recipe():
    """Returns a sample recipe data."""
    return {
        "amountOfPersons": 4,
        "dishType": "main",
        "maxCooking": 60,
        "allergiesList": ["nuts", "dairy"],
        "dietRequirements": ["vegetarian"],
        "cuisineList": ["Italian"]
    }

@pytest.mark.asyncio
async def test_generate_recipe(sample_recipe):
    async with httpx.AsyncClient(app=app, base_url="http://test") as async_client:
        response = await async_client.post("/generate_recipe", json=sample_recipe)
        assert response.status_code == 200
        data = response.json()
        assert "recipe_id" in data
        assert data["status"] == "Recipe generation started"

        response = await async_client.post("/generate_recipe?use_weights=true", json=sample_recipe)
        assert response.status_code == 200
        data = response.json()
        assert "recipe_id" in data
        assert data["status"] == "Recipe generation started"

@pytest.mark.asyncio
async def test_update_recipe_status():
    """Test updating the status of a recipe to FROZEN and ACTIVE."""
    async with httpx.AsyncClient(app=app, base_url="http://test") as async_client:

        recipe_id = str(uuid4())

        response = await async_client.patch(f"/recipe/{recipe_id}/status", params={"status": "FROZEN"})
        assert response.status_code == 404
        assert response.json() == {"detail": "Recipe not found"}


@pytest.mark.asyncio
async def test_edit_recipe():
    """Test editing an existing recipe."""
    async with httpx.AsyncClient(app=app, base_url="http://test") as async_client:

        recipe_id = str(uuid4())
        edit_data = {
            "amountOfPersons": 2,
            "dishType": "dessert",
            "maxCooking": 30,
            "allergiesList": ["gluten"],
            "dietRequirements": ["gluten-free"],
            "cuisineList": ["Mexican"]
        }

        response = await async_client.put(f"/recipe/{recipe_id}", json=edit_data)
        assert response.status_code == 404
        assert response.json() == {"detail": "Recipe not found"}


@pytest.mark.asyncio
async def test_get_all_recipes():
    """Test retrieval of all recipes from the database."""
    async with httpx.AsyncClient(app=app, base_url="http://test") as async_client:

        response = await async_client.get("/recipes")
        assert response.status_code == 200
        assert isinstance(response.json(), list)


