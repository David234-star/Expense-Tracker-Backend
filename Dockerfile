# # Use an official Python runtime as a parent image
# FROM python:3.9-slim

# # Set the working directory in the container
# WORKDIR /code

# # Copy the requirements file into the container at /code
# COPY ./requirements.txt /code/requirements.txt

# # Install any needed packages specified in requirements.txt
# RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt && alembic upgrade head

# # Copy the application code into the container
# COPY ./app /code/app

# # Expose the port the app runs on
# EXPOSE 8000

# # Run uvicorn server.
# # The host 0.0.0.0 makes the server accessible from outside the container.
# # The --port will be set by Render automatically, but we can default it.
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /code

# Copy the requirements file and install dependencies
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the application code into the container
COPY ./app /code/app
COPY ./alembic /code/alembic
COPY ./alembic.ini /code/alembic.ini

# --- NEW STEPS ---
# Copy the entrypoint script into the container
COPY ./entrypoint.sh /code/entrypoint.sh
# Ensure it has execute permissions inside the container
RUN chmod +x /code/entrypoint.sh

# --- Use the script as the entrypoint ---
ENTRYPOINT ["/code/entrypoint.sh"]

# The CMD is now passed as an argument to the entrypoint script
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]