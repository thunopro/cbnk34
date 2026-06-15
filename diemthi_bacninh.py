import requests
import json
import os

def get_captcha(session):
    print("Đang lấy Captcha...")
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
            uuid = captcha_data.get("uuid")
            image_svg = captcha_data.get("image")
            
            # Lưu SVG ra file để xem
            with open("captcha.svg", "w", encoding="utf-8") as f:
                f.write(image_svg)
                
            print("Đã lưu mã Captcha vào file 'captcha.svg'. Vui lòng mở file này bằng trình duyệt để xem mã.")
            return uuid
        else:
            print(f"Lỗi API Captcha: {data.get('message')}")
    else:
        print(f"Lỗi HTTP: {response.status_code}")
    
    return None

def lookup_score(session, sbd, uuid, captcha_text):
    url = "https://diemthi10.bacninh.edu.vn/api/lookup"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    payload = {
        "uuid": uuid,
        "captcha": captcha_text,
        "sbd": sbd
    }
    
    response = session.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        if data.get("errorCode") == 0:
            diemthi = data.get("data", {}).get("diemthi", {})
            print("\n=== KẾT QUẢ TRA CỨU ===")
            print(f"Họ tên: {diemthi.get('FULLNAME')}")
            print(f"Số báo danh: {diemthi.get('CODE')}")
            print(f"Ngày sinh: {diemthi.get('BIRTHDATE')} | Giới tính: {diemthi.get('GIOIT')}")
            print(f"Trường: {diemthi.get('TENTRUONG')}")
            print("--- Điểm đại trà ---")
            print(f"Ngữ Văn: {diemthi.get('NGUVAN')}")
            print(f"Tiếng Anh: {diemthi.get('TIENGANH')}")
            print(f"Toán (Trắc nghiệm): {diemthi.get('TOANTRN')}")
            print(f"Toán (Tự luận): {diemthi.get('TOANTULUAN')}")
            print(f"Tổng toán: {diemthi.get('TONGTOAN')}")
            print(f"Tổng đại trà: {diemthi.get('TONGDT')}")
            
            if diemthi.get('MONCHUYEN'):
                print("--- Điểm chuyên ---")
                print(f"Môn chuyên: {diemthi.get('MONCHUYEN')}")
                print(f"Điểm chuyên: {diemthi.get('DIEMCHUYEN')}")
        else:
            print(f"\nLỗi tra cứu: {data.get('message', 'Không tìm thấy kết quả hoặc sai Captcha.')}")
    else:
        print(f"Lỗi HTTP: {response.status_code}")

def main():
    session = requests.Session()
    
    sbd = input("Nhập số báo danh cần tra cứu: ")
    
    uuid = get_captcha(session)
    if uuid:
        captcha_text = input("Nhập mã Captcha (xem trong file captcha.svg): ")
        lookup_score(session, sbd, uuid, captcha_text)

if __name__ == "__main__":
    main()
