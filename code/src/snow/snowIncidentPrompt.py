# =============================================================================
# Configuration (Conceptual)
# =============================================================================
import requests

# ServiceNow API endpoint (replace with your instance URL)
SERVICENOW_API_URL = "https://your_instance.service-now.com/api/now/table/incident"
# ServiceNow API credentials (replace with a dedicated service account)
SERVICENOW_USER = "api_user"
SERVICENOW_PASSWORD = "api_password"
# Gemini API key (replace with your actual Gemini API key)
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
# Gemini model to use
GEMINI_MODEL = "gemini-pro"  # Or "gemini-pro-vision" if you're including images

# =============================================================================
# Libraries (Conceptual)
# =============================================================================

# In a real ServiceNow server-side script, you'd use global objects like:
# - sn_ws.RESTMessageV2 (for making REST API calls)
# - GlideRecord (for database operations)
# - gs (for logging)
#
# For this pseudocode, we'll assume these exist.  In a Python
# implementation, you'd use the requests library.
# import requests  # Python equivalent

# =============================================================================
# Helper Functions (Conceptual)
# =============================================================================

def call_gemini_api(prompt, model=GEMINI_MODEL):
    """
    Sends a prompt to the Gemini API and returns the response.

    Args:
        prompt (str): The text prompt to send to Gemini.
        model (str): The Gemini model to use (e.g., "gemini-pro").

    Returns:
        dict: The JSON response from the Gemini API, or None on error.
    """
    # Construct the Gemini API endpoint URL
    gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

    # Prepare the request payload
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
    }
    headers = {"Content-Type": "application/json"}
    params = {"key": GEMINI_API_KEY}

    try:
        # Make the API call (replace with sn_ws.RESTMessageV2 in ServiceNow)
        response = requests.post(gemini_url, json=payload, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes

        # Simulate a successful response, replace with actual parsing
        response_json = {
            "candidates": [
                {
                    "content": {
                        "parts": [
                            {
                                "text": "Simulated Gemini response: Intent: Report network problem.  CI: laptop123. Location: Conference Room A. Urgency: High.  Impact: High.  Summary: Laptop network issue in Conference Room A."
                            }
                        ]
                    }
                }
            ]
        }
        return response_json  #  response.json()

    except Exception as e:
        # Log the error (use gs.error in ServiceNow)
        print(f"Error calling Gemini API: {e}")
        return None

def create_incident_in_servicenow(incident_data):
    """
    Creates a new incident in ServiceNow using the provided data.

    Args:
        incident_data (dict): A dictionary containing the incident data
            (short_description, description, ci, category, etc.).
    Returns:
        str: The sys_id of the created incident, or None on error.
    """
    # Construct the ServiceNow API request payload

    payload = {
        "short_description": incident_data.get("short_description", ""),
        "description": incident_data.get("description", ""),
        "cmdb_ci": incident_data.get("ci", ""),  # Corrected key name
        "category": incident_data.get("category", ""),
        "subcategory": incident_data.get("subcategory", ""),
        "urgency": incident_data.get("urgency", ""),
        "impact": incident_data.get("impact", ""),
        "caller_id": incident_data.get("caller_id", ""), # Added caller_id
        "assignment_group": incident_data.get("assignment_group", "")
    }

    try:
        # Make the ServiceNow API call (replace with sn_ws.RESTMessageV2 in ServiceNow)
        response = requests.post(
            SERVICENOW_API_URL,
            json=payload,
            auth=(SERVICENOW_USER, SERVICENOW_PASSWORD),
            headers={"Content-Type": "application/json", "Accept": "application/json"},
        )
        response.raise_for_status()
        response_json = response.json()

        # Simulate a successful response. Replace with actual parsing.
        response_json = {
            "result": {
                "sys_id": "simulated_sys_id_12345",
                "number": "INC0012345"
            }
        }

        if response_json and response_json.get("result") and response_json["result"].get("sys_id"):
            return response_json["result"]["sys_id"] # Return sys_id
        else:
            print(f"Error: Unexpected response from ServiceNow: {response_json}")
            return None

    except Exception as e:
        # Log the error (use gs.error in ServiceNow)
        print(f"Error creating incident in ServiceNow: {e}")
        return None

def process_incident_request(user_input, caller_id):
    """
    Processes a user's natural language input to create an incident in ServiceNow
    using Gemini.

    Args:
        user_input (str): The user's natural language description of the incident.
        caller_id (str): The sys_id of the user in ServiceNow.

    Returns:
        str: The sys_id of the created incident, or None on error.
    """
    # 1. Call the Gemini API to analyze the user input
    gemini_response = call_gemini_api(user_input)

    if gemini_response is None:
        print("Failed to get a valid response from Gemini.")
        return None

    # 2. Extract relevant information from the Gemini response
    #    (This is where you'd parse the structured output from Gemini)
    try:
        gemini_output = gemini_response["candidates"][0]["content"]["parts"][0]["text"]
        print(f"Gemini Output: {gemini_output}") # Debug
        # Parse the Gemini output (this is a simplified example)
        #  Use more robust parsing logic here, potentially with regular expressions
        #  or by asking Gemini to return JSON.
        intent = gemini_output.split("Intent: ")[1].split(".")[0].strip()
        ci = gemini_output.split("CI: ")[1].split(".")[0].strip()
        location = gemini_output.split("Location: ")[1].split(".")[0].strip()
        urgency = gemini_output.split("Urgency: ")[1].split(".")[0].strip()
        impact = gemini_output.split("Impact: ")[1].split(".")[0].strip()
        short_description = gemini_output.split("Summary: ")[1].strip()

        incident_data = {
            "short_description": short_description,
            "description": user_input,  # Use the original user input
            "ci": ci,  #  Populate with the sys_id if found.
            "category": "Problem",  #  Map from intent
            "subcategory": intent, # map from intent
            "urgency": urgency,  # Map from Gemini output
            "impact": impact,    # Map from Gemini output
            "caller_id": caller_id,
            "assignment_group": "IT Service Desk",  #  Use a mapping table
        }
    except (KeyError, IndexError) as e:
        print(f"Error parsing Gemini output: {e}.  Gemini Response: {gemini_response}")
        return None

    # 3. Create the incident in ServiceNow
    incident_sys_id = create_incident_in_servicenow(incident_data)
    if incident_sys_id:
        print(f"Successfully created incident: {incident_sys_id}")
        return incident_sys_id
    else:
        print("Failed to create incident in ServiceNow.")
        return None

# =============================================================================
# ServiceNow Script (Conceptual)
# =============================================================================

# This is the entry point for the ServiceNow server-side script (e.g., a
# Business Rule or a Scripted REST API endpoint).
def on_before_insert(current): # 'current' is a GlideRecord object
    """
    ServiceNow Business Rule:
    - Runs "before" a new incident is inserted.
    - Assumes the user has provided a description in the 'description' field.
    - Calls process_incident_request to use Gemini to populate other fields.
    """

    user_input = current.description
    caller_id = current.caller_id.sys_id # Get the sys_id of the caller

    if not user_input:
        # Log an error and abort.  The user must provide a description.
        # gs.error("Incident description is required.")
        current.setAbortAction(True)
        print("Incident description is required.") #  Simulate abort
        return  #  Important:  Exit the function!

    # Process the incident request using Gemini
    incident_sys_id = process_incident_request(user_input, caller_id)

    if incident_sys_id:
        #  Fetch the newly created incident
        from GlideRecord import GlideRecord
        new_incident = GlideRecord("incident")
        if new_incident.get(incident_sys_id):
            # Update the current incident with the values from the newly created one.
            current.short_description = new_incident.short_description
            current.category = new_incident.category
            current.subcategory = new_incident.subcategory
            current.urgency = new_incident.urgency
            current.impact = new_incident.impact
            current.cmdb_ci = new_incident.cmdb_ci
            current.assignment_group = new_incident.assignment_group
            # gs.info(f"Incident fields populated by Gemini.  New Incident sys_id: {incident_sys_id}")
            print(f"Incident fields populated by Gemini.  New Incident sys_id: {incident_sys_id}")
        else:
            print(f"Could not retrieve new incident with sys_id: {incident_sys_id}")
    else:
        # Log an error;  process_incident_request() should already log.
        # gs.error("Failed to create incident via Gemini.")
        #  Consider whether to abort the current insert, or allow it with partial data
        # current.setAbortAction(true); #  <--  Uncomment to prevent creation.
        print("Failed to create incident via Gemini.")
        pass #  Allow incident to be created with what the user provided.

# =============================================================================
# Example Usage (Conceptual)
# =============================================================================

if __name__ == "__main__":
    # Simulate a user submitting an incident request
    user_input = "My computer monitor is flickering and then goes black.  I've tried restarting it, but it didn't help.  I need this fixed ASAP."
    caller_id = "user_sys_id_123" #  Replace with a valid sys_id
    created_incident_id = process_incident_request(user_input, caller_id)

    if created_incident_id:
        print(f"Incident created successfully with sys_id: {created_incident_id}")
    else:
        print("Failed to create incident.")