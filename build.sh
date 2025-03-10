#!/bin/bash
# Build script for Render deployment (Free tier)

echo "Starting build process..."

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "Creating directories..."
mkdir -p ./chroma_db || echo "Failed to create ./chroma_db"
mkdir -p documents/json || echo "Failed to create documents/json"

# Initialize the database
echo "Initializing database..."
python -c "from app.db.models import init_db; init_db()" || echo "Failed to initialize database"

# Ingest documents if they exist
echo "Checking for documents to ingest..."
if [ -d "documents/json" ] && [ "$(ls -A documents/json 2>/dev/null)" ]; then
    echo "Ingesting documents..."
    python ingest_documents.py --documents-dir ./documents/json --persist-dir ./chroma_db || echo "Failed to ingest documents"
else
    echo "No documents to ingest or directory doesn't exist"
fi

echo "Build completed successfully!"
