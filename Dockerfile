FROM python:3.11-slim as base

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

# ---------------------
# Test stage
# ---------------------
FROM base as test

COPY ./tests /code/tests

CMD ["pytest"]

# ---------------------
# Development stage
# ---------------------
FROM base as dev

CMD ["fastapi", "run", "app/main.py", "--port", "8000"]

# ---------------------
# Production stage
# ---------------------
FROM base as production

CMD ["fastapi", "run", "app/main.py", "--port", "8000", "--workers", "4"]