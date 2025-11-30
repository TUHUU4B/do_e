import math
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
import matplotlib
matplotlib.use('Agg')

# Cấu hình font để hiển thị tiếng Việt
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

st.set_page_config(
    page_title="Tính toán Mô đun Đàn hồi (E) hiện trường - 22 TCN 211-2006 - Phụ lục D",
    page_icon="📊",
    layout="wide",
)

# Hệ số Poisson theo loại vật liệu
POISSON_RATIOS = {
    "Đất nền": 0.35,
    "Vật liệu": 0.25,
    "Kết cấu áo đường": 0.30,
}



@st.cache_data
def format_number(value: float, digits: int = 2) -> str:
    """Format number using Vietnamese separators."""
    if math.isnan(value) or value is None:
        return "-"
    formatted = f"{value:,.{digits}f}"
    parts = formatted.split(".")
    if len(parts) == 2:
        integer_part = parts[0].replace(",", ".")
        decimal_part = parts[1]
        return f"{integer_part},{decimal_part}"
    return parts[0].replace(",", ".")


def calculate_elastic_modulus(
    pressure: float,
    diameter: float,
    poisson_ratio: float,
    deformation: float,
) -> float:
    """
    Tính Mô đun Đàn hồi (E) theo công thức 22 TCN 211-2006 Phụ lục D.
    
    Công thức: E = (π/4) × (p × D × (1 - µ²)) / l
    
    Trong đó:
    - E: Mô đun đàn hồi (MPa)
    - π: Hằng số Pi (≈ 3.14159)
    - p: Áp lực (MPa)
    - D: Đường kính tấm ép (cm, chuyển đổi sang mm)
    - µ: Hệ số Poisson
    - l: Biến dạng hồi phục (mm)
    """
    if deformation <= 0:
        return None
    
    # Chuyển đổi đường kính từ cm sang mm
    D_mm = diameter * 10
    
    # Tính E theo công thức với hệ số π/4
    E = (math.pi / 4) * (pressure * D_mm * (1 - poisson_ratio ** 2)) / deformation
    
    return E


def calculate_deformation(
    pressure: float,
    diameter: float,
    poisson_ratio: float,
    elastic_modulus: float,
) -> float:
    """
    Tính Biến dạng hồi phục (l) từ công thức ngược.
    
    Công thức: l = (p * D * (1 - µ²)) / E
    
    Trong đó:
    - l: Biến dạng hồi phục (mm)
    - p: Áp lực (MPa)
    - D: Đường kính tấm ép (cm, chuyển đổi sang mm)
    - µ: Hệ số Poisson
    - E: Mô đun đàn hồi (MPa)
    """
    if elastic_modulus <= 0:
        return None
    
    # Chuyển đổi đường kính từ cm sang mm
    D_mm = diameter * 10
    
    # Tính l theo công thức ngược
    l = (pressure * D_mm * (1 - poisson_ratio ** 2)) / elastic_modulus
    
    return l


def calculate_deformation_from_gauge(
    reading_after_load: float,
    reading_after_unload: float,
) -> float:
    """
    Tính Biến dạng hồi phục (l) từ số đọc đồng hồ.
    
    Công thức: l = [số đọc sau khi gia tải - số đọc sau khi xả tải] × 2 × 0,01
    
    Trong đó:
    - l: Biến dạng hồi phục (mm)
    - số đọc sau khi gia tải: số đọc đồng hồ sau khi gia tải (đơn vị: 0,01mm)
    - số đọc sau khi xả tải: số đọc đồng hồ sau khi xả tải (đơn vị: 0,01mm)
    """
    # Tính biến dạng hồi phục
    l = (reading_after_load - reading_after_unload) * 2 * 0.01
    
    return l


