import os
import pandas as pd
from dotenv import load_dotenv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from google import genai

# Load environment variables
GENAI_API_KEY="AIzaSyDHYEMLgM9ID1Z--FlXB6WDmxD8ojPNIuw"
load_dotenv()
api_key = GENAI_API_KEY
if not api_key:
    raise ValueError("API key not found. Please set the GENAI_API_KEY environment variable.")

# Initialize GenAI client
client = genai.Client(api_key=api_key)

# Load knowledge base
knowledge_base_path = "data/knowledge_base.csv"
knowledge_base = pd.read_csv(knowledge_base_path)
knowledge_base['combined_text'] = (
    knowledge_base['short_description'] + " " +
    knowledge_base['resolution'] + " " +
    knowledge_base['combined_text']
)  # Adjust columns as needed

# Initialize TF-IDF Vectorizer for retrieval
vectorizer = TfidfVectorizer()
knowledge_base_vectors = vectorizer.fit_transform(knowledge_base['combined_text'])

# Conversation history storage
conversation_history = {}

def get_relevant_knowledge(prompt):
    """Retrieve the most relevant knowledge base entries for a given prompt."""
    prompt_vector = vectorizer.transform([prompt])
    similarities = cosine_similarity(prompt_vector, knowledge_base_vectors)
    top_indices = similarities.argsort()[0][-3:]  # Get top 3 relevant rows
    return "\n".join(knowledge_base.iloc[top_indices]['combined_text'])

def chat_with_aii(session_id, prompt):
    """Handles chat logic, including retrieving relevant data and generating a response."""
    if session_id not in conversation_history:
        conversation_history[session_id] = [
            "You are a technical support assistant for a software platform. Your role is to help users troubleshoot issues, provide guidance on using the platform, and answer technical questions."
        ]

    conversation_history[session_id].append(f"User: {prompt}")

    retrieved_data = get_relevant_knowledge(prompt)
    dataset_context = f"Here is some relevant information from the knowledge base:\n{retrieved_data}\n"
    context = dataset_context + "\n".join(conversation_history[session_id]) + "\nAI:"

    # Call GenAI to generate a response
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=context
    )

    ai_response = response.text
    conversation_history[session_id].append(f"AI: {ai_response}")

    return ai_response
