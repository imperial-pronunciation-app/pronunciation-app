FROM python:3.11-slim as base

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

# ---------------------
# Development stage
# ---------------------
FROM base as dev-stage

CMD ["fastapi", "run", "app/main.py", "--port", "8000"]

# ---------------------
# Production stage
# ---------------------
FROM base as production-stage

CMD ["fastapi", "run", "app/main.py", "--port", "8000", "--workers", "4"]