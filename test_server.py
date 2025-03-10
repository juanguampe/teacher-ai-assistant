import requests
import sys

def test_server():
    try:
        response = requests.get("http://localhost:8000")
        print(f"Server is running. Status code: {response.status_code}")
        print(f"Response: {response.text[:100]}...")
        return True
    except requests.exceptions.ConnectionError:
        print("Server is not running or not accessible.")
        return False

if __name__ == "__main__":
    if test_server():
        sys.exit(0)
    else:
        sys.exit(1)
