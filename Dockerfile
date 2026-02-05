FROM python:3.13.2-slim-bookworm

RUN pip install uv

## envything in the env is globally available

WORKDIR /app

ENV PATH="/app/ •venv/bin: $PATH"


# Copy dependency files
COPY .python-version pyproject.toml uv.lock ./

# Install dependencies using uv
RUN uv sync --frozen --no-cache

# Copy application code and models
COPY RULService ./RULService
COPY Models ./Models

EXPOSE 9696

# Use uv run to execute uvicorn with the correct app path
CMD ["uv", "run", "uvicorn", "RULService.api.rulapi:app", "--host", "0.0.0.0", "--port", "9696"]



