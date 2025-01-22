FROM python:3.11-slim AS base

WORKDIR /code

RUN apt-get -y update && apt-get -y upgrade && apt-get install -y --no-install-recommends ffmpeg

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

# ---------------------
# Test stage
# ---------------------
FROM base AS test

COPY ./tests /code/tests

CMD ["pytest"]

# ---------------------
# Development stage
# ---------------------
FROM base AS dev

CMD ["fastapi", "run", "app/main.py", "--port", "8000"]

# ---------------------
# Production stage
# ---------------------
FROM base AS prod

CMD ["fastapi", "run", "app/main.py", "--port", "8000", "--workers", "4"]