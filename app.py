import json
import os
import logging
from flask import Flask, render_template, request, abort, send_file, jsonify
import subprocess
import requests
import tempfile
import shutil
from utils.template_utils import get_template_from_json


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

cases_dir = os.path.join(BASE_DIR, "cases")
allowed_categories = [d for d in os.listdir(cases_dir) if os.path.isdir(os.path.join(cases_dir, d))]

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def execute_php_case(php_code, request_data=None):
    try:
        env = os.environ.copy()
        env['REQUEST_METHOD'] = request_data.get('method', 'GET') if request_data else 'GET'
        
        if request_data and 'params' in request_data:
            query_string = '&'.join([f"{k}={v}" for k, v in request_data['params'].items()])
            env['QUERY_STRING'] = query_string
            
            php_input = f"<?php\n"
            for key, value in request_data['params'].items():
                safe_key = json.dumps(str(key))[1:-1]
                safe_value = json.dumps(str(value))[1:-1]
                php_input += f"$_GET[{json.dumps(key)}] = {json.dumps(str(value))};\n"
            
            php_input += f"$_SERVER['QUERY_STRING'] = {json.dumps(query_string)};\n"
            php_input += f"$_SERVER['REQUEST_METHOD'] = {json.dumps(request_data.get('method', 'GET'))};\n"
            php_input += f"?>\n"
            
            php_input += php_code
        
        php_cmd = [
            'php', 
            '-d', 'disable_functions=exec,passthru,shell_exec,system,proc_open,popen,curl_exec,curl_multi_exec,parse_ini_file,show_source', 
            '-d', 'allow_url_fopen=Off',
            '-d', 'allow_url_include=Off',
            '-d', 'open_basedir=' + cases_dir,
            '-d', 'max_execution_time=10',
            '-d', 'memory_limit=64M'
        ]
        
        if request_data and 'params' in request_data:
            result = subprocess.run(
                php_cmd,
                input=php_input,
                env=env,
                capture_output=True,
                text=True,
                timeout=10,
                cwd=cases_dir
            )
        else:
            result = subprocess.run(
                php_cmd,
                input=php_code,
                env=env,
                capture_output=True,
                text=True,
                timeout=10,
                cwd=cases_dir
            )
        
        logging.info(f"PHP execution result - returncode: {result.returncode}")
        logging.info(f"PHP stdout: {result.stdout[:200]}...")
        if result.stderr:
            logging.info(f"PHP stderr: {result.stderr}")
        
        if result.returncode != 0:
            logging.error(f"PHP execution error: {result.stderr}")
            return f"<div class='error'>PHP execution error: {result.stderr}</div>"
        
        return result.stdout
        
    except subprocess.TimeoutExpired:
        logging.error("PHP execution timeout")
        return "<div class='error'>PHP execution timeout (10 seconds)</div>"
    except Exception as e:
        logging.error(f"PHP execution unexpected error: {str(e)}")
        return f"<div class='error'>PHP execution error: {str(e)}</div>"



@app.route("/")
def home():
    cases_json_path = os.path.join(BASE_DIR, "templates", "index_cases.json")
    with open(cases_json_path, "r", encoding="utf-8") as f:
        cases = json.load(f)
    risk_order = {"low": 0, "medium": 1, "high": 2}
    cases_with_empty = []
    for case in cases:
        case_dir = os.path.join(BASE_DIR, "cases", case["category"])
        if os.path.exists(case_dir):
            items = [f for f in os.listdir(case_dir) if f.endswith(".json")]
            is_empty = not bool(items)
            case_count = len(items)
        else:
            is_empty = True
            case_count = 0
        case_copy = dict(case)
        case_copy["is_empty"] = is_empty
        case_copy["case_count"] = case_count
        cases_with_empty.append(case_copy)
    cases_sorted = sorted(cases_with_empty, key=lambda c: risk_order.get(c["tag"].lower(), 99))
    return render_template("index.html", cases=cases_sorted)

@app.route("/style.css")
def style():
    return send_file(os.path.join(BASE_DIR, "src", "assets", "style.css"))

@app.route("/logo.png")
def logo():
    return send_file(os.path.join(BASE_DIR, "src", "logo.png"))

@app.route("/cases/<case_category>")
def case_category(case_category):
    try:
        if case_category not in allowed_categories:
            logging.error(f"Invalid category: {case_category}")
            abort(404)

        cases_json_path = os.path.join(BASE_DIR, "templates", "index_cases.json")
        with open(cases_json_path, "r", encoding="utf-8") as f:
            categories = json.load(f)
        
        category = next((c for c in categories if c["category"] == case_category), None)
        if not category:
            logging.error(f"Category not found: {case_category}")
            abort(404)

        case_dir = os.path.join(BASE_DIR, "cases", case_category)
        test_cases = []
        
        if not os.path.exists(case_dir):
            logging.error(f"Category directory not found: {case_dir}")
            abort(404)

        json_files = [f for f in os.listdir(case_dir) if f.endswith('.json')]
        for fname in json_files:
            fpath = os.path.join(case_dir, fname)
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    required_fields = ["title", "description", "category"]
                    data.setdefault("title", "Untitled")
                    data.setdefault("description", "No description available")
                    data.setdefault("category", case_category)
                    data.setdefault("difficulty", "Not specified")
                    data.setdefault("risk", "Not specified")
                    if all(field in data for field in required_fields):
                        data["slug"] = os.path.splitext(fname)[0]
                        test_cases.append(data)
                    else:
                        logging.warning(f"Missing fields: {fpath}")
            except json.JSONDecodeError as e:
                logging.error(f"JSON reading error {fpath}: {str(e)}")
                continue
            except Exception as e:
                logging.error(f"Unexpected error {fpath}: {str(e)}")
                continue

        if not test_cases:
            logging.warning(f"No test cases found in category: {case_category}")

        logging.info(f"Total {len(test_cases)} test cases found: {case_category}")
        if "details" not in category:
            category["details"] = {}
        
        category["details"]["test_cases"] = []
        for test_case in sorted(test_cases, key=lambda x: x.get("title", "")):
            case_details = {
                "title": test_case.get("title", "Untitled"),
                "desc": test_case.get("description", "No description available"),
                "slug": test_case.get("slug", ""),
                "difficulty": test_case.get("difficulty", ""),
                "risk": test_case.get("risk", "")
            }
            category["details"]["test_cases"].append(case_details)

        return render_template(
            "category_template.html",
            category=category
        )

    except Exception as e:
        logging.error(f"Error processing category: {str(e)}")
        abort(500)


@app.route("/cases/<case_category>/<sub_category>/", methods=["GET", "POST"])
def case(case_category, sub_category):
    logging.info(f"case_category: {case_category}, sub_category: {sub_category}")
    if case_category not in allowed_categories:
        abort(404)

    json_path = os.path.join(BASE_DIR, "cases", case_category, f"{sub_category}.json")
    
    if os.path.exists(json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            case_type = data.get("type", "html")
            
            if case_type == "php":
                php_code = data.get("php")
                if not php_code:
                    logging.error(f"PHP code not specified in PHP case: {json_path}")
                    abort(500)
                
                request_data = {
                    'method': request.method,
                    'params': dict(request.args) if request.args else {}
                }
                
                php_output = execute_php_case(php_code, request_data)
                
                data["body"] = php_output
                
                return render_template(
                    "template_pages/case_template.html",
                    **data
                )
            else:
                return render_template(
                    "template_pages/case_template.html",
                    **data
                )
                
        except Exception as e:
            logging.error(f"Template creation error: {str(e)}")
            abort(500)
    
    abort(404)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

