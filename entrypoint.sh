#!/bin/sh



OPENAI_API_KEY='c2stcHJvai1JY0ItUHJXSW9YVll6akVYcGU0cEw2d2RFOTl3NjFiNDA1WGJwdFJ1VnFOblI4UloxVzV4azBRVmJENUhIN0liQ0RKenNXLWFZaVQzQmxia0ZKNEdQa3Z4aEFoQzRsN3BwVkRNZEx4VThwRDBxUWtscktwakZ6bVQzaTRncVZ1bnFOYTV2eExyYXdsd1RzV0NhYUVCUUZlNGZXd0E='
TAVILY_API_KEY='dHZseS0wNU1BYmJPR3VPWjBCeWJhNTBLbWpmVmtoMEw0Z0cxWA=='


# Decode and export the environment variables
export OPENAI_API_KEY=$(echo $OPENAI_API_KEY | base64 --decode)
export TAVILY_API_KEY=$(echo $TAVILY_API_KEY | base64 --decode)

# Activate the virtual environment
. /app/venv/bin/activate

# Run the application
exec python main.py
