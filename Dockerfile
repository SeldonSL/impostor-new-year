FROM python:3.12-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy dependency files
COPY pyproject.toml .

# Install dependencies
RUN uv sync --no-install-project --no-dev

# Copy application code
COPY . .

# Create volume mount point for SQLite database
VOLUME ["/app/data"]

# Expose port
EXPOSE 8000

# Run migrations and start server
CMD ["sh", "-c", "uv run python manage.py migrate && uv run gunicorn impostor_project.wsgi:application --bind 0.0.0.0:8000"]
