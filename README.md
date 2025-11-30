# Tính toán Mô đun Đàn hồi (E) – 22 TCN 211-2006

Ứng dụng Streamlit giúp kỹ sư tính toán và đánh giá Mô đun Đàn hồi (E) của đất và vật liệu áo đường theo tiêu chuẩn **22 TCN 211-2006 – Phụ lục D**. Ứng dụng cho phép:

- Tính toán Mô đun Đàn hồi (E) từ kết quả thí nghiệm ép tấm lớn.
- Tính toán Biến dạng hồi phục (l) từ các thông số đã biết.
- So sánh Mô đun Đàn hồi đo được với Mô đun Đàn hồi yêu cầu (E_yc).
- Hỗ trợ tính toán đơn giản (1 cấp tải) hoặc nhiều cấp tải (3-4 cấp).
- Vẽ biểu đồ quan hệ giữa Áp lực - Biến dạng và Áp lực - Mô đun Đàn hồi.
- Đánh giá tự động kết quả và so sánh với yêu cầu thiết kế.
- Hiển thị chi tiết quá trình tính toán theo công thức tiêu chuẩn.
- Tải biểu đồ kết quả dưới dạng PNG.

## Tiêu chuẩn tham khảo

- **22 TCN 211-2006**: Quy trình thiết kế áo đường mềm – Phụ lục D: Phương pháp thử nghiệm xác định mô đun đàn hồi của đất và vật liệu áo đường tại hiện trường hoặc tại máng thí nghiệm.

## Công thức tính toán

### Tính Mô đun Đàn hồi (E):
```
E = (p × D × (1 - µ²)) / l
```

### Tính Biến dạng hồi phục (l):
```
l = (p × D × (1 - µ²)) / E
```

**Trong đó:**
- **E**: Mô đun đàn hồi (MPa)
- **p**: Áp lực tác dụng lên tấm ép (MPa)
- **D**: Đường kính tấm ép (cm, chuyển đổi sang mm trong tính toán)
- **µ**: Hệ số Poisson
  - 0,35 đối với đất nền
  - 0,25 đối với vật liệu
  - 0,30 đối với cả kết cấu áo đường
- **l**: Biến dạng hồi phục đo được (mm)

## Yêu cầu hệ thống

- Python 3.10+
- Các thư viện trong `requirements.txt`:
  - streamlit >= 1.31.0
  - pandas >= 2.1.0
  - matplotlib >= 3.7.0
  - numpy >= 1.24.0

## Cài đặt

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

## Chạy ứng dụng

```bash
streamlit run app.py
```

Ứng dụng sẽ mở trên trình duyệt tại địa chỉ `http://localhost:8501`.

## Các hàm tính toán chính

- `format_number()`: Chuẩn hóa cách hiển thị số theo định dạng Việt Nam.
- `calculate_elastic_modulus()`: Tính Mô đun Đàn hồi (E) theo công thức 22 TCN 211-2006.
- `calculate_deformation()`: Tính Biến dạng hồi phục (l) từ công thức ngược.
- `evaluate_elastic_modulus()`: Đánh giá và so sánh Mô đun Đàn hồi với giá trị yêu cầu.
- `create_deformation_chart()`: Vẽ biểu đồ quan hệ Áp lực - Biến dạng và Áp lực - Mô đun Đàn hồi.

## Cách sử dụng ứng dụng

### 1. Chọn loại vật liệu/đất nền
Chọn một trong ba loại:
- **Đất nền** (µ = 0,35)
- **Vật liệu** (µ = 0,25)
- **Kết cấu áo đường** (µ = 0,30)

Hệ số Poisson sẽ được tự động chọn theo loại vật liệu.

### 2. Nhập thông số tấm ép
Nhập đường kính tấm ép từ **30 cm đến 76 cm** (khuyến nghị dùng 76 cm nếu có điều kiện).

### 3. Nhập kết quả thí nghiệm

#### Chế độ tính toán đơn giản (1 cấp tải):
- **Tính Mô đun Đàn hồi (E)**:**
  - Nhập áp lực p (MPa) và biến dạng hồi phục l (mm)
  - Nhập Mô đun Đàn hồi yêu cầu (E_yc) để so sánh (tùy chọn)
  - Ứng dụng sẽ tính E và so sánh với E_yc nếu có

- **Tính Biến dạng hồi phục (l)**:**
  - Nhập áp lực p (MPa) và Mô đun Đàn hồi E (MPa)
  - Ứng dụng sẽ tính biến dạng hồi phục l

#### Chế độ nhiều cấp tải:
- Nhập số cấp tải (thường 3-4 cấp)
- Nhập áp lực và biến dạng hồi phục cho từng cấp
- Nhập Mô đun Đàn hồi yêu cầu (E_yc) để so sánh (tùy chọn)
- Ứng dụng sẽ:
  - Tính Mô đun Đàn hồi cho từng cấp
  - Tính giá trị trung bình
  - So sánh với E_yc
  - Vẽ biểu đồ quan hệ

### 4. Xem kết quả
- **Chi tiết tính toán**: Xem công thức và các bước tính toán
- **Bảng kết quả**: Hiển thị kết quả cho từng cấp tải (nếu nhiều cấp)
- **So sánh với yêu cầu**: 
  - Hiển thị kết quả "Đạt yêu cầu" hoặc "Không đạt yêu cầu"
  - Tỷ lệ đạt (%)
  - Bảng so sánh chi tiết
- **Biểu đồ**: Quan hệ giữa Áp lực - Biến dạng và Áp lực - Mô đun Đàn hồi
- **Tải biểu đồ**: Tải biểu đồ dưới dạng PNG

## Quy trình thí nghiệm (Tham khảo)

### Bước Gia tải Chuẩn bị:
- Gia tải đến tải trọng p lớn nhất, giữ tải 2 phút
- Sau đó dỡ tải và chờ biến dạng hồi phục hết

### Bước Thử nghiệm Chính thức:
- Thực hiện gia tải với 3-4 cấp cho đến tải trọng p là cấp cuối cùng
- Mỗi cấp: Gia tải, đợi biến dạng ổn định (tốc độ ≤ 0,02 mm/phút)
- Sau đó: Dỡ tải, đợi biến dạng hồi phục ổn định (tốc độ ≤ 0,02 mm/phút)
- Ghi số đọc ở chuyển vị kế để tính biến dạng hồi phục l tương ứng với các tải trọng

## Tùy biến

- Thay logo bằng cách cập nhật `logo.png` trong thư mục gốc.
- Điều chỉnh ngưỡng đánh giá trong hàm `evaluate_elastic_modulus()` tùy theo yêu cầu dự án.

## Góp ý

Liên hệ: **MR Tuấn – 0946 135 156** (Công ty Tứ Hữu).
