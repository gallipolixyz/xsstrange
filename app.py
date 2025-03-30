import json
import os
import logging
from flask import Flask, render_template, request, abort, send_file


allowed_categories = ["xss"]
app = Flask(__name__)

# Dinamik sayfa yönlendirme
@app.route("/")
def home():
    return send_file("./src/index.html")

@app.route("/style.css")
def style():
    return send_file("./src/assets/style.css")

@app.route("/logo.png")
def logo():
    return send_file("./src/logo.png")

@app.route("/cases/<case_category>")
def case_category(case_category):

    if case_category.lower() not in allowed_categories:
        abort(404)

    file_path = f'./src/cases/{case_category}/index.html'

    if os.path.exists(file_path):
        return send_file(file_path)
    else:
        abort(404)

@app.route("/cases/<case_category>/<sub_category>/", methods=["GET"])
def case(case_category, sub_category):
    logging.info(f"case_category: {case_category}, sub_category: {sub_category}")
    if case_category not in allowed_categories:
        abort(404)

    # Sadece 'reflected' için özel bir işlem yapılıyor
    if case_category == "xss" and sub_category == "reflected":
        return get_template_from_json(case_category, sub_category)

    # Gelecekte başka alt kategoriler eklenirse buraya eklenebilir
    abort(404)

def get_template_from_json(category, template_name):
    # JSON file path
    json_file_path = f"./templates/{category}/{template_name}.json"
    try:
        # Load JSON data
        with open(json_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        logging.error(f"JSON file not found: {json_file_path}")
        abort(404)
    except json.JSONDecodeError:
        logging.error(f"Invalid JSON format in file: {json_file_path}")
        abort(404)

    # Get user input
    user_input = request.args.get("userInput", "")  # Default to an empty string
    logging.info(f"User input: {user_input}")

    # Render template with JSON data
    return render_template(
        "template_pages/template.html",
        layout=data.get("layout", {}),
        user_input=user_input,
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
