# Use Python 3.9 as base image
FROM python:3.9-slim

# Set working directory in container
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application files
COPY . .

# Expose port 8501 (Streamlit's default port)
EXPOSE 8501

# Command to run the application
CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0"] 