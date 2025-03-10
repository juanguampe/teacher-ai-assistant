import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment
api_key = os.getenv("OPENAI_API_KEY")
print(f"API key loaded: {api_key[:5]}...{api_key[-5:]}")

def test_chat_completions():
    """Test the Chat Completions API using requests"""
    print("\n--- Testing Chat Completions API ---")
    
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello, how are you?"}
        ],
        "max_tokens": 50
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise an exception for 4XX/5XX responses
        
        result = response.json()
        print("✅ Chat Completions API is working!")
        print(f"Response: {result['choices'][0]['message']['content']}")
        return True
    except Exception as e:
        print(f"❌ Chat Completions API error: {str(e)}")
        print(f"Response status code: {response.status_code if 'response' in locals() else 'N/A'}")
        print(f"Response text: {response.text if 'response' in locals() else 'N/A'}")
        return False

def test_assistants_api():
    """Test the Assistants API using requests"""
    print("\n--- Testing Assistants API ---")
    assistant_id = "asst_x3bKYpzO7PntzgPuMDItvLdm"
    
    base_url = "https://api.openai.com/v1"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "OpenAI-Beta": "assistants=v1"
    }
    
    try:
        # Retrieve the assistant
        assistant_url = f"{base_url}/assistants/{assistant_id}"
        assistant_response = requests.get(assistant_url, headers=headers)
        assistant_response.raise_for_status()
        assistant_data = assistant_response.json()
        print(f"✅ Assistant retrieved: {assistant_data.get('name', 'Unnamed')}")
        
        # Create a thread
        thread_url = f"{base_url}/threads"
        thread_response = requests.post(thread_url, headers=headers, json={})
        thread_response.raise_for_status()
        thread_data = thread_response.json()
        thread_id = thread_data["id"]
        print(f"✅ Thread created: {thread_id}")
        
        # Add a message to the thread
        message_url = f"{base_url}/threads/{thread_id}/messages"
        message_data = {
            "role": "user",
            "content": "Hello, how are you?"
        }
        message_response = requests.post(message_url, headers=headers, json=message_data)
        message_response.raise_for_status()
        print(f"✅ Message added to thread")
        
        # Run the assistant
        run_url = f"{base_url}/threads/{thread_id}/runs"
        run_data = {
            "assistant_id": assistant_id
        }
        run_response = requests.post(run_url, headers=headers, json=run_data)
        run_response.raise_for_status()
        run_data = run_response.json()
        print(f"✅ Run created: {run_data['id']}")
        
        print("Run status: ", run_data["status"])
        print("The run is now in progress. In a real application, you would poll for completion.")
        return True
    except Exception as e:
        print(f"❌ Assistants API error: {str(e)}")
        return False

if __name__ == "__main__":
    chat_success = test_chat_completions()
    assistants_success = test_assistants_api()
    
    print("\n--- Summary ---")
    print(f"Chat Completions API: {'✅ Working' if chat_success else '❌ Not working'}")
    print(f"Assistants API: {'✅ Working' if assistants_success else '❌ Not working'}")
