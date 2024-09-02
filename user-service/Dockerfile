FROM python:3.12.5-alpine

WORKDIR /app

COPY . .

RUN pip install poetry

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction
    
CMD alembic upgrade head
