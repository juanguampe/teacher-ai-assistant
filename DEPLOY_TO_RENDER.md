# Deploying Teacher's AI Assistant to Render

This guide provides step-by-step instructions for deploying the Teacher's AI Assistant application to Render.

## Prerequisites

1. A Render account (sign up at [render.com](https://render.com))
2. A GitHub or GitLab account to host your repository
3. OpenAI API key

## Deployment Steps

### 1. Prepare Your Repository

1. Make sure your code is committed to a Git repository:

```bash
git add .
git commit -m "Prepare for Render deployment"
```

2. Push your repository to GitHub or GitLab:

```bash
# For GitHub
git remote add origin https://github.com/yourusername/teacher-ai-assistant.git
git push -u origin main

# For GitLab
git remote add origin https://gitlab.com/yourusername/teacher-ai-assistant.git
git push -u origin main
```

### 2. Deploy to Render

1. Log in to your Render account
2. Click on the "New +" button and select "Blueprint"
3. Connect your GitHub or GitLab account if you haven't already
4. Select the repository containing your Teacher's AI Assistant code
5. Render will automatically detect the `render.yaml` file and configure your services
6. Click "Apply" to create the services defined in the Blueprint

### 3. Configure Environment Variables

After the services are created, you'll need to set up your OpenAI API key:

1. Go to the "teacher-ai-assistant" web service in your Render dashboard
2. Click on "Environment" in the left sidebar
3. Find the "OPENAI_API_KEY" variable
4. Click "Edit" and enter your OpenAI API key
5. Click "Save Changes"

### 4. Upload Documents

To upload your JSON documents to the persistent disk:

1. Go to the "teacher-ai-assistant" web service in your Render dashboard
2. Click on "Shell" in the left sidebar
3. Use the following commands to upload your documents:

```bash
# Create the documents directory if it doesn't exist
mkdir -p /data/documents/json

# Upload your JSON files (example using cat)
cat > /data/documents/json/your_file.json << 'EOL'
{
  "your": "json",
  "content": "here"
}
EOL

# Run the document ingestion script
python ingest_documents.py --documents-dir /data/documents/json --persist-dir /data/chroma_db
```

### 5. Verify Deployment

1. Once the deployment is complete, click on the URL provided by Render to access your application
2. Test the chat functionality to ensure everything is working correctly

## Troubleshooting

If you encounter any issues during deployment:

1. Check the logs in the Render dashboard for error messages
2. Verify that all environment variables are set correctly
3. Make sure your OpenAI API key is valid and has sufficient credits
4. Check that the persistent disk is properly mounted and accessible

## Maintenance

To update your application after making changes:

1. Commit your changes to your Git repository
2. Push the changes to GitHub or GitLab
3. Render will automatically detect the changes and redeploy your application

## Resources

- [Render Documentation](https://render.com/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [OpenAI API Documentation](https://platform.openai.com/docs/api-reference)
