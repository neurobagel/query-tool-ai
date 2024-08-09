#!/bin/bash

# Start the Ollama services first
ollama serve &
ollama run mistral &

# Start the FastAPI application
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Wait for all background processes to complete
wait
