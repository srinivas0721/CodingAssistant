#!/bin/bash

echo "Starting CP Assistant Backend..."

if [ ! -f .env ]; then
    echo "Error: .env file not found!"
    echo "Please copy .env.example to .env and add your GOOGLE_API_KEY"
    exit 1
fi

source .env

if [ -z "$GOOGLE_API_KEY" ]; then
    echo "Error: GOOGLE_API_KEY not set in .env file"
    exit 1
fi

cd backend
python -m uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000} --reload
