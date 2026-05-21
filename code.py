import os
import fitz  # pymupdf - thư viện xử lý PDF mạnh mẽ
from itertools import combinations

# ============================================================
# CHƯƠNG TRÌNH GHÉP TRANG 1 CỦA 2 FILE PDF THÀNH 1 TRANG DUY NHẤT
# GHÉP TỰ ĐỘNG TẤT CẢ CẶP FOLDER (1-7 VÀ 8-14)
# ============================================================

# Định nghĩa đường dẫn của 14 folder
folders = {
    1: r"c:\Users\hieu.pv\Desktop\tien_xu_ly_1_7_Hieu\hieu\1.GRV",
    2: r"c:\Users\hieu.pv\Desktop\tien_xu_ly_1_7_Hieu\hieu\2. Bang ke",
    3: r"c:\Users\hieu.pv\Desktop\tien_xu_ly_1_7_Hieu\hieu\3. Hoa don",
    4: r"c:\Users\hieu.pv\Desktop\tien_xu_ly_1_7_Hieu\hieu\4. Don_thuoc",
    5: r"c:\Users\hieu.pv\Desktop\tien_xu_ly_1_7_Hieu\hieu\5. Chuan doan hinh anh",
    6: r"c:\Users\hieu.pv\Desktop\tien_xu_ly_1_7_Hieu\hieu\6. Lab test",
    7: r"c:\Users\hieu.pv\Desktop\tien_xu_ly_1_7_Hieu\hieu\7.Tom tat benh an",
    8: r"c:\Users\hieu.pv\Desktop\tien_xu_ly_1_7_Hieu\hieu\8. Claim form",
    9: r"c:\Users\hieu.pv\Desktop\tien_xu_ly_1_7_Hieu\hieu\9. Báo cáo y tế",
    10: r"c:\Users\hieu.pv\Desktop\tien_xu_ly_1_7_Hieu\hieu\10. Bản TT tai nạn",
    11: r"c:\Users\hieu.pv\Desktop\tien_xu_ly_1_7_Hieu\hieu\11. Thẻ BHYT",
    12: r"c:\Users\hieu.pv\Desktop\tien_xu_ly_1_7_Hieu\hieu\12. Giấy chứng nhận phẫu thuật",
    13: r"c:\Users\hieu.pv\Desktop\tien_xu_ly_1_7_Hieu\hieu\13. Biên lai, phiếu thu",
    14: r"c:\Users\hieu.pv\Desktop\tien_xu_ly_1_7_Hieu\hieu\14. Hóa đơn bán hàng"
}

# Định nghĩa folder kết quả chính
folder_output_base = r"c:\Users\hieu.pv\Desktop\tien_xu_ly_1_7_Hieu\hieu\trung_nhau"

# Tạo folder output nếu chưa tồn tại
os.makedirs(folder_output_base, exist_ok=True)

# ===== PHẦN 1: GHÉP FOLDER 1-7 =====
print("\n" + "="*60)
print("PHẦN 1: GHÉP FOLDER 1-7")
print("="*60)

# Tạo tất cả cặp folder (combinations) từ 7 folder đầu
folder_pairs_1_7 = list(combinations(range(1, 8), 2))

# Duyệt qua tất cả các cặp folder 1-7
for folder_idx_1, folder_idx_2 in folder_pairs_1_7:
    folder_1 = folders[folder_idx_1]
    folder_2 = folders[folder_idx_2]
    
    # Tạo folder kết quả cho cặp này: trung_nhau/1_2, trung_nhau/1_3, v.v
    folder_output = os.path.join(folder_output_base, f"{folder_idx_1}_{folder_idx_2}")
    os.makedirs(folder_output, exist_ok=True)
    
    print(f"\nĐang ghép: Folder {folder_idx_1} + Folder {folder_idx_2}")
    
    # Duyệt qua từng file PDF trong folder 1
    for file1 in os.listdir(folder_1):
        if not file1.endswith('.pdf') or file1.startswith('.'):
            continue
        
        # Kiểm tra xem file tương ứng có tồn tại trong folder 2 không
        file1_path = os.path.join(folder_1, file1)
        file2_path = os.path.join(folder_2, file1)
        
        if os.path.exists(file2_path):
            try:
                # Mở file PDF từ folder 1
                pdf1 = fitz.open(file1_path)
                # Lấy trang 1 (index 0 = trang 1)
                page1_img = pdf1[0].get_pixmap(matrix=fitz.Matrix(1, 1))
                
                # Mở file PDF từ folder 2
                pdf2 = fitz.open(file2_path)
                # Lấy trang 1 (index 0 = trang 1)
                page2_img = pdf2[0].get_pixmap(matrix=fitz.Matrix(1, 1))
                
                # Chuyển đổi pixmap thành PIL Image
                from PIL import Image
                import io
                
                # Tạo hình ảnh từ pixmap trang 1
                img1 = Image.frombytes("RGB", [page1_img.width, page1_img.height], page1_img.samples)
                
                # Tạo hình ảnh từ pixmap trang 2
                img2 = Image.frombytes("RGB", [page2_img.width, page2_img.height], page2_img.samples)
                
                # Tính toán kích thước trang ghép (2 trang cạnh nhau ngang)
                total_width = img1.width + img2.width
                max_height = max(img1.height, img2.height)
                
                # Tạo trang PDF mới với kích thước ghép
                merged_pdf = fitz.open()
                
                # Tạo trang mới với kích thước phù hợp
                new_page = merged_pdf.new_page(width=total_width, height=max_height)
                
                # Chuyển đổi hình ảnh PNG thành pixmap
                img1_bytes = io.BytesIO()
                img1.save(img1_bytes, format='PNG')
                img1_bytes.seek(0)
                pix1 = fitz.Pixmap(img1_bytes)
                
                img2_bytes = io.BytesIO()
                img2.save(img2_bytes, format='PNG')
                img2_bytes.seek(0)
                pix2 = fitz.Pixmap(img2_bytes)
                
                # Đặt hình ảnh 1 vào bên trái
                new_page.insert_image(fitz.Rect(0, 0, img1.width, img1.height), pixmap=pix1)
                
                # Đặt hình ảnh 2 vào bên phải
                new_page.insert_image(fitz.Rect(img1.width, 0, total_width, img2.height), pixmap=pix2)
                
                # Lưu file PDF vào folder output
                output_path = os.path.join(folder_output, file1)
                merged_pdf.save(output_path)
                merged_pdf.close()
                pdf1.close()
                pdf2.close()
                
                print(f"  ✓ Đã ghép: {file1}")
                
            except Exception as e:
                # In ra lỗi nếu có vấn đề
                print(f"  ✗ Lỗi khi ghép {file1}: {str(e)}")

