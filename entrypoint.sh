#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# This script is the entrypoint for the Docker container.
# Its purpose is to run database migrations before starting the main application.

# Step 1: Run Alembic database migrations.
# The 'alembic upgrade head' command applies any pending migration scripts
# to the database, bringing it up to date with the latest schema.
echo "Running database migrations..."
alembic upgrade head

# Step 2: Start the main application.
# The 'exec "$@"' command takes all the arguments passed to this script
# (which will be the CMD from the Dockerfile) and executes them.
# In our case, it will run: uvicorn app.main:app --host 0.0.0.0 --port 8000
echo "Starting application..."
exec "$@"