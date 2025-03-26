from flask import Flask, render_template, jsonify
from utils.temp_id_name import find_similar_templates, refine_results
from utils.temp_id_incident1 import get_template_id

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/template_search/<name>')
def template_search(name):
    results = find_similar_templates(name,top_n=5)
    return results.to_json(orient="records")


@app.route('/template_id/<incident_no>')
def get_template_id_route(incident_no):
    template_id = get_template_id(incident_no)

    if template_id is None:
        return jsonify({"error": "Incident not found"}), 404  # Return JSON with a 404 status
    
    return jsonify({"template_id": int(template_id)})  # Return JSON response


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