# ===== PHẦN 2: GHÉP FOLDER 8-14 =====
print("\n" + "="*60)
print("PHẦN 2: GHÉP FOLDER 8-14")
print("="*60)

# Tạo tất cả cặp folder (combinations) từ 7 folder 8-14
folder_pairs_8_14 = list(combinations(range(8, 15), 2))

# Duyệt qua tất cả các cặp folder 8-14
for folder_idx_1, folder_idx_2 in folder_pairs_8_14:
    folder_1 = folders[folder_idx_1]
    folder_2 = folders[folder_idx_2]
    
    # Tạo subfolder cho cặp này: trung_nhau/8_9, trung_nhau/8_10, v.v
    folder_output = os.path.join(folder_output_base, f"{folder_idx_1}_{folder_idx_2}")
    os.makedirs(folder_output, exist_ok=True)
    
    print(f"\nĐang ghép: Folder {folder_idx_1} + Folder {folder_idx_2}")
    
    # Duyệt qua từng file PDF trong folder 1
    for file1 in os.listdir(folder_1):
        if not file1.endswith('.pdf') or file1.startswith('.'):
            continue
        
        # Kiểm tra xem file tương ứng có tồn tại trong folder 2 không
        file1_path = os.path.join(folder_1, file1)
        file2_path = os.path.join(folder_2, file1)
        
        if os.path.exists(file2_path):
            try:
                # Mở file PDF từ folder 1
                pdf1 = fitz.open(file1_path)
                # Lấy trang 1 (index 0 = trang 1)
                page1_img = pdf1[0].get_pixmap(matrix=fitz.Matrix(1, 1))
                
                # Mở file PDF từ folder 2
                pdf2 = fitz.open(file2_path)
                # Lấy trang 1 (index 0 = trang 1)
                page2_img = pdf2[0].get_pixmap(matrix=fitz.Matrix(1, 1))
                
                # Chuyển đổi pixmap thành PIL Image
                from PIL import Image
                import io
                
                # Tạo hình ảnh từ pixmap trang 1
                img1 = Image.frombytes("RGB", [page1_img.width, page1_img.height], page1_img.samples)
                
                # Tạo hình ảnh từ pixmap trang 2
                img2 = Image.frombytes("RGB", [page2_img.width, page2_img.height], page2_img.samples)
                
                # Tính toán kích thước trang ghép (2 trang cạnh nhau ngang)
                total_width = img1.width + img2.width
                max_height = max(img1.height, img2.height)
                
                # Tạo trang PDF mới với kích thước ghép
                merged_pdf = fitz.open()
                
                # Tạo trang mới với kích thước phù hợp
                new_page = merged_pdf.new_page(width=total_width, height=max_height)
                
                # Chuyển đổi hình ảnh PNG thành pixmap
                img1_bytes = io.BytesIO()
                img1.save(img1_bytes, format='PNG')
                img1_bytes.seek(0)
                pix1 = fitz.Pixmap(img1_bytes)
                
                img2_bytes = io.BytesIO()
                img2.save(img2_bytes, format='PNG')
                img2_bytes.seek(0)
                pix2 = fitz.Pixmap(img2_bytes)
                
                # Đặt hình ảnh 1 vào bên trái
                new_page.insert_image(fitz.Rect(0, 0, img1.width, img1.height), pixmap=pix1)
                
                # Đặt hình ảnh 2 vào bên phải
                new_page.insert_image(fitz.Rect(img1.width, 0, total_width, img2.height), pixmap=pix2)
                
                # Lưu file PDF vào folder output (subfolder)
                output_path = os.path.join(folder_output, file1)
                merged_pdf.save(output_path)
                merged_pdf.close()
                pdf1.close()
                pdf2.close()
                
                print(f"   Đã ghép: {file1}")
                
            except Exception as e:
                # In ra lỗi nếu có vấn đề
                print(f"  ✗ Lỗi khi ghép {file1}: {str(e)}")

print("\n" + "="*60)
print("Hoàn tất! Tất cả các cặp folder đã được ghép!")
print(f"Kết quả lưu ở: {folder_output_base}")
print("="*60)
