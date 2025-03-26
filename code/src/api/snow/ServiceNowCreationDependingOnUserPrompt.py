import json
import csv
from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

def create_servicenow_incident(user_prompt, knowledge_data):
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

    enriched_prompt = f"{user_prompt}.  Here is related information from past incidents: "
    return enriched_prompt



def generate_ai_response(enriched_prompt, knowledge_data):
    print("\n[DEBUG] Calling simulated Gen AI with prompt:", enriched_prompt)

    relevant_incidents = []
    for incident in knowledge_data:
        if incident['Description'].lower() in enriched_prompt.lower() or incident['Category'].lower() in enriched_prompt.lower():
            relevant_incidents.append(incident)

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

    else:
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
        "short_description": incident_data["short_description"], # Added for more realistic simulation
        "description": incident_data["description"],
        "category": incident_data["category"],

    }
    print("[DEBUG] Simulated ServiceNow API response:", simulated_response)
    return simulated_response



@app.route('/create_incident', methods=['POST'])
def create_incident_api():
    try:
        data = request.get_json()
        user_prompt = data.get('user_prompt')

        if not user_prompt:
            return jsonify({'error': 'Missing user_prompt in the request'}), 400

        knowledge_data = load_knowledge_from_csv('synthetic_servicenow_incidents_cleaned.csv')

        print(f"\n[USER INPUT] User Prompt: {user_prompt}")
        new_incident = create_servicenow_incident(user_prompt, knowledge_data)

        if new_incident:
            print(f"\n[SUCCESS] Created incident in ServiceNow:")
            return jsonify({'result': new_incident}), 201  # 201 Created status
        else:
            return jsonify({'error': 'Failed to create incident'}), 500  # 500 Internal Server Error

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        print(f"[ERROR] {error_message}")
        return jsonify({'error': error_message}), 500


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
        print(f"[ERROR] File not found: {filename}.  Returning empty knowledge base.")
        return []
    except Exception as e:
        print(f"[ERROR] An error occurred while reading {filename}: {e}.  Returning empty knowledge base.")
        return []



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
