import pandas as pd
import json
import os

def build_data():
    csv_file = 'ket_qua_diemthi.csv'
    if not os.path.exists(csv_file):
        print(f"File {csv_file} không tồn tại!")
        return

    # Đọc CSV, ép kiểu DIEMCHUYEN về số thực
    df = pd.read_csv(csv_file)
    
    # Lọc bỏ những dòng không có môn chuyên hoặc điểm chuyên
    df = df.dropna(subset=['MONCHUYEN', 'DIEMCHUYEN'])
    
    # Chuyển đổi DIEMCHUYEN sang float để sort chính xác
    df['DIEMCHUYEN'] = pd.to_numeric(df['DIEMCHUYEN'], errors='coerce')
    df = df.dropna(subset=['DIEMCHUYEN'])
    
    # Chuyển đổi TONGDT sang float
    df['TONGDT'] = pd.to_numeric(df['TONGDT'], errors='coerce').fillna(0)
    
    # Tính điểm xét tuyển chuyên (Tổng đại trà + Điểm chuyên * 2) - có thể dùng hoặc không
    df['TONGDX'] = df['TONGDT'] + df['DIEMCHUYEN'] * 2
    
    # Làm tròn điểm
    df['TONGDX'] = df['TONGDX'].round(2)
    
    # Nhóm theo môn chuyên
    subjects = df['MONCHUYEN'].unique()
    data = {}
    
    for subject in subjects:
        # Lọc theo môn
        sub_df = df[df['MONCHUYEN'] == subject]
        # Sort theo Điểm chuyên giảm dần, nếu bằng thì xét Tổng điểm xét tuyển giảm dần
        sub_df = sub_df.sort_values(by=['DIEMCHUYEN', 'TONGDX'], ascending=[False, False])
        
        # Thêm thứ hạng (Rank)
        sub_df['RANK'] = range(1, len(sub_df) + 1)
        
        # Chọn các cột cần thiết và chuyển thành dictionary
        records = sub_df[['RANK', 'SBD', 'FULLNAME', 'TENTRUONG', 'DIEMCHUYEN', 'TONGDT', 'TONGDX', 'NGUVAN', 'TIENGANH', 'TONGTOAN']].to_dict('records')
        data[subject] = records
        
    # Ghi ra JSON
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    print("Đã tạo file data.json thành công!")

if __name__ == '__main__':
    build_data()
