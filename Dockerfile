
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run the application
CMD ["python", "script/main.py"]