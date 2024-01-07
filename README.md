# Đồ án được viết bằng ngôn ngữ Python và JavaScript
- File "fe" chứa 
+  File node_modules là thư viện 
+ File public chứa index.html được tạo ra bởi create-react-app để bắt đầu phát triển một ứng dụng React. Và chứa file manifest.json mô tả thông tin về ứng dụng web và cung cấp dữ liệu cho trình duyệt và các nền tảng khác khi ứng dụng được cài đặt hoặc thêm vào màn hình chính.
+ File src chứa App.js xây dựng giao diện người dùng
- File "Recommandatinon" chứa
+ File dataset chứa 3 file là file "combined-data_1.txt" có ID phim: ID người dùng,hạng sao,ngày đánh giá, file probe.txt chứa các dòng biểu thị ID phim: ID khách hàng, file qualifying.txt chứa ID phim: ID khách hàng, ngày xếp hạng.
+ File a.csv và file movie_titles.csv là 1 vì dữ liệu quá lớn nên phải cắt ra thành 2 file, các file này chứa ID phim, năm sản xuất, tên bộ phim. Có tổng 17770 bộ phim.
+ File index.py triển khai một ứng dụng web sử dụng Flask để cung cấp dịch vụ đề xuất phim dựa trên thuật toán lọc cộng tác SVD (Singular Value Decomposition) tập dữ liệu nguồn từ: https://www.kaggle.com/code/laowingkin/netflix-movie-recommendation/notebook
## Hướng dẫn cách chạy đồ án 
- Bước 1: Vào link https://www.kaggle.com/code/laowingkin/netflix-movie-recommendation/input hãy download tập dữ liệu có tên "combined-data_1.txt" và tập dữ liệu "qualifying.txt" và lưu trong thư mục dataset
- Bước 2: Mở Terminal, chọn New Termianl, tiếp theo chọn Command Prompt
- Bước 3: Nhập lệnh 'cd fe' , tiếp theo nhập lệnh 'npm run start'
- Bước 4: Tiếp tục mở thêm 1 Command Prompt
- Bước 5: Nhập lệnh 'cd Recommandation', tiếp theo nhập lệnh 'python index.py'
 Sau khi làm xong 4 bước thì giao hiện sẽ tự động hiển thị trên trình duyệt.
### Nhập tên bộ phim để tìm kiếm
- 'X2: X-Men United' nhập tên bộ phim và nhấn nút tìm kiếm
- Dữ liệu sẽ được xử lý trong Terminal python.
- Lọc ra 10 bộ phim có độ tương quan cao nhất và hiển thị lên giao diện web.