def evaluate_elastic_modulus(E_value: float, E_required: float = None) -> dict:
    """
    Đánh giá giá trị Mô đun Đàn hồi và so sánh với giá trị yêu cầu.
    """
    if E_value is None:
        return {
            "status": "Không xác định",
            "details": "Không thể tính toán Mô đun Đàn hồi từ dữ liệu hiện có.",
            "comparison": None
        }
    
    comparison = None
    if E_required is not None and E_required > 0:
        ratio = (E_value / E_required) * 100
        if E_value >= E_required:
            comparison_status = "✅ Đạt yêu cầu"
            comparison_details = f"Mô đun đàn hồi đo được ({format_number(E_value, 2)} MPa) lớn hơn hoặc bằng mô đun đàn hồi yêu cầu ({format_number(E_required, 2)} MPa). Đạt {format_number(ratio, 1)}% so với yêu cầu."
        else:
            comparison_status = "❌ Không đạt yêu cầu"
            comparison_details = f"Mô đun đàn hồi đo được ({format_number(E_value, 2)} MPa) nhỏ hơn mô đun đàn hồi yêu cầu ({format_number(E_required, 2)} MPa). Chỉ đạt {format_number(ratio, 1)}% so với yêu cầu. Cần kiểm tra lại vật liệu hoặc phương án thiết kế."
        
        comparison = {
            "status": comparison_status,
            "details": comparison_details,
            "ratio": ratio,
            "E_measured": E_value,
            "E_required": E_required
        }
    
    # Đánh giá chung
    if E_required is not None and E_required > 0:
        if E_value >= E_required:
            status = "Đạt yêu cầu"
            details = f"Mô đun đàn hồi đo được đáp ứng yêu cầu thiết kế ({format_number(E_required, 2)} MPa)."
        else:
            status = "Không đạt yêu cầu"
            details = f"Mô đun đàn hồi đo được không đáp ứng yêu cầu thiết kế ({format_number(E_required, 2)} MPa)."
    else:
        # Đánh giá theo giá trị tuyệt đối nếu không có E_yc
        if E_value < 50:
            status = "Thấp"
            details = "Mô đun đàn hồi ở mức thấp. Cần kiểm tra lại vật liệu hoặc phương án thiết kế."
        elif E_value < 200:
            status = "Trung bình"
            details = "Mô đun đàn hồi ở mức trung bình. Vật liệu có thể sử dụng được."
        else:
            status = "Tốt"
            details = "Mô đun đàn hồi ở mức tốt. Vật liệu đáp ứng yêu cầu thiết kế."
    
    return {
        "status": status,
        "details": details,
        "value": E_value,
        "comparison": comparison
    }


