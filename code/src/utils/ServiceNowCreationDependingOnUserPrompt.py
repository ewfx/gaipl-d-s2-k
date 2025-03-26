import json
import csv
import random

def create_servicenow_incident(user_prompt):
    knowledge_data = load_knowledge_from_csv("data/synthetic_servicenow_incidents_cleaned.csv")
    enriched_prompt = enrich_prompt(user_prompt, knowledge_data)
    print(f"\n[DEBUG] Enriched Prompt: {enriched_prompt}")
    
    ai_response = generate_ai_response(enriched_prompt, knowledge_data)
    if ai_response is None:
        print("[ERROR] Failed to get a valid response from the simulated Gen AI.")
        return None
    
    new_incident = create_incident(ai_response)
    return new_incident

def enrich_prompt(user_prompt, knowledge_data):
    if not knowledge_data:
        return user_prompt
    return f"{user_prompt}. Here is related information from past incidents: "

def generate_ai_response(enriched_prompt, knowledge_data):
    print("\n[DEBUG] Calling simulated Gen AI with prompt:", enriched_prompt)
    
    relevant_incidents = [incident for incident in knowledge_data if incident['Description'].lower() in enriched_prompt.lower() or incident['Category'].lower() in enriched_prompt.lower()]
    
    if relevant_incidents:
        chosen_incident = random.choice(relevant_incidents)
        ai_response = {
            "short_description": chosen_incident['Description'][:80],
            "description": enriched_prompt,
            "category": chosen_incident['Category'],
            "cmdb_ci": "unknown",
            "urgency": "Medium",
            "impact": "Medium"
        }
        print("[DEBUG] Simulated Gen AI response from relevant incident:", ai_response)
        return ai_response
    
    ai_response = {
        "short_description": "General issue reported",
        "description": enriched_prompt,
        "category": "General",
        "cmdb_ci": "unknown",
        "urgency": "Medium",
        "impact": "Medium"
    }
    print("[DEBUG] Simulated Gen AI response (no relevant incident):", ai_response)
    return ai_response

def create_incident(incident_data):
    print("\n[DEBUG] Creating incident in ServiceNow with data:", incident_data)
    simulated_response = {
        "sys_id": "simulated_sys_id_123",
        "number": "INC0000123",
        "short_description": incident_data["short_description"],
        "description": incident_data["description"],
        "category": incident_data["category"],
    }
    print("[DEBUG] Simulated ServiceNow API response:", simulated_response)
    return simulated_response

def load_knowledge_from_csv(filename):
    knowledge_data = []
    try:
        with open(filename, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                knowledge_data.append(row)
        print(f"[DEBUG] Loaded knowledge data from {filename}: {knowledge_data}")
        return knowledge_data
    except FileNotFoundError:
        print(f"[ERROR] File not found: {filename}. Returning empty knowledge base.")
        return []
    except Exception as e:
        print(f"[ERROR] An error occurred while reading {filename}: {e}. Returning empty knowledge base.")
        return []