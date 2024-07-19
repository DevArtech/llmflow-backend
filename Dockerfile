FROM python:3.11-slim
WORKDIR /
COPY Pipfile /
RUN pip install --no-cache-dir pipenv
RUN pipenv lock
RUN pipenv install --deploy --system
COPY . /
EXPOSE 80
CMD ["pipenv", "run", "start"]
