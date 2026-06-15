import requests
import json
import time
import io
import cairosvg
import pytesseract
from PIL import Image

def get_captcha(session):
    url = "https://diemthi10.bacninh.edu.vn/api/captcha"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }
    
    response = session.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data.get("errorCode") == 0:
            captcha_data = data.get("data", {})
            return captcha_data.get("uuid"), captcha_data.get("image")
    return None, None

import re
import ddddocr

# Tải model ddddocr 1 lần để tối ưu tốc độ
ocr_engine = ddddocr.DdddOcr(show_ad=False)

def solve_captcha(svg_content):
    try:
        # 0. Làm sạch nhiễu trong SVG: loại bỏ các đường kẻ có fill="none"
        clean_svg = re.sub(r'<path[^>]*fill="none"[^>]*>', '', svg_content)

        # 1. Chuyển SVG đã làm sạch sang định dạng PNG bytes bằng cairosvg
        png_data = cairosvg.svg2png(bytestring=clean_svg.encode('utf-8'))
        
        # 2. Sử dụng ddddocr (Model Deep Learning chuyên trị Captcha) để đọc trực tiếp từ bytes
        text = ocr_engine.classification(png_data)
        
        return text
    except Exception as e:
        print(f"[!] Lỗi giải mã Captcha: {e}")
        return ""

def lookup_score(session, sbd, uuid, captcha_text):
    url = "https://diemthi10.bacninh.edu.vn/api/lookup"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    payload = {
        "uuid": uuid,
        "captcha": captcha_text,
        "sbd": sbd
    }
    
    response = session.post(url, headers=headers, json=payload)
    try:
        return response.json()
    except:
        return None

def auto_lookup(sbd):
    session = requests.Session()
    max_retries = 20 # Số lần thử lại tối đa (nếu OCR đọc sai Captcha)
    
    print(f"\n[*] Đang tiến hành tra cứu tự động SBD: {sbd}...")
    
    for attempt in range(max_retries):
        uuid, image_svg = get_captcha(session)
        if not uuid:
            print("[!] Không lấy được Captcha, thử lại...")
            time.sleep(1)
            continue
            
        # Tự động giải mã Captcha
        captcha_text = solve_captcha(image_svg)
        if not captcha_text:
            continue
            
        print(f"    - Lần {attempt+1}/{max_retries}: Đã đoán Captcha là '{captcha_text}'. Đang gửi yêu cầu...")
        
        result = lookup_score(session, sbd, uuid, captcha_text)
        if result:
            if result.get("errorCode") == 0:
                print("\n[+] TÌM THẤY KẾT QUẢ THÀNH CÔNG!")
                diemthi = result.get("data", {}).get("diemthi", {})
                print(f"    Họ tên: {diemthi.get('FULLNAME')}")
                print(f"    Số báo danh: {diemthi.get('CODE')}")
                print(f"    Trường: {diemthi.get('TENTRUONG')}")
                print(f"    Tổng điểm đại trà: {diemthi.get('TONGDT')}")
                print(f"    Tổng toán: {diemthi.get('TONGTOAN')} | Ngữ Văn: {diemthi.get('NGUVAN')} | Tiếng Anh: {diemthi.get('TIENGANH')}")
                return diemthi
            else:
                msg = result.get("message", "")
                if "Captcha" in msg or "xác nhận" in msg.lower():
                    # Đọc sai Captcha, hệ thống sẽ tự thử vòng lặp tiếp theo
                    pass
                else:
                    print(f"\n[-] Lỗi từ hệ thống (có thể sai SBD): {msg}")
                    return False
        time.sleep(0.5)
        
    print("\n[-] Đã thử quá nhiều lần nhưng Captcha đều sai. Tỷ lệ nhiễu ảnh quá cao đối với OCR cơ bản.")
    return False

def main():
    sbd = input("Nhập số báo danh để tra cứu tự động: ")
    auto_lookup(sbd)

if __name__ == "__main__":
    main()
