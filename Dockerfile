# Use the official Python image as a base
FROM python:3.12-slim

# Set the working directory
WORKDIR /

# Copy the current directory contents into the container at /app
COPY . .

# Install the required dependencies
RUN pip install fastapi \
    uvicorn \
    python-multipart \
    python-dotenv \
    requests \
    pydantic \
    sqlalchemy \
    scikit-learn \
    numpy \
    pillow \
    bs4 \
    docstring_parser \
    python-dateutil \
    uv \
    duckdb \
    Markdown \
    
RUN npm install -g prettier



# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
