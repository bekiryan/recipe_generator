# Recipe Generation API

This API provides endpoints for managing recipe generation tasks, updating recipe statuses, editing recipes, and retrieving recipe data. It uses FastAPI for API routing and Celery for background task processing, integrated with an asynchronous SQLAlchemy database.

## Requirements
Install the dependencies from `requirements.txt`:
```bash
pip install -r requirements.txt
```

## Getting Started

### 1. Start the Application
To run the application, first, setup redis server and start the celery worker:
```bash
celery -A app.api.routes.recipe_routes worker --loglevel=info
```
Add your openai API key to the `.env` file:
```
OPENAI_API_KEY=your_openai_api_key
```

Then, start the FastAPI application:
```bash
uvicorn app.main:app --reload
```

### 2. Access the Swagger UI
Once the application is running, access the interactive API documentation at:
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Running Tests
To run the tests, use the following command:

```bash
pytest
```
