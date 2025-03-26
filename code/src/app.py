from flask import Flask, render_template, jsonify, request
from utils.temp_id_name import find_similar_templates, refine_results
from utils.temp_id_incident1 import get_template_id
from utils.ServiceNowCreationDependingOnUserPrompt import create_servicenow_incident
import utils.chatbot as cb




app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/template_search/')
def template_search():
    name = request.args.get("name", "")  # Get name input from the form

    results = []
    if name:  # Only search if name is provided
        results = find_similar_templates(name, top_n=5)
        results = results.drop(columns=["embedding"]).to_dict(orient="records")  # Exclude embeddings

    return render_template('name_inp.html', name=name, results=results)


@app.route('/incident_template')
def get_incident_inp():
    return render_template('incident_inp.html')

@app.route('/template_id/<incident_no>')
def get_template_id_route(incident_no):
    template_id = get_template_id(incident_no)
    return render_template('template_search_incident.html', incident_no=incident_no, template_id=template_id)


@app.route('/create_incident', methods=['GET','POST'])
def quick_incident():
    if request.method == 'POST':
        data = request.get_json()
        user_prompt = data.get('user_prompt')  # Expect JSON input
        print(user_prompt)

        if user_prompt:
            result = create_servicenow_incident(user_prompt)
            print(result)
            return jsonify({"result": result})  # Return JSON response
        
        return jsonify({"error": "No user prompt provided"}), 400  # Bad Request
    
    return render_template('Snowcreator.html')  # Render page only for GET request
    


@app.route('/platformbuddy')
def home():
    return render_template('chatbot.html')  # Changed from 'index.html' to 'chatbot.html'

@app.route('/query', methods=['POST'])
def query():
    try:
        data = request.get_json()
        session_id = data.get("session_id")
        prompt = data.get("prompt")

        if not session_id or not prompt:
            return jsonify({"error": "Both 'session_id' and 'prompt' fields are required"}), 400

        response_text = cb.chat_with_aii(session_id, prompt)
        return jsonify({"response": response_text}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    #app.run(host="0.0.0.0", port=5000)
    app.run(debug=True)
