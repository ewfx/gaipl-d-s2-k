from flask import Flask, render_template, jsonify, request
from utils.temp_id_name import find_similar_templates, refine_results
from utils.temp_id_incident1 import get_template_id

app = Flask(__name__)


# @app.route('/template_search/<name>')
# def template_search(name):
#     results = find_similar_templates(name,top_n=5)
#     return results.to_json(orient="records")

# @app.route('/name_template')
# def get_incident_inp():
#     return render_template('name_inp.html')


# @app.route('/template_search/<name>')
# def template_search(name):
#     results = find_similar_templates(name, top_n=5)

#     # Convert DataFrame to a list of dictionaries, excluding embeddings
#     results = results.drop(columns=["embedding"]).to_dict(orient="records")

#     return render_template('name_inp.html', name=name, results=results)

@app.route('/template_search/')
def template_search():
    name = request.args.get("name", "")  # Get name input from the form

    results = []
    if name:  # Only search if name is provided
        results = find_similar_templates(name, top_n=5)
        results = results.drop(columns=["embedding"]).to_dict(orient="records")  # Exclude embeddings

    return render_template('name_inp.html', name=name, results=results)

# @app.route('/template_id/<incident_no>')
# def get_template_id_route(incident_no):
#     template_id = get_template_id(incident_no)

#     if template_id is None:
#         return jsonify({"error": "Incident not found"}), 404  # Return JSON with a 404 status
    
#     return jsonify({"template_id": int(template_id)})  # Return JSON response

@app.route('/incident_template')
def get_incident_inp():
    return render_template('incident_inp.html')

@app.route('/template_id/<incident_no>')
def get_template_id_route(incident_no):
    template_id = get_template_id(incident_no)
    return render_template('template_search_incident.html', incident_no=incident_no, template_id=template_id)


if __name__ == '__main__':
    # app.run(host="0.0.0.0", port=5000)
    app.run(debug=True)
