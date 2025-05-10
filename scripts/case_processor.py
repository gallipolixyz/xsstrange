import json
from bs4 import BeautifulSoup
import sys
import os
import re
import logging

# Logging ayarları
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
        # HTML dosyasını oku
        with open(html_file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # BeautifulSoup ile HTML'i parse et
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Case Info bölümünü al
        case_info = get_case_info(html_content)
        
        # JSON yapısını oluştur
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
        logging.error(f"HTML to JSON dönüşümünde hata: {str(e)}")
        return None

def update_index_cases(category, case_name):
    try:
        # index_cases.json dosyasını oku
        index_cases_path = 'templates/index_cases.json'
        if not os.path.exists(index_cases_path):
            logging.error(f"index_cases.json dosyası bulunamadı: {index_cases_path}")
            return False

        try:
            with open(index_cases_path, 'r', encoding='utf-8') as f:
                index_cases = json.load(f)
        except json.JSONDecodeError as e:
            logging.error(f"index_cases.json dosyası geçersiz JSON formatında: {str(e)}")
            return False
        except Exception as e:
            logging.error(f"index_cases.json dosyası okunurken hata: {str(e)}")
            return False
        
        # İlgili kategoriyi bul
        category_found = False
        for case in index_cases:
            if case["category"] == category:
                category_found = True
                # test_cases alanı yoksa oluştur
                if "test_cases" not in case["details"]:
                    case["details"]["test_cases"] = []
                
                # Case adını ekle (eğer yoksa)
                if case_name not in case["details"]["test_cases"]:
                    case["details"]["test_cases"].append(case_name)
                    logging.info(f"Test case eklendi: {category} -> {case_name}")
                else:
                    logging.info(f"Test case zaten mevcut: {category} -> {case_name}")
                
                # Değişiklikleri kaydet
                try:
                    with open(index_cases_path, 'w', encoding='utf-8') as f:
                        json.dump(index_cases, f, indent=2, ensure_ascii=False)
                    logging.info(f"index_cases.json güncellendi: {category}")
                    return True
                except Exception as e:
                    logging.error(f"index_cases.json dosyası yazılırken hata: {str(e)}")
                    return False
        
        if not category_found:
            logging.error(f"Kategori bulunamadı: {category}")
            return False
        
        return False
    except Exception as e:
        logging.error(f"index_cases.json güncellenirken hata: {str(e)}")
        return False

def process_case(html_file_path):
    try:
        # JSON dönüşümü
        json_output = html_to_json(html_file_path)
        if not json_output:
            logging.error(f"HTML to JSON dönüşümü başarısız: {html_file_path}")
            return False

        # Case adını al (uzantısız)
        case_name = os.path.splitext(os.path.basename(html_file_path))[0]
        
        # Kategori adını dosya yolundan al
        category = os.path.basename(os.path.dirname(html_file_path))
        logging.info(f"Kategori belirlendi: {category}")

        # JSON dosyasını kaydet (aynı dizinde)
        output_file = os.path.join(os.path.dirname(html_file_path), f"{case_name}.json")
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(json_output, f, indent=2, ensure_ascii=False)
            
            # JSON dosyasının oluşturulduğunu doğrula
            if not os.path.exists(output_file):
                logging.error(f"JSON dosyası oluşturulamadı: {output_file}")
                return False
                
            logging.info(f"JSON dosyası oluşturuldu: {output_file}")
        except Exception as e:
            logging.error(f"JSON dosyası oluşturulurken hata: {str(e)}")
            return False
        
        # index_cases.json'ı güncelle
        if update_index_cases(category, case_name):
            logging.info(f"index_cases.json güncellendi: {category} -> {case_name}")
            
            # JSON dosyası başarıyla oluşturulduktan sonra HTML dosyasını sil
            try:
                if os.path.exists(html_file_path):
                    os.remove(html_file_path)
                    logging.info(f"HTML dosyası silindi: {html_file_path}")
                else:
                    logging.warning(f"Silinecek HTML dosyası bulunamadı: {html_file_path}")
                return True
            except Exception as e:
                logging.error(f"HTML dosyası silinirken hata: {str(e)}")
                return False
        else:
            logging.error("index_cases.json güncellenemedi")
            return False
            
    except Exception as e:
        logging.error(f"Case işlenirken hata: {str(e)}")
        return False

def find_html_files(cases_dir):
    html_files = []
    # Sadece /cases altındaki klasörleri kontrol et
    for category_dir in os.listdir(cases_dir):
        category_path = os.path.join(cases_dir, category_dir)
        if os.path.isdir(category_path):
            # Kategori klasöründeki HTML dosyalarını bul
            for file in os.listdir(category_path):
                if file.endswith('.html'):
                    full_path = os.path.join(category_path, file)
                    html_files.append(full_path)
                    logging.info(f"HTML dosyası bulundu: {full_path}")
    return html_files

def main():
    try:
        cases_dir = 'cases'
        if not os.path.exists(cases_dir):
            logging.error(f"{cases_dir} dizini bulunamadı")
            sys.exit(1)

        # HTML dosyalarını bul
        html_files = find_html_files(cases_dir)
        
        if not html_files:
            logging.warning("İşlenecek HTML dosyası bulunamadı")
            sys.exit(0)

        # Her bir case'i işle
        success_count = 0
        for html_file in html_files:
            if process_case(html_file):
                success_count += 1

        logging.info(f"İşlem tamamlandı. Başarılı: {success_count}/{len(html_files)}")

    except Exception as e:
        logging.error(f"Program çalışırken hata: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 