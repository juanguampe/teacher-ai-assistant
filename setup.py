import os
import subprocess
import sys
import platform

def create_venv():
    """Create a virtual environment"""
    print("Creating virtual environment...")
    subprocess.run([sys.executable, "-m", "venv", "venv"])
    print("Virtual environment created successfully.")

def activate_venv():
    """Return the activation command for the virtual environment"""
    if platform.system() == "Windows":
        return os.path.join("venv", "Scripts", "activate")
    else:
        return os.path.join("venv", "bin", "activate")

def install_dependencies():
    """Install dependencies from requirements.txt"""
    print("Installing dependencies...")
    
    if platform.system() == "Windows":
        pip_path = os.path.join("venv", "Scripts", "pip")
    else:
        pip_path = os.path.join("venv", "bin", "pip")
    
    subprocess.run([pip_path, "install", "-r", "requirements.txt"])
    print("Dependencies installed successfully.")

def setup_env_file():
    """Set up the .env file if it doesn't exist"""
    if not os.path.exists(".env"):
        print("Creating .env file from .env.example...")
        with open(".env.example", "r") as example_file:
            example_content = example_file.read()
        
        with open(".env", "w") as env_file:
            env_file.write(example_content)
        
        print(".env file created. Please update it with your OpenAI API key.")
    else:
        print(".env file already exists.")

def main():
    """Main setup function"""
    print("Setting up Teacher's AI Assistant...")
    
    # Create virtual environment
    create_venv()
    
    # Install dependencies
    install_dependencies()
    
    # Set up .env file
    setup_env_file()
    
    # Print activation instructions
    activate_cmd = activate_venv()
    
    print("\nSetup completed successfully!")
    print("\nTo activate the virtual environment:")
    
    if platform.system() == "Windows":
        print(f"Run: {activate_cmd}")
    else:
        print(f"Run: source {activate_cmd}")
    
    print("\nTo start the application:")
    print("Run: python main.py")
    print("\nThen open your browser and navigate to: http://localhost:8000")

if __name__ == "__main__":
    main()
