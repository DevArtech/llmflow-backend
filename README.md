# LLMFlow - Backend

LLMFlow - A programming language for LLM Apps

## How to use Virtual Environment

1. Install pipenv via `pip install pipenv` (Make sure you also set pipenv in your computer's environment variables)
2. Install dependencies with `pipenv install`
3. Start the virtual environment with `pipenv shell`

## How to run the API locally

1. To boot up the API, run: `pipenv run start`
   > Executing the API in this manner allows for the application to automatically relaunch on edits to the scripts
2. Application should open on `http://localhost:8000`
3. To access the API docs, go to `http://localhost:8000/docs` or `http://localhost:8000/redoc`
   > The docs are a way to see what endpoints are available, and make test calls to the given endpoints.
