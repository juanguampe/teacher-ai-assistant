import importlib
import sys

def check_dependency(module_name):
    try:
        importlib.import_module(module_name)
        print(f"✅ {module_name} is installed")
        return True
    except ImportError:
        print(f"❌ {module_name} is not installed")
        return False

def main():
    dependencies = [
        "fastapi",
        "uvicorn",
        "python-dotenv",
        "langchain",
        "openai",
        "chromadb",
        "pydantic",
        "jinja2",
        "sqlalchemy",
        "python-multipart",
        "tiktoken"
    ]
    
    all_installed = True
    
    for dependency in dependencies:
        if not check_dependency(dependency):
            all_installed = False
    
    if all_installed:
        print("\nAll dependencies are installed.")
    else:
        print("\nSome dependencies are missing. Please run:")
        print("pip install -r requirements.txt")
    
    return all_installed

if __name__ == "__main__":
    if main():
        sys.exit(0)
    else:
        sys.exit(1)
