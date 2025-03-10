#!/bin/bash
# Build script for Render deployment

# Install dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p /data/chroma_db
mkdir -p /data/documents/json
mkdir -p documents/json

# Copy JSON documents to the documents directory
cp -r documents/json/* /data/documents/json/ || echo "No JSON documents to copy"

# Initialize the database
python -c "from app.db.models import init_db; init_db()"

# Ingest documents if they exist
if [ -d "/data/documents/json" ] && [ "$(ls -A /data/documents/json)" ]; then
    python ingest_documents.py --documents-dir /data/documents/json --persist-dir /data/chroma_db
fi

echo "Build completed successfully!"
