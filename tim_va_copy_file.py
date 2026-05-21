

import os
import shutil
from pathlib import Path

# Đường dẫn các thư mục cần xử lý
# Thư mục chứa các file PDF cần tìm gốc
lab_test_folder = r"C:\Users\hieu.pv\Desktop\tien_xu_ly_1_7_Hieu\giong\6. Lab test"

# Các thư mục nguồn gốc cần tìm kiếm
source_folders = [
    r"C:\Users\hieu.pv\Desktop\tien_xu_ly_1_7_Hieu\giong\Hoso",
    r"C:\Users\hieu.pv\Desktop\tien_xu_ly_1_7_Hieu\giong\HSYCBT"
]

# Thư mục đích để lưu các file gốc
destination_folder = r"C:\Users\hieu.pv\Desktop\tien_xu_ly_1_7_Hieu\giong\Labtest_goc"

# Tạo thư mục đích nếu nó chưa tồn tại
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)
    print(f" Tạo thư mục: {destination_folder}")

# Bước 1: Lấy danh sách tên file trong thư mục 6. Lab test
print(f"\n--- BẮT ĐẦU QUÉT THƯMỤC 6. Lab test ---")
if not os.path.exists(lab_test_folder):
    print(f" Thư mục {lab_test_folder} không tồn tại!")
    exit()

lab_test_files = os.listdir(lab_test_folder)
print(f"Tìm thấy {len(lab_test_files)} file trong 6. Lab test")

# Bước 2: Duyệt qua từng file trong 6. Lab test
files_copied = 0
files_not_found = 0

for file_name in lab_test_files:
    # Bỏ qua nếu là thư mục
    lab_test_file_path = os.path.join(lab_test_folder, file_name)
    if os.path.isdir(lab_test_file_path):
        continue
    
    print(f"\n→ Tìm kiếm file: {file_name}")
    file_found = False
    
    # Bước 3: Tìm kiếm file có cùng tên trong các thư mục nguồn
    for source_folder in source_folders:
        if not os.path.exists(source_folder):
            print(f"   Thư mục {source_folder} không tồn tại, bỏ qua")
            continue
        
        # Tìm kiếm đệ quy (bao gồm các thư mục con)
        for root, dirs, files in os.walk(source_folder):
            if file_name in files:
                source_file_path = os.path.join(root, file_name)
                destination_file_path = os.path.join(destination_folder, file_name)
                
                # Nếu file đã tồn tại trong thư mục đích, không copy lại
                if os.path.exists(destination_file_path):
                    print(f" File đã tồn tại trong Labtest_goc, bỏ qua")
                else:
                    # Copy file từ thư mục nguồn vào thư mục đích
                    try:
                        shutil.copy2(source_file_path, destination_file_path)
                        print(f"   Copy từ: {source_folder}")
                        files_copied += 1
                        file_found = True
                    except Exception as e:
                        print(f"   Lỗi khi copy file: {str(e)}")
    
    # Nếu không tìm thấy file trong cả hai thư mục nguồn
    if not file_found:
        print(f" Không tìm thấy file gốc")
        files_not_found += 1

# Bước 4: Hiển thị kết quả cuối cùng
print(f"\n--- KẾT QUẢ ---")
print(f" Tổng file copy: {files_copied}")
print(f" Tổng file không tìm thấy: {files_not_found}")
print(f" Các file gốc đã được lưu vào: {destination_folder}")
