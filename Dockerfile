# Use the official Python image as a base
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install the required dependencies
RUN pip install fastapi \
    uvicorn \
    python-multipart \
    python-dotenv \
    requests \
    pydantic \
    aiofiles \
    python-jose[cryptography] \
    passlib[bcrypt] \
    sqlalchemy \
    scikit-learn \
    numpy \
    pillow \
    bs4 \
    docstring_parser \
    python-dateutil \
    uv \



# Expose the port the app runs on
EXPOSE 8030

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]