# KẾ HOẠCH BÁO CÁO CHUYÊN ĐỀ: 21 THUẬT TOÁN ĐỐI SÁNH MẪU (STRING MATCHING)

> **Môn học:** Cấu trúc Dữ liệu và Giải thuật Nâng cao  
> **Tài liệu tham khảo chính:** *Handbook of Exact String-Matching Algorithms* (Christian Charras & Thierry Lecroq) — file `/Users/ductn/master-ptit/advance-algorithm/string.pdf` (220 trang).
> **Tài liệu tham khảo bổ sung:** Slide bài giảng gốc `/Users/ductn/master-ptit/advance-algorithm/Chuyende-Thuattoan.ppt`
> **Hình thức nộp:** File Word (`.docx`), làm **bản độc lập** (không làm nhóm), in ra bản cứng, nộp vào buổi thi cuối kỳ.  
> **File bìa mẫu:** `/Users/ductn/master-ptit/advance-algorithm/BiaTieuLuan.docx` (mẫu Học viện Công nghệ Bưu chính Viễn thông — Khoa Sau đại học).
> **File giao nộp cuối cùng:** `Thuật toán nâng cao/Tieu-luan-21-Thuat-toan-Doi-sanh-mau.docx`

> ⚠️ **QUY TẮC BẮT BUỘC — nguồn cho nội dung báo cáo:** File kế hoạch này (`.md`) là tài liệu làm việc **nội bộ**, được phép ghi chú chéo `Chuyende-Thuattoan.ppt`để tra cứu yêu cầu chấm điểm. Nhưng **nội dung báo cáo thật** (mọi file trong `bao-cao-21-thuat-toan/`) chỉ được phép trích dẫn/tham chiếu **duy nhất** `String matching.pdf` (Handbook) — **không được nhắc đến** slide, giảng viên, tên tác giả slide, hay bất kỳ tài liệu nào khác. Đây là báo cáo làm độc lập. Khi soạn nội dung các Phần tiếp theo (Ngày 3–5), luôn kiểm tra lại quy tắc này trước khi lưu file.

### 1. Mục tiêu và Yêu cầu
> **Yêu cầu gốc từ giảng viên**: *"Với 35 thuật toán trong string matching. Với mỗi chuyên đề, trình bày ít nhất 10–21 thuật toán, mỗi mục (nhóm) ít nhất 1 thuật toán, càng nhiều thì càng nhiều điểm. Làm bản độc lập, làm file docx rồi in ra bản cứng, nộp vào hôm thi."*

- **Số lượng thuật toán:** Báo cáo chi tiết **21 thuật toán** — chạm mức trần của khung 10–21 mà giảng viên đưa ra để tối đa hóa điểm (đề bài không giới hạn điểm ở mốc 20, nhưng 21 là số nhiều nhất được liệt kê nên chọn làm mục tiêu).
- **Độ phủ cấu trúc:** Đã phân loại và phân bổ đủ **4 nhóm thuật toán** không trùng lặp, mỗi nhóm có nhiều hơn 1 thuật toán (vượt yêu cầu tối thiểu "mỗi mục ít nhất 1 thuật toán"), theo đúng khung phân loại của Handbook và đối chiếu với slide bài giảng gốc.
- **Cấu trúc bắt buộc cho MỖI thuật toán trong 21 thuật toán:**
  1. **Trình bày thuật toán:** Ý tưởng chính, cơ chế hoạt động, bảng/sơ đồ mô phỏng từng bước trên dữ liệu mẫu chuẩn ($x = \text{GCAGAGAG}$, $y = \text{GCATCGCAGAGAGTATACAGTACG}$).
  2. **Đánh giá độ phức tạp:** Độ phức tạp thời gian (Trường hợp tốt nhất, Trung bình, Xấu nhất) và độ phức tạp bộ nhớ phụ trợ (Extra space).
  3. **Kiểm nghiệm thuật toán:** Đánh giá thực nghiệm số phép so sánh ký tự / kiểm tra trạng thái trên chuỗi thử nghiệm.
  4. **Lập trình theo thuật toán:** Mã nguồn C++ hoàn chỉnh, chuẩn hóa, có chú thích chi tiết.
- Dưới đây là danh sách 35 thuật toán theo yêu cầu của giảng viên, hãy dựa vào 2 tài liệu đã được trích dẫn. Hãy chọn ra 21 thuật toán phù hợp và thực hiện theo yêu cầu và lưu lại ra 1 file `draft.docx`.
```
1. Thuật toán Knuth-Morris-Partt
2. Thuật toán Karp-Rabin
3. Thuật toán Shift or
4. Thuật toán Morris-Partt
5. Thuật toán Automat hữu hạn
6. Thuật toán Simon
7. Thuật toán Colussi
8. Thuật toán Galil-Giancarlo
9. Apostolico-Crochemore algorithm
10. Not So Naive algorithm
11. Turbo BM algorithm 
12. Apostolico-Giancarlo algorithm
13. Reverse Colussi algorithm
14. Reverse Colussi algorithm
15. Horspool algorithm
16. Quick Search algorithm
17. Tuned Boyer-Moore algorithm
18. Zhu-Takaoka algorithm
19. Berry-Ravindran algorithm
20. Smith algorithm
21. Raita algorithm
22. Reverse Factor algorithm
23. Turbo Reverse Factor algorithm
24. Forward Dawg Matching algorithm
25. Backward Nondeterministic Dawg 2.38. Matching algorithm
26. Backward Oracle Matching algorithm
27 Galil-Seiferas algorithm
28. Two Way algorithm
29. String Matching on Ordered 
30. Alphabets algorithm
31. Optimal Mismatch algorithm
32. Maximal Shift algorithm
33. Skip Search algorithm
34. KMP Skip Search algorithm
35. Alpha Skip Search algorithm
```