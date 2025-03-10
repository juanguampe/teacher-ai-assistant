document.addEventListener('DOMContentLoaded', function() {
    // DOM elements
    const chatContainer = document.getElementById('chat-container');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    
    // Current conversation ID (will be set when first message is sent)
    let conversationId = null;
    
    // Function to add a message to the chat container
    function addMessage(content, role) {
        const messageDiv = document.createElement('div');
        messageDiv.className = role + '-message';
        
        const messageContent = document.createElement('p');
        messageContent.textContent = content;
        messageDiv.appendChild(messageContent);
        
        const timeDiv = document.createElement('div');
        timeDiv.className = 'message-time';
        timeDiv.textContent = new Date().toLocaleTimeString();
        messageDiv.appendChild(timeDiv);
        
        chatContainer.appendChild(messageDiv);
        
        // Scroll to bottom
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
    
    // Function to show typing indicator
    function showTypingIndicator() {
        const indicator = document.createElement('div');
        indicator.className = 'typing-indicator';
        indicator.id = 'typing-indicator';
        
        for (let i = 0; i < 3; i++) {
            const dot = document.createElement('span');
            indicator.appendChild(dot);
        }
        
        chatContainer.appendChild(indicator);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
    
    // Function to remove typing indicator
    function removeTypingIndicator() {
        const indicator = document.getElementById('typing-indicator');
        if (indicator) {
            indicator.remove();
        }
    }
    
    // Function to send message to API
    async function sendMessage(message) {
        try {
            showTypingIndicator();
            
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: message,
                    conversation_id: conversationId
                })
            });
            
            const data = await response.json();
            
            // Remove typing indicator
            removeTypingIndicator();
            
            // Update conversation ID if this is a new conversation
            if (!conversationId) {
                conversationId = data.conversation_id;
            }
            
            // Add assistant's response to chat
            addMessage(data.message, 'assistant');
            
        } catch (error) {
            console.error('Error sending message:', error);
            removeTypingIndicator();
            addMessage('Sorry, there was an error processing your request. Please try again.', 'system');
        }
    }
    
    // Event listener for send button
    sendButton.addEventListener('click', function() {
        const message = userInput.value.trim();
        
        if (message) {
            // Add user message to chat
            addMessage(message, 'user');
            
            // Clear input field
            userInput.value = '';
            
            // Send message to API
            sendMessage(message);
        }
    });
    
    // Event listener for Enter key
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendButton.click();
        }
    });
    
    // Focus input field on page load
    userInput.focus();
    
    // Document upload functionality
    const uploadForm = document.getElementById('upload-form');
    const documentFile = document.getElementById('document-file');
    const uploadStatus = document.getElementById('upload-status');

    uploadForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        if (!documentFile.files[0]) {
            uploadStatus.innerHTML = '<div class="alert alert-warning">Please select a file to upload</div>';
            return;
        }
        
        const file = documentFile.files[0];
        if (!file.name.endsWith('.json')) {
            uploadStatus.innerHTML = '<div class="alert alert-warning">Please upload a JSON file</div>';
            return;
        }
        
        uploadStatus.innerHTML = '<div class="alert alert-info">Uploading document...</div>';
        
        const formData = new FormData();
        formData.append('file', file);
        
        try {
            const response = await fetch('/api/upload-document', {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            
            if (result.success) {
                uploadStatus.innerHTML = `<div class="alert alert-success">${result.message}</div>`;
                documentFile.value = '';
            } else {
                uploadStatus.innerHTML = `<div class="alert alert-danger">${result.message}</div>`;
            }
        } catch (error) {
            console.error('Error uploading document:', error);
            uploadStatus.innerHTML = '<div class="alert alert-danger">Error uploading document. Please try again.</div>';
        }
    });
});
