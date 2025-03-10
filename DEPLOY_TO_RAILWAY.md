# Deploying Teacher's AI Assistant to Railway

This guide provides step-by-step instructions for deploying the Teacher's AI Assistant application to Railway.

## Prerequisites

1. A Railway account (sign up at [railway.app](https://railway.app))
2. Your GitHub repository with the application code

## Deployment Steps

### 1. Connect Your GitHub Repository

1. Log in to your Railway account
2. Click on "New Project" button
3. Select "Deploy from GitHub repo"
4. Connect your GitHub account if you haven't already
5. Select the repository containing your Teacher's AI Assistant code
6. Railway will automatically detect the configuration files and start the deployment

### 2. Configure Environment Variables

After the project is created, you'll need to set up your OpenAI API key:

1. Go to your project in the Railway dashboard
2. Click on the "Variables" tab
3. Add the following environment variables:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `CHROMA_DB_DIR`: `./chroma_db` (this should already be set in the configuration)
   - `DATABASE_URL`: `sqlite:///./app.db` (or use Railway's PostgreSQL if you prefer)

### 3. Upload Documents

Once your application is deployed, you can use the document upload feature we added:

1. Go to your deployed application URL (provided by Railway)
2. Scroll down to find the "Upload Documents" section
3. Click "Choose File" and select a JSON document
4. Click "Upload Document"
5. The document will be uploaded, processed, and added to the AI's knowledge base

### 4. Verify Deployment

1. Test the chat functionality to ensure everything is working correctly
2. Try asking questions about the documents you've uploaded

## Advantages of Railway

1. **Persistent Storage**: Railway provides persistent storage, so your uploaded documents will remain available between deployments
2. **Automatic Deployments**: Any changes pushed to your GitHub repository will automatically trigger a new deployment
3. **Free Tier**: Railway offers a generous free tier with $5 credit per month
4. **Scaling**: Easy to scale as your application grows

## Troubleshooting

If you encounter any issues during deployment:

1. Check the deployment logs in the Railway dashboard
2. Verify that all environment variables are set correctly
3. Make sure your OpenAI API key is valid and has sufficient credits
4. Check that the application is properly configured to use the persistent storage

## Maintenance

To update your application after making changes:

1. Commit your changes to your Git repository
2. Push the changes to GitHub
3. Railway will automatically detect the changes and redeploy your application
