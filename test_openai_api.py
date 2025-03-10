import os
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment
api_key = os.getenv("OPENAI_API_KEY")
print(f"API key loaded: {api_key[:5]}...{api_key[-5:]}")

# Initialize OpenAI client
client = openai.OpenAI(api_key=api_key)

def test_chat_completions():
    """Test the Chat Completions API"""
    print("\n--- Testing Chat Completions API ---")
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello, how are you?"}
            ],
            max_tokens=50
        )
        print("✅ Chat Completions API is working!")
        print(f"Response: {response.choices[0].message.content}")
        return True
    except Exception as e:
        print(f"❌ Chat Completions API error: {str(e)}")
        return False

def test_assistants_api():
    """Test the Assistants API"""
    print("\n--- Testing Assistants API ---")
    assistant_id = "asst_x3bKYpzO7PntzgPuMDItvLdm"
    
    try:
        # First, retrieve the assistant to verify it exists
        assistant = client.beta.assistants.retrieve(assistant_id=assistant_id)
        print(f"✅ Assistant retrieved: {assistant.name}")
        
        # Create a thread
        thread = client.beta.threads.create()
        print(f"✅ Thread created: {thread.id}")
        
        # Add a message to the thread
        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content="Hello, how are you?"
        )
        print(f"✅ Message added to thread")
        
        # Run the assistant
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant_id
        )
        print(f"✅ Run created: {run.id}")
        
        print("Run status: ", run.status)
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
