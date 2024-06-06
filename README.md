# llmflow-backend

LLMFlow - A programming language for LLM Apps

## How to use Virtual Environment

1. Install pipenv via `pip install pipenv`
2. Install dependencies with `python -m pipenv install` or just `pipenv install`
3. Start the virtual environment with `python -m pipenv shell` or `pipenv shell`

## How to run the API locally

1. While in a virtual environment, first run `cd src`, then run `uvicorn main:app --reload`
   > Executing the API in this manner allows for the application to automatically relaunch on edits to the scripts
2. Application should open on `http://localhost:8000`
3. To access the API docs, go to `http://localhost:8000/docs`
   > The docs are a way to see what endpoints are available, and make test calls to the given endpoints.
