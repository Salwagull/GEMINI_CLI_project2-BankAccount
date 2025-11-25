#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Start the FastAPI backend in the background
uvicorn backend.main:app --host 0.0.0.0 --port 8000 &

# Give the backend a moment to start up
echo "Waiting for backend to start..."
sleep 5

# Start the Streamlit frontend
# The Replit webview will automatically connect to the default port (8501)
echo "Starting frontend..."
streamlit run frontend/app.py
