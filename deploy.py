#!/usr/bin/env python3
"""
Deployment Script for Step 4

This script helps with deploying the application to cloud services like Render or Railway.
It will be used in Step 4 of the development process.
"""

import os
import argparse
import subprocess
import json
import sys

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        # Check if git is installed
        subprocess.run(["git", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("✅ Git is installed")
    except (subprocess.SubprocessError, FileNotFoundError):
        print("❌ Git is not installed. Please install Git: https://git-scm.com/downloads")
        return False
    
    return True

def init_git_repo():
    """Initialize a git repository if not already initialized"""
    if not os.path.exists(".git"):
        print("Initializing git repository...")
        subprocess.run(["git", "init"], check=True)
        print("✅ Git repository initialized")
    else:
        print("✅ Git repository already initialized")

def create_render_config():
    """Create a render.yaml file for Render deployment"""
    render_config = {
        "services": [
            {
                "type": "web",
                "name": "teacher-ai-assistant",
                "env": "python",
                "buildCommand": "pip install -r requirements.txt",
                "startCommand": "uvicorn main:app --host 0.0.0.0 --port $PORT",
                "envVars": [
                    {
                        "key": "OPENAI_API_KEY",
                        "sync": "false"
                    },
                    {
                        "key": "DATABASE_URL",
                        "fromDatabase": {
                            "name": "teacher-ai-db",
                            "property": "connectionString"
                        }
                    }
                ],
                "disk": {
                    "name": "data",
                    "mountPath": "/data",
                    "sizeGB": 1
                }
            }
        ],
        "databases": [
            {
                "name": "teacher-ai-db",
                "type": "postgresql"
            }
        ]
    }
    
    with open("render.yaml", "w") as f:
        json.dump(render_config, f, indent=2)
    
    print("✅ Created render.yaml for Render deployment")

def create_railway_config():
    """Create a railway.json file for Railway deployment"""
    railway_config = {
        "$schema": "https://railway.app/railway.schema.json",
        "build": {
            "builder": "NIXPACKS",
            "buildCommand": "pip install -r requirements.txt"
        },
        "deploy": {
            "startCommand": "uvicorn main:app --host 0.0.0.0 --port $PORT",
            "restartPolicyType": "ON_FAILURE",
            "restartPolicyMaxRetries": 10
        }
    }
    
    with open("railway.json", "w") as f:
        json.dump(railway_config, f, indent=2)
    
    print("✅ Created railway.json for Railway deployment")

def create_procfile():
    """Create a Procfile for Heroku-compatible platforms"""
    with open("Procfile", "w") as f:
        f.write("web: uvicorn main:app --host 0.0.0.0 --port $PORT")
    
    print("✅ Created Procfile for Heroku-compatible platforms")

def prepare_for_deployment(platform):
    """Prepare the application for deployment to the specified platform"""
    if not check_dependencies():
        return
    
    init_git_repo()
    
    if platform == "render":
        create_render_config()
    elif platform == "railway":
        create_railway_config()
    elif platform == "all":
        create_render_config()
        create_railway_config()
        create_procfile()
    else:
        print(f"Unsupported platform: {platform}")
        return
    
    print("\n✅ Deployment preparation complete!")
    print("\nNext steps:")
    
    if platform == "render" or platform == "all":
        print("\nFor Render deployment:")
        print("1. Create a new account on Render (https://render.com)")
        print("2. Connect your GitHub/GitLab repository")
        print("3. Use the render.yaml file for Blueprint deployment")
    
    if platform == "railway" or platform == "all":
        print("\nFor Railway deployment:")
        print("1. Create a new account on Railway (https://railway.app)")
        print("2. Connect your GitHub repository")
        print("3. Create a new project from your repository")
        print("4. Add environment variables (OPENAI_API_KEY)")
    
    print("\nRemember to update your .env file with the appropriate values for production!")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Prepare the application for deployment")
    parser.add_argument("platform", choices=["render", "railway", "all"], 
                        help="The platform to deploy to (render, railway, or all)")
    
    args = parser.parse_args()
    prepare_for_deployment(args.platform)

if __name__ == "__main__":
    main()
