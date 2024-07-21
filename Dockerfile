FROM python:3.11-slim

WORKDIR /
COPY Pipfile /
RUN pip install --no-cache-dir pipenv
RUN pipenv lock
RUN pipenv install --system --deploy
COPY . /

EXPOSE 80

CMD ["uvicorn", "--app-dir", "src", "main:app", "--host", "0.0.0.0", "--port", "80"]
