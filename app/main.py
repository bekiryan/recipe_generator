from fastapi import FastAPI
from app.api.routes.recipe_routes import router as recipe_router
from app.db import init_db
app = FastAPI()

app.add_event_handler("startup", init_db)
app.include_router(recipe_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
