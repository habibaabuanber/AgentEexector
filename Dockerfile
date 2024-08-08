FROM python:3.10.12

# Set the USER_AGENT environment variable
ENV USER_AGENT='DockerContainer/1.0'

# Set the working directory
WORKDIR /app

# Copy the requirements file into the image
COPY requirements.txt .

# Install venv
RUN python -m venv venv

# Activate the virtual environment and install dependencies
RUN . venv/bin/activate && pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Copy the entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Run the application using the entrypoint script
ENTRYPOINT ["/entrypoint.sh"]

