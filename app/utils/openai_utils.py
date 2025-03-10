import os
import sys
import json
import traceback
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set the API key directly
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("WARNING: OPENAI_API_KEY is not set in the .env file")
else:
    print(f"API key loaded: {api_key[:5]}...{api_key[-5:]}")

# Dictionary to store conversation history by conversation ID
conversation_history = {}

# Load sample knowledge from JSON files
def load_sample_knowledge():
    """
    Load sample knowledge from JSON files
    
    Returns:
        Dictionary with file names as keys and content as values
    """
    knowledge = {}
    json_dir = "./documents/json"
    
    if not os.path.exists(json_dir):
        print(f"JSON directory {json_dir} does not exist.")
        return knowledge
    
    # Load a sample of each JSON file
    for file_name in os.listdir(json_dir):
        if file_name.endswith(".json"):
            file_path = os.path.join(json_dir, file_name)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Extract a sample of the content
                if isinstance(data, list) and len(data) > 0:
                    # Take first 3 items if it's a list
                    sample = data[:min(3, len(data))]
                    content = json.dumps(sample, ensure_ascii=False, indent=2)
                elif isinstance(data, dict):
                    # Take the dictionary as is
                    content = json.dumps(data, ensure_ascii=False, indent=2)
                else:
                    content = str(data)
                
                # Limit content length
                if len(content) > 2000:
                    content = content[:2000] + "...(truncated)"
                
                knowledge[file_name] = content
                print(f"Loaded sample from {file_name}")
            except Exception as e:
                print(f"Error loading {file_path}: {str(e)}")
    
    return knowledge

# Load sample knowledge
SAMPLE_KNOWLEDGE = load_sample_knowledge()

async def get_openai_response(message: str, conversation_id: str = None) -> str:
    """
    Get a response from OpenAI Chat Completions API using requests.
    
    Args:
        message: The user's message
        conversation_id: Optional conversation ID for continuing a conversation
        
    Returns:
        The AI's response
    """
    try:
        # Get or initialize conversation history
        if conversation_id and conversation_id in conversation_history:
            messages = conversation_history[conversation_id]
        else:
            # Create system message with sample knowledge
            system_content = """
# Instrucciones para el Asistente Educativo - Magis XXI

## 🎯 Propósito
Eres un asistente especializado en pedagogía ignaciana del Colegio San Bartolomé La Merced, diseñado para apoyar a profesores nuevos y experimentados. Tu misión es proporcionar información clara, concisa y práctica sobre cuatro pilares fundamentales:

1. Pedagogía Ignaciana
2. Propuesta educativa Magis XXI
3. Programa de Afectividad
4. Sistema Integrado de Evaluación Escolar (SIEE)

## 📚 Base de Conocimiento
A continuación se presenta una muestra de la información disponible en los documentos:
"""
            
            # Add sample knowledge to system message
            for file_name, content in SAMPLE_KNOWLEDGE.items():
                system_content += f"\n\n### {file_name}:\n{content}\n"
            
            system_content += """
## 🔍 Principios de Respuesta

1. **Precisión Documental**:
   - Responde ÚNICAMENTE con información contenida en la base de conocimiento
   - NUNCA incluyas referencias numéricas como [1], [2], [3], etc. en ninguna parte de tus respuestas
   - Si la información no está disponible, indica: "Esta pregunta requiere consulta adicional con el equipo de Formación en Pedagogía Ignaciana"

2. **Claridad y Accesibilidad**:
   - Utiliza lenguaje sencillo y directo
   - Explica términos técnicos cuando sea necesario
   - Estructura tus respuestas de forma lógica y fácil de seguir

3. **Orientación Práctica**:
   - Proporciona ejemplos concretos de aplicación en el aula
   - Ofrece sugerencias implementables y orientadas a soluciones
   - Relaciona los conceptos teóricos con situaciones reales de enseñanza

4. **Equilibrio Pedagógico**:
   - Honra la tradición ignaciana mientras destacas la innovación de Magis XXI
   - Mantén la confidencialidad institucional (sin revelar información no autorizada)
   - Asegura que tus respuestas reflejen los valores del colegio

## 📝 Formato de Respuesta

Estructura tus respuestas de forma fluida y natural, incluyendo los siguientes elementos sin usar subtítulos, numeración explícita o cualquier tipo de referencia numérica:

- Comienza con una respuesta directa y clara a la pregunta planteada (2-3 oraciones)
- Continúa explicando los conceptos relevantes basándote en los documentos oficiales
- Incluye un ejemplo concreto de aplicación en el aula o en la práctica educativa
- Concluye con un consejo práctico o sugerencia que pueda implementarse inmediatamente

## ⚠️ Limitaciones Importantes

- No generes información que no esté explícitamente en los documentos
- No menciones fuentes externas no incluidas en la base de conocimiento
- No compartas opiniones personales sobre las políticas o prácticas del colegio
- No reveles información confidencial sobre estudiantes, profesores o directivos
- NUNCA incluyas referencias numéricas como [1], [2], [3], etc. al final de tus párrafos o respuestas
- NO utilices notas al pie, superíndices, o cualquier notación similar que indique una referencia
"""
            
            # Start with system message
            messages = [
                {"role": "system", "content": system_content}
            ]
            
            if conversation_id:
                conversation_history[conversation_id] = messages
        
        # Add user message to history
        messages.append({"role": "user", "content": message})
        
        print(f"Sending message to OpenAI: {message[:50]}...")
        
        # Make API request
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        data = {
            "model": "gpt-3.5-turbo-16k",  # Using a model with larger context window
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise an exception for 4XX/5XX responses
        
        result = response.json()
        content = result['choices'][0]['message']['content']
        
        # Add assistant response to history
        messages.append({"role": "assistant", "content": content})
        
        # Update conversation history
        if conversation_id:
            conversation_history[conversation_id] = messages
        
        print(f"Received response from OpenAI: {content[:50]}...")
        return content
        
    except Exception as e:
        print(f"Error calling OpenAI API: {str(e)}")
        print("Exception type:", type(e).__name__)
        print("Exception traceback:")
        traceback.print_exc(file=sys.stdout)
        
        # If we have response details, print them
        if 'response' in locals():
            print(f"Response status code: {response.status_code}")
            print(f"Response text: {response.text}")
        
        # Return a fallback response instead of raising the exception
        return "I'm sorry, I encountered an error while processing your request. Please try again later."
