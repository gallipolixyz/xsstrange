import os
import json
import logging
from flask import render_template

def get_template_from_json(base_dir, case_category, sub_category):
    """
    JSON dosyasından template oluşturur
    
    Args:
        base_dir (str): Uygulama kök dizini
        case_category (str): Case kategorisi
        sub_category (str): Alt kategori
        
    Returns:
        str: Oluşturulan HTML template
        
    Raises:
        FileNotFoundError: JSON dosyası bulunamazsa
        ValueError: JSON verisi geçersizse
        Exception: Diğer hatalar
    """
    try:
        # JSON dosyasının yolunu oluştur
        json_path = os.path.join(base_dir, "templates", "cases", case_category, f"{sub_category}.json")
        
        # JSON dosyası var mı kontrol et
        if not os.path.exists(json_path):
            error_msg = f"JSON dosyası bulunamadı: {json_path}"
            logging.error(error_msg)
            raise FileNotFoundError(error_msg)
        
        # JSON dosyasını oku
        with open(json_path, 'r', encoding='utf-8') as f:
            case_data = json.load(f)
        
        # Case bilgilerini al
        try:
            case_info = case_data['layout']['caseInfo']
        except KeyError as e:
            error_msg = f"JSON verisinde gerekli alan bulunamadı: {str(e)}"
            logging.error(error_msg)
            raise ValueError(error_msg)
        
        # JavaScript kodlarını hazırla
        processed_js = case_data['layout']['processed_js']
        onload_js = processed_js.get('onload', '')
        functions_js = processed_js.get('functions', [])
        
        # Template'i oluştur
        template = render_template(
            'template_pages/case_template.html',
            # Case bilgileri
            title=case_info['title'],
            difficulty=case_info['difficulty'],
            category=case_info['category'],
            risk=case_info['risk'],
            description=case_info['description'],
            hints=case_info['hints'],
            objectives=case_info['objectives'],
            
            # Sayfa yapısı
            head=case_data['layout']['head'],
            navigation=case_data['layout']['navigation'],
            body=case_data['layout']['body'],
            footer=case_data['layout']['footer'],
            
            # JavaScript
            onload_js=onload_js,
            functions_js=functions_js
        )
        
        return template
        
    except (FileNotFoundError, ValueError) as e:
        # Bu hataları tekrar fırlat
        raise
    except Exception as e:
        error_msg = f"Template oluşturulurken hata: {str(e)}"
        logging.error(error_msg)
        raise Exception(error_msg) 