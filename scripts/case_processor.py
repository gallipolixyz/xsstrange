import json
from bs4 import BeautifulSoup
import sys
import os
import re
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def get_case_info(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    case_info = soup.find('div', class_='case-info')
    
    return {
        "title": case_info.find('h1').text if case_info and case_info.find('h1') else "",
        "difficulty": case_info.find('span', class_='difficulty').text if case_info and case_info.find('span', class_='difficulty') else "",
        "category": case_info.find('span', class_='category').text if case_info and case_info.find('span', class_='category') else "",
        "risk": case_info.find('span', class_='risk').text if case_info and case_info.find('span', class_='risk') else "",
        "description": case_info.find('div', class_='description').text if case_info and case_info.find('div', class_='description') else "",
        "hints": [li.text for li in case_info.find('div', class_='hints').find_all('li')] if case_info and case_info.find('div', class_='hints') else [],
        "objectives": [li.text for li in case_info.find('div', class_='objectives').find_all('li')] if case_info and case_info.find('div', class_='objectives') else []
    }

def html_to_json(html_file_path):
    try:
        with open(html_file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()

        soup = BeautifulSoup(html_content, 'html.parser')
        
        case_info = get_case_info(html_content)
        
        json_structure = {
            "title": case_info["title"],
            "description": case_info["description"],
            "objectives": case_info["objectives"],
            "hints": case_info["hints"],
            "difficulty": case_info["difficulty"],
            "category": case_info["category"],
            "risk": case_info["risk"],
            "status": "active",
            "body": str(soup.find('article')) if soup.find('article') else ""
        }

        return json_structure
    except Exception as e:
        logging.error(f"HTML to JSON conversion error: {str(e)}")
        return None

def update_index_cases(category, case_name):
    try:
        index_cases_path = 'templates/index_cases.json'
        if not os.path.exists(index_cases_path):
            logging.error(f"index_cases.json file not found: {index_cases_path}")
            return False

        try:
            with open(index_cases_path, 'r', encoding='utf-8') as f:
                index_cases = json.load(f)
        except json.JSONDecodeError as e:
            logging.error(f"index_cases.json file has invalid JSON format: {str(e)}")
            return False
        except Exception as e:
            logging.error(f"Error reading index_cases.json file: {str(e)}")
            return False
        
        category_found = False
        for case in index_cases:
            if case["category"] == category:
                category_found = True
                if "test_cases" not in case["details"]:
                    case["details"]["test_cases"] = []
                
                if case_name not in case["details"]["test_cases"]:
                    case["details"]["test_cases"].append(case_name)
                    logging.info(f"Test case added: {category} -> {case_name}")
                else:
                    logging.info(f"Test case already exists: {category} -> {case_name}")
                
                try:
                    with open(index_cases_path, 'w', encoding='utf-8') as f:
                        json.dump(index_cases, f, indent=2, ensure_ascii=False)
                    logging.info(f"index_cases.json updated: {category}")
                    return True
                except Exception as e:
                    logging.error(f"Error writing index_cases.json file: {str(e)}")
                    return False
        
        if not category_found:
            logging.error(f"Category not found: {category}")
            return False
        
        return False
    except Exception as e:
        logging.error(f"Error updating index_cases.json: {str(e)}")
        return False

def process_case(html_file_path):
    try:
        json_output = html_to_json(html_file_path)
        if not json_output:
            logging.error(f"HTML to JSON conversion failed: {html_file_path}")
            return False

        case_name = os.path.splitext(os.path.basename(html_file_path))[0]
        
        category = os.path.basename(os.path.dirname(html_file_path))
        logging.info(f"Category determined: {category}")

        output_file = os.path.join(os.path.dirname(html_file_path), f"{case_name}.json")
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(json_output, f, indent=2, ensure_ascii=False)
            
            if not os.path.exists(output_file):
                logging.error(f"JSON file could not be created: {output_file}")
                return False
                
            logging.info(f"JSON file created: {output_file}")
        except Exception as e:
            logging.error(f"Error creating JSON file: {str(e)}")
            return False
        
        if update_index_cases(category, case_name):
            logging.info(f"index_cases.json updated: {category} -> {case_name}")
            
            try:
                if os.path.exists(html_file_path):
                    os.remove(html_file_path)
                    logging.info(f"HTML file deleted: {html_file_path}")
                else:
                    logging.warning(f"HTML file to be deleted not found: {html_file_path}")
                return True
            except Exception as e:
                logging.error(f"Error deleting HTML file: {str(e)}")
                return False
        else:
            logging.error("index_cases.json could not be updated")
            return False
            
    except Exception as e:
        logging.error(f"Error processing case: {str(e)}")
        return False

def find_html_files(cases_dir):
    html_files = []
    for category_dir in os.listdir(cases_dir):
        category_path = os.path.join(cases_dir, category_dir)
        if os.path.isdir(category_path):
            for file in os.listdir(category_path):
                if file.endswith('.html'):
                    full_path = os.path.join(category_path, file)
                    html_files.append(full_path)
                    logging.info(f"HTML file found: {full_path}")
    return html_files

def main():
    try:
        cases_dir = 'cases'
        if not os.path.exists(cases_dir):
            logging.error(f"Directory not found: {cases_dir}")
            sys.exit(1)

        html_files = find_html_files(cases_dir)
        
        if not html_files:
            logging.warning("No HTML files to process found")
            sys.exit(0)

        success_count = 0
        for html_file in html_files:
            if process_case(html_file):
                success_count += 1

        logging.info(f"Process completed. Successful: {success_count}/{len(html_files)}")

    except Exception as e:
        logging.error(f"Program execution error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 