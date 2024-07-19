# LLMFlow - Backend

LLMFlow - A programming language for LLM Apps

## How to use Virtual Environment

1. Install pipenv via `pip install pipenv` (Make sure you also set pipenv in your computer's environment variables)
2. Install dependencies with `pipenv install -d`
3. Start the virtual environment with `pipenv shell`

## How to run the API locally

1. To boot up the API, run: `pipenv run start`
   > Executing the API in this manner allows for the application to automatically relaunch on edits to the scripts
2. Application should open on `http://localhost:8000`
3. To access the API docs, go to `http://localhost:8000/docs` or `http://localhost:8000/redoc`
   > The docs are a way to see what endpoints are available, and make test calls to the given endpoints.

## How to make commits

This project uses `enforce-git-message`, which requires commit messages to follow a standard which `python-semantic-release` can understand (Refer to [How to get/update the project version](#how-to-getupdate-the-project-version)).

Once a commit has been made using the Angular format, then run `pipenv run release` in the terminal. This will allow `python-semantic-release` to automatically update the [CHANGELOG.md](https://github.com/DevArtech/llmflow-backend/blob/main/CHANGELOG.md) and commit the changes, then automatically fetch the pushed changes.
> Note: If the change does not immediately require a CHANGELOG update, you can push as normal without running the command

## How to get/update the project version

Before using, make sure you have a [Github personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) set in your environment variables on your device.

This project uses `python-semantic-release` which will automatically update the [Changelog.md](https://github.com/DevArtech/llmflow-backend/blob/main/CHANGELOG.md) and the version of the project when commits are titled to match the Angular format. The following are the standard types:

- `feat`: New feature (+0.1.0)
- `fix`: Bug fix (+0.0.1)
- `docs`: Documentation changes (+0)
- `style`: Code style changes (+0)
- `refactor`: Code changes without fixing bugs or adding features (+0)
- `perf`: Performance improvements (+0.0.1)
- `test`: Testing changes (+0)
- `chore`: Build process or auxiliary tool changes (+0)
- `build`: Project build (+0)
- `ci`: CI/CD changes (+0)

An example of a commit message which would initate a version change is: `feat: added world domination`

> All major, minor, and patch changes will be reflected in the [CHANGELOG.md](https://github.com/DevArtech/llmflow-backend/blob/main/CHANGELOG.md)

You can check the current version by running `pipenv run version`
