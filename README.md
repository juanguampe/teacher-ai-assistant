# Teacher's AI Assistant

A web-based AI assistant for teachers using FastAPI, LangChain, and OpenAI's API. This application allows teachers to ask questions about internal school policies and procedures in a chat-like web interface.

## Features

- Chat interface for teachers to ask questions
- AI responses based on internal documents (using LangChain and Vector Store)
- Conversation history (threaded chats)
- FastAPI backend with OpenAI integration

## Project Structure

```
teacher-ai-assistant/
├── app/
│   ├── api/            # API routes
│   ├── db/             # Database models and utilities
│   ├── models/         # Pydantic models
│   ├── static/         # Static files (CSS, JS)
│   ├── templates/      # HTML templates
│   └── utils/          # Utility functions
├── .env                # Environment variables
├── .env.example        # Example environment variables
├── main.py             # Main application entry point
└── requirements.txt    # Python dependencies
```

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- OpenAI API key

### Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd teacher-ai-assistant
```

2. Create a virtual environment:

```bash
python -m venv venv
```

3. Activate the virtual environment:

- On Windows:
```bash
venv\Scripts\activate
```

- On macOS/Linux:
```bash
source venv/bin/activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Set up environment variables:

Copy the `.env.example` file to `.env` and update the values:

```bash
cp .env.example .env
```

Edit the `.env` file and add your OpenAI API key.

### Running the Application

1. Start the application:

```bash
python main.py
```

2. Open your browser and navigate to:

```
http://localhost:8000
```

## Development Roadmap

### Step 1: Basic Project Setup (Current)

- FastAPI backend with endpoints
- Simple chat API endpoint (/chat) connected to OpenAI
- Basic web UI

### Step 2: Integrate LangChain & Vector Store

- Store internal documents in a Vector Database (ChromaDB)
- Implement document retrieval using LangChain
- Modify the chat endpoint to retrieve relevant documents before calling OpenAI

### Step 3: Implement Conversation History

- Add a database to store chat history per user
- Modify the API for continuing previous conversations
- Ensure the AI remembers context within a thread

### Step 4: Deployment & Testing

- Local testing
- Deployment setup for cloud services (Render, Railway)
- Performance and scalability optimization

## License

[MIT License](LICENSE)
