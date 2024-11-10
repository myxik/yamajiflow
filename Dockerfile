# Use a lightweight official Python base image
FROM python:3.9-slim AS base

# Set environment variables for consistent, non-interactive installs
ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.5.1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true

# Install essential system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl build-essential && \
    rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Set PATH to include Poetry
ENV PATH="${PATH}:/root/.local/bin"

# Set working directory
WORKDIR /app

# Copy only the Poetry files to leverage Docker caching
COPY pyproject.toml poetry.lock /app/

# Install dependencies with Poetry
RUN poetry install --no-root --only main

# Copy the rest of the application code
COPY . /app

# Build stage for removing unnecessary dependencies
FROM python:3.9-slim AS production

# Copy Poetry dependencies and app code from the previous stage
COPY --from=base /app /app

# Set the final working directory and PATH
WORKDIR /app
ENV PATH="/app/.venv/bin:$PATH"

# Define command for starting the app
# CMD ["poetry", "run", "python", "-m", "jyflow"]
