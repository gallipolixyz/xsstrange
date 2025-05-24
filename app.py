import json
import os
import logging
from flask import Flask, render_template, request, abort, send_file, jsonify
import subprocess
import requests
from utils.template_utils import get_template_from_json


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Get allowed categories from cases directory
cases_dir = os.path.join(BASE_DIR, "cases")
allowed_categories = [d for d in os.listdir(cases_dir) if os.path.isdir(os.path.join(cases_dir, d))]

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


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
            items = os.listdir(case_dir)
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
        # Kategori kontrolü
        if case_category not in allowed_categories:
            logging.error(f"Geçersiz kategori: {case_category}")
            abort(404)

        # index_cases.json'dan kategori bilgilerini al
        cases_json_path = os.path.join(BASE_DIR, "templates", "index_cases.json")
        with open(cases_json_path, "r", encoding="utf-8") as f:
            categories = json.load(f)
        
        category = next((c for c in categories if c["category"] == case_category), None)
        if not category:
            logging.error(f"Kategori bulunamadı: {case_category}")
            abort(404)

        # Test case'leri oku
        case_dir = os.path.join(BASE_DIR, "cases", case_category)
        test_cases = []
        
        if not os.path.exists(case_dir):
            logging.error(f"Kategori dizini bulunamadı: {case_dir}")
            abort(404)

        json_files = [f for f in os.listdir(case_dir) if f.endswith('.json')]
        for fname in json_files:
            fpath = os.path.join(case_dir, fname)
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # Temel alanların varlığını kontrol et
                    required_fields = ["title", "description", "category"]
                    # Eğer alanlar eksikse varsayılan değerler ata
                    data.setdefault("title", "Untitled")
                    data.setdefault("description", "No description available")
                    data.setdefault("category", case_category)
                    data.setdefault("difficulty", "Not specified")
                    data.setdefault("risk", "Not specified")
                    if all(field in data for field in required_fields):
                        data["slug"] = os.path.splitext(fname)[0]
                        test_cases.append(data)
                    else:
                        logging.warning(f"Eksik alanlar var: {fpath}")
            except json.JSONDecodeError as e:
                logging.error(f"JSON okuma hatası {fpath}: {str(e)}")
                continue
            except Exception as e:
                logging.error(f"Beklenmeyen hata {fpath}: {str(e)}")
                continue

        if not test_cases:
            logging.warning(f"Kategoride test case bulunamadı: {case_category}")

        logging.info(f"Toplam {len(test_cases)} test case bulundu: {case_category}")
            # Kategori detaylarını güncelle
        if "details" not in category:
            category["details"] = {}
        
        # Test case'leri kategori detaylarına ekle
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
        logging.error(f"Kategori işlenirken hata: {str(e)}")
        abort(500)


@app.route("/cases/<case_category>/<sub_category>/", methods=["GET"])
def case(case_category, sub_category):
    logging.info(f"case_category: {case_category}, sub_category: {sub_category}")
    if case_category not in allowed_categories:
        abort(404)

    json_path = os.path.join(BASE_DIR, "cases", case_category, f"{sub_category}.json")
    
    if os.path.exists(json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return render_template(
                "template_pages/case_template.html",
                **data
            )
        except Exception as e:
            logging.error(f"Template oluşturma hatası: {str(e)}")
            abort(500)
    
    abort(404)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
