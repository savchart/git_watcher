# Use an official Python runtime as the base image
FROM python:3.9.1-slim-buster

# Set the working directory in the container
WORKDIR /app_root

# Copy the local files to the container
COPY . .

#install wget and unzip and delete the apt cache
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Run the create_dataframe script
RUN python scripts/process_db.py

# Check if the db file is present in the root folder
RUN ls | grep -E "app.db"

#run guvicorn
CMD ["gunicorn", "app_run:app", "-b", "localhost:5000"]
