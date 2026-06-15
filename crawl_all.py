import csv
import time
import diemthi_bacninh_auto
import os

def main():
    sbds = []
    try:
        with open('danh_sach_sbd.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader) # Bỏ qua dòng tiêu đề
            for row in reader:
                if row:
                    sbds.append(row[0])
    except FileNotFoundError:
        print("Không tìm thấy file danh_sach_sbd.csv. Bạn cần chạy extract_sbd.py trước.")
        return
            
    print(f"Bắt đầu thu thập dữ liệu cho {len(sbds)} thí sinh...")
    
    output_file = 'ket_qua_diemthi.csv'
    is_new_file = not os.path.exists(output_file) or os.path.getsize(output_file) == 0
    
    with open(output_file, 'a', newline='', encoding='utf-8') as f:
        fieldnames = ['SBD', 'FULLNAME', 'BIRTHDATE', 'GIOIT', 'TENTRUONG', 
                      'NGUVAN', 'TIENGANH', 'TOANTRN', 'TOANTULUAN', 'TONGTOAN', 
                      'TONGDT', 'MONCHUYEN', 'DIEMCHUYEN']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        if is_new_file:
            writer.writeheader()
            
        for i, sbd in enumerate(sbds):
            print(f"\n--- Tiến độ: Thí sinh {i+1}/{len(sbds)} ---")
            diemthi = diemthi_bacninh_auto.auto_lookup(sbd)
            if diemthi and isinstance(diemthi, dict):
                row = {
                    'SBD': diemthi.get('CODE', sbd),
                    'FULLNAME': diemthi.get('FULLNAME', ''),
                    'BIRTHDATE': diemthi.get('BIRTHDATE', ''),
                    'GIOIT': diemthi.get('GIOIT', ''),
                    'TENTRUONG': diemthi.get('TENTRUONG', ''),
                    'NGUVAN': diemthi.get('NGUVAN', ''),
                    'TIENGANH': diemthi.get('TIENGANH', ''),
                    'TOANTRN': diemthi.get('TOANTRN', ''),
                    'TOANTULUAN': diemthi.get('TOANTULUAN', ''),
                    'TONGTOAN': diemthi.get('TONGTOAN', ''),
                    'TONGDT': diemthi.get('TONGDT', ''),
                    'MONCHUYEN': diemthi.get('MONCHUYEN', ''),
                    'DIEMCHUYEN': diemthi.get('DIEMCHUYEN', '')
                }
                writer.writerow(row)
                f.flush() # Ghi trực tiếp xuống đĩa ngay lập tức
            else:
                print(f"[!] Bỏ qua SBD {sbd} do lỗi hoặc không tìm thấy.")
                
    print(f"\nĐã hoàn thành! Toàn bộ kết quả được lưu tại: {output_file}")

if __name__ == '__main__':
    main()