def main() -> None:
    st.title("Tính toán Mô đun Đàn hồi (E) - 22 TCN 211-2006")
    st.caption(
        "Phương pháp xác định mô đun đàn hồi của đất và vật liệu áo đường "
        "tại hiện trường hoặc tại máng thí nghiệm theo 22 TCN 211-2006 - Phụ lục D."
    )

    with st.sidebar:
        try:
            st.image("logo.png", use_container_width=True)
        except FileNotFoundError:
            st.warning("Không tìm thấy file logo.png")

        st.markdown(
            "<div style='text-align: center; margin-top: 10px; margin-bottom: 10px;'>"
            "<h4>CÔNG TY TỨ HỮU</h4>"
            "<p style='font-size: 0.9em; color: #666;'>Tác giả: MR Tuấn - 0946135156</p>"
            "</div>",
            unsafe_allow_html=True,
        )
        st.divider()

        st.header("Hướng dẫn nhanh")
        st.markdown(
            "- Chọn loại vật liệu/đất nền cần đo.\n"
            "- Nhập đường kính tấm ép (30-76 cm).\n"
            "- Nhập áp lực và biến dạng hồi phục.\n"
            "- Nhập biến dạng từ số đọc đồng hồ hoặc nhập trực tiếp.\n"
            "- Công thức: l = [số đọc gia tải - số đọc xả tải] × 2 × 0,01\n"
            "- Công thức tính E: E = (π/4) × (p × D × (1 - µ²)) / l\n"
            "- Nhập Mô đun Đàn hồi yêu cầu để so sánh."
        )

    # Chọn loại vật liệu
    st.subheader("1. Chọn loại vật liệu/đất nền")
    material_type = st.selectbox(
        "Loại vật liệu",
        options=list(POISSON_RATIOS.keys()),
        index=0,
        help="Hệ số Poisson sẽ được tự động chọn theo loại vật liệu"
    )
    
    poisson_ratio = POISSON_RATIOS[material_type]
    st.info(f"**Hệ số Poisson (µ):** {poisson_ratio}")

    # Nhập đường kính tấm ép
    st.subheader("2. Thông số tấm ép")
    diameter = st.number_input(
        "Đường kính tấm ép (cm)",
        min_value=30.0,
        max_value=76.0,
        value=76.0,
        step=1.0,
        help="Đường kính tấm ép từ 30 cm đến 76 cm (khuyến nghị dùng 76 cm)"
    )
    st.info(f"**Đường kính tấm ép:** {format_number(diameter, 0)} cm")

    # Nhập kết quả thí nghiệm
    st.subheader("3. Nhập kết quả thí nghiệm")
    
    # Nhập áp lực
    pressure = st.number_input(
        "Áp lực p (MPa)",
        min_value=0.0,
        value=0.5,
        step=0.01,
        format="%.3f",
        help="Áp lực tác dụng lên tấm ép"
    )
    
    # Chọn cách nhập biến dạng
    deformation_input_mode = st.radio(
        "Cách nhập biến dạng hồi phục",
        options=["Nhập từ số đọc đồng hồ", "Nhập trực tiếp biến dạng (mm)"],
        index=0,
        horizontal=True
    )
    
    reading_after_load = None
    reading_after_unload = None
    
    if deformation_input_mode == "Nhập từ số đọc đồng hồ":
        col1, col2 = st.columns(2)
        
        with col1:
            reading_after_load = st.number_input(
                "Số đọc sau khi gia tải (0,01mm)",
                min_value=0.0,
                value=100.0,
                step=0.1,
                format="%.2f",
                help="Số đọc đồng hồ sau khi gia tải (đơn vị: 0,01mm)"
            )
        
        with col2:
            reading_after_unload = st.number_input(
                "Số đọc sau khi xả tải (0,01mm)",
                min_value=0.0,
                value=50.0,
                step=0.1,
                format="%.2f",
                help="Số đọc đồng hồ sau khi xả tải (đơn vị: 0,01mm)"
            )
        
        # Tính biến dạng từ số đọc
        if reading_after_load is not None and reading_after_unload is not None:
            deformation = calculate_deformation_from_gauge(reading_after_load, reading_after_unload)
            if deformation is not None:
                st.info(f"**Biến dạng hồi phục tính được: l = {format_number(deformation, 3)} mm**")
                st.caption(f"Công thức: l = ({format_number(reading_after_load, 2)} - {format_number(reading_after_unload, 2)}) × 2 × 0,01 = {format_number(deformation, 3)} mm")
        else:
            deformation = None
    else:
        deformation = st.number_input(
            "Biến dạng hồi phục l (mm)",
            min_value=0.0,
            value=1.0,
            step=0.01,
            format="%.3f",
            help="Biến dạng hồi phục đo được trực tiếp (mm)"
        )
    
    # Nhập Mô đun Đàn hồi yêu cầu
    st.markdown("**Mô đun Đàn hồi yêu cầu (E_yc):**")
    E_required = st.number_input(
        "E_yc (MPa)",
        min_value=0.0,
        value=None,
        step=1.0,
        format="%.2f",
        help="Nhập Mô đun Đàn hồi yêu cầu để so sánh (có thể để trống)",
        key="E_required_simple"
    )

    # Tính toán
    if st.button("🔢 Tính toán Mô đun Đàn hồi", type="primary"):
        if deformation is not None and deformation > 0:
            E = calculate_elastic_modulus(pressure, diameter, poisson_ratio, deformation)
            
            if E is not None:
                st.success(f"**Mô đun Đàn hồi E = {format_number(E, 2)} MPa**")
                
                # Hiển thị chi tiết tính toán
                with st.expander("📊 Xem chi tiết tính toán", expanded=True):
                    detail_text = f"""
                    **Công thức:** E = (π/4) × (p × D × (1 - µ²)) / l
                    """
                    
                    # Thêm thông tin về cách tính biến dạng nếu nhập từ số đọc
                    if deformation_input_mode == "Nhập từ số đọc đồng hồ":
                        detail_text += f"""
                        
                        **Tính biến dạng hồi phục từ số đọc đồng hồ:**
                        - Số đọc sau khi gia tải = {format_number(reading_after_load, 2)} (0,01mm)
                        - Số đọc sau khi xả tải = {format_number(reading_after_unload, 2)} (0,01mm)
                        - l = ({format_number(reading_after_load, 2)} - {format_number(reading_after_unload, 2)}) × 2 × 0,01 = {format_number(deformation, 3)} mm
                        """
                    
                    detail_text += f"""
                    
                    **Thay số vào công thức tính E:**
                    - π = {format_number(math.pi, 6)}
                    - p = {format_number(pressure, 3)} MPa
                    - D = {format_number(diameter, 2)} cm = {format_number(diameter * 10, 2)} mm
                    - µ = {poisson_ratio}
                    - l = {format_number(deformation, 3)} mm
                    
                    **Tính toán:**
                    - (1 - µ²) = (1 - {poisson_ratio}²) = {format_number(1 - poisson_ratio**2, 4)}
                    - π/4 = {format_number(math.pi / 4, 6)}
                    - E = (π/4) × ({format_number(pressure, 3)} × {format_number(diameter * 10, 2)} × {format_number(1 - poisson_ratio**2, 4)}) / {format_number(deformation, 3)}
                    - **E = {format_number(E, 2)} MPa**
                    """
                    
                    st.markdown(detail_text)
                
                # Đánh giá và so sánh
                eval_result = evaluate_elastic_modulus(E, E_required if E_required and E_required > 0 else None)
                st.subheader("4. Đánh giá kết quả")
                
                if eval_result['comparison']:
                    st.markdown(f"**So sánh với Mô đun Đàn hồi yêu cầu:**")
                    st.markdown(f"**{eval_result['comparison']['status']}**")
                    st.info(eval_result['comparison']['details'])
                    
                    # Hiển thị bảng so sánh
                    comparison_df = pd.DataFrame({
                        "Chỉ tiêu": ["Mô đun Đàn hồi đo được (E)", "Mô đun Đàn hồi yêu cầu (E_yc)", "Tỷ lệ đạt (%)"],
                        "Giá trị": [
                            f"{format_number(E, 2)} MPa",
                            f"{format_number(E_required, 2)} MPa",
                            f"{format_number(eval_result['comparison']['ratio'], 1)}%"
                        ]
                    })
                    st.dataframe(comparison_df, use_container_width=True, hide_index=True)
                else:
                    status_color = {
                        "Tốt": "✅",
                        "Trung bình": "⚠️",
                        "Thấp": "❌",
                        "Đạt yêu cầu": "✅",
                        "Không đạt yêu cầu": "❌",
                        "Không xác định": "❓"
                    }
                    st.markdown(f"**Đánh giá:** {status_color.get(eval_result['status'], '')} {eval_result['status']}")
                    st.info(eval_result['details'])
        else:
            st.error("Biến dạng hồi phục phải lớn hơn 0!")

    # Thông tin bổ sung
    st.divider()
    st.subheader("📋 Thông tin bổ sung")
    with st.expander("ℹ️ Công thức và các đại lượng", expanded=False):
        st.markdown("""
        **Công thức tính Mô đun Đàn hồi (E):**
        
        E = (π/4) × (p × D × (1 - µ²)) / l
        
        **Công thức tính Biến dạng hồi phục (l) từ số đọc đồng hồ:**
        
        l = [số đọc sau khi gia tải - số đọc sau khi xả tải] × 2 × 0,01
        
        **Trong đó:**
        - **E**: Mô đun đàn hồi (MPa)
        - **π**: Hằng số Pi (≈ 3.14159)
        - **p**: Tải trọng cấp nén (áp lực) tác dụng lên tấm ép (MPa)
        - **D**: Đường kính tấm ép (cm, chuyển đổi sang mm trong tính toán)
        - **µ**: Hệ số Poisson
          - 0,35 đối với đất nền
          - 0,25 đối với vật liệu
          - 0,30 đối với cả kết cấu áo đường
        - **l**: Biến dạng hồi phục đo được trong thực nghiệm tương ứng với cấp tải trọng p (mm)
        - **số đọc sau khi gia tải**: Số đọc đồng hồ sau khi gia tải (đơn vị: 0,01mm)
        - **số đọc sau khi xả tải**: Số đọc đồng hồ sau khi xả tải (đơn vị: 0,01mm)
        """)
    
    with st.expander("🔧 Quy trình thí nghiệm", expanded=False):
        st.markdown("""
        **Bước Gia tải Chuẩn bị:**
        - Gia tải đến tải trọng p lớn nhất, giữ tải 2 phút
        - Sau đó dỡ tải và chờ biến dạng hồi phục hết
        
        **Bước Thử nghiệm Chính thức:**
        - Thực hiện gia tải với 3-4 cấp cho đến tải trọng p là cấp cuối cùng
        - Mỗi cấp: Gia tải, đợi biến dạng ổn định (tốc độ ≤ 0,02 mm/phút)
        - Sau đó: Dỡ tải, đợi biến dạng hồi phục ổn định (tốc độ ≤ 0,02 mm/phút)
        - Ghi số đọc ở chuyển vị kế để tính biến dạng hồi phục l tương ứng với các tải trọng
        """)

    st.caption(
        "**Ghi chú:**\n"
        "- Tính toán theo tiêu chuẩn 22 TCN 211-2006 - Phụ lục D.\n"
        "- Phương pháp xác định mô đun đàn hồi bằng thí nghiệm đo ép trên tấm ép lớn.\n"
        "- Đường kính tấm ép: cho phép từ 30 cm đến 76 cm, khuyến nghị dùng 76 cm nếu có điều kiện."
    )


if __name__ == "__main__":
    main()
