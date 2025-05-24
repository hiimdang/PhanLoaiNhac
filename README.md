# PhanLoaiNhac
Đồ án môn Deep Learning

## Tổng quan
Phân loại thể loại nhạc dựa vào hai loại đặc trưng là lyrics và file âm thanh.

Với 4 nhãn:
- Hiphop  
- Nhạc trẻ  
- Trữ tình  
- Thiếu nhi

## Mô tả dữ liệu

Bộ dữ liệu bài hát được lưu trữ trong một file CSV, trong đó mỗi dòng gồm 3 thành phần chính:

- **Đường dẫn tới file âm thanh**: các file định dạng `.mp3` chứa bản nhạc tương ứng.
- **Lời bài hát (Lyrics)**: văn bản thuần túy mô tả nội dung lời bài hát.
- **Nhãn thể loại**: phân loại bài hát thuộc 1 trong 4 thể loại — Hiphop, Nhạc trẻ, Trữ tình hoặc Thiếu nhi.

### Thống kê
- Tổng số bài hát: 3,873  
- Phân bố thể loại:  
  - Hiphop: 663 bài  
  - Nhạc trẻ: 1567 bài  
  - Trữ tình: 1159 bài  
  - Thiếu nhi: 484 bài

### Nguồn dữ liệu
- Tự thu thập hoàn toàn từ trang [Zing MP3](https://zingmp3.vn)

---

## Quy trình thực hiện
1. Chuẩn bị bộ dữ liệu bao gồm lyrics và file âm thanh theo đúng định dạng đã mô tả 
2. Thực hiện bước tiền xử lý (preprocessing):
    - Xử lý âm thanh
        - Trích xuất MFCCs: Tính toán 20 hệ số MFCC từ mỗi đoạn âm thanh .mp3, giúp mô tả đặc điểm phổ tần của tín hiệu âm thanh.
        - Trích xuất Chroma features: Lấy 12 đặc trưng chroma biểu diễn cường độ của các nốt nhạc trong đoạn âm thanh.
        - Tính Mel-spectrogram: Chuyển đổi âm thanh sang dạng phổ Mel với 128 dải tần số, phản ánh cấu trúc tần số trong âm thanh.
    - Xử lý lời bài hát 
        - Làm sạch và chuẩn hóa văn bản lời bài hát(loại bỏ các từ vô nghĩa, chuyển lowercase, ký tự đặc biệt...).
        - Chuyển đổi lời bài hát thành vector đặc trưng bằng phương pháp TF-IDF với 100 từ phổ biến nhất được chọn làm vocabulary.
        - Mỗi lời bài hát được biểu diễn bằng vector TF-IDF 100 chiều, phản ánh mức độ quan trọng của từng từ trong bài.
    - Kết hợp dữ liệu
        - Ghép các đặc trưng âm thanh (MFCC, Chroma, Mel-spectrogram) và đặc trưng lời bài hát (TF-IDF) lại thành một vector đặc trưng tổng hợp cho mỗi bài hát.
        - Chuẩn hóa các đặc trưng trước khi đưa vào mô hình học sâu.
3. Huấn luyện mô hình Deep Learning.
4. Xây dựng app để nghe nhạc cũng như dự đoán thể loại nhạc dựa sử dụng mô hình đã huấn luyện

---
## Ý tưởng tương lai
- Thay vì phân loại thể loại nhạc thì sẽ tách các đặc trưng bài hát để tìm bài hát liên quan, ứng dụng cho gợi ý thêm bài nhạc tương tự vào playlist.

