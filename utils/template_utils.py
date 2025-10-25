import os
import json
import logging
from flask import render_template

def get_template_from_json(base_dir, case_category, sub_category):
    try:
        json_path = os.path.join(base_dir, "templates", "cases", case_category, f"{sub_category}.json")
        
        if not os.path.exists(json_path):
            error_msg = f"JSON file not found: {json_path}"
            logging.error(error_msg)
            raise FileNotFoundError(error_msg)
        
        with open(json_path, 'r', encoding='utf-8') as f:
            case_data = json.load(f)
        
        try:
            case_info = case_data['layout']['caseInfo']
        except KeyError as e:
            error_msg = f"Required field not found in JSON data: {str(e)}"
            logging.error(error_msg)
            raise ValueError(error_msg)
        
        processed_js = case_data['layout']['processed_js']
        onload_js = processed_js.get('onload', '')
        functions_js = processed_js.get('functions', [])
        
        template = render_template(
            'template_pages/case_template.html',
            title=case_info['title'],
            difficulty=case_info['difficulty'],
            category=case_info['category'],
            risk=case_info['risk'],
            description=case_info['description'],
            hints=case_info['hints'],
            objectives=case_info['objectives'],
            
            head=case_data['layout']['head'],
            navigation=case_data['layout']['navigation'],
            body=case_data['layout']['body'],
            footer=case_data['layout']['footer'],
            
            onload_js=onload_js,
            functions_js=functions_js
        )
        
        return template
        
    except (FileNotFoundError, ValueError) as e:
        raise
    except Exception as e:
        error_msg = f"Error creating template: {str(e)}"
        logging.error(error_msg)
        raise Exception(error_msg) 