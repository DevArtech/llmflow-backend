FROM python:3.11-slim
WORKDIR /
COPY pipfile /
RUN pip install --no-cache-dir pipenv
RUN pipenv lock
RUN pipenv install --deploy --system
COPY . /
EXPOSE 80
CMD ["uvicorn", "--app-dir", "src", "main:app", "--host", "0.0.0.0", "--port", "80"]
