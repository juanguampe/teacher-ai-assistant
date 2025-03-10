#!/bin/bash

# Get the PORT from environment variable or use 8000 as default
PORT=${PORT:-8000}

# Start the application with the correct port
exec uvicorn main:app --host 0.0.0.0 --port $PORT
