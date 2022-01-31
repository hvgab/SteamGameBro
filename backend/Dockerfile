
FROM python:3.10

RUN pip install pipenv

ENV PROJECT_DIR /app

WORKDIR ${PROJECT_DIR}

COPY Pipfile Pipfile.lock ${PROJECT_DIR}

RUN pipenv install --system --deploy

WORKDIR /app/steambro
