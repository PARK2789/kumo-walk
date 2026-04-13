import streamlit as st
import pandas as pd
# 1. 디자인 및 설정 (iOS 감성)
st.set_page_config(page_title="CEO 소통 산책", page_icon="🍏", layout="centered")
st.markdown("""
<style>
.stApp { background-color: #F2F2F7; }
.ios-card {
background-color: white;
padding: 20px;
border-radius: 18px;
box-shadow: 0 4px 10px rgba(0,0,0,0.05);
margin-bottom: 15px;
border: 0.5px solid #E5E5EA;
}
.stButton>button {
width: 100%; border-radius: 12px; background-color: #007AFF;
color: white; font-weight: 600; border: none; height: 3.5em;
}
</style>
""", unsafe_allow_status=True)
# 2. 메뉴 선택
page = st.sidebar.radio("Menu", ["🏠 행사 안내", "👥 조원 명단"])
# 3. 페이지 로직
if page == "🏠 행사 안내":
st.title("CEO 소통 산책")
st.markdown("### 금오산 올레길 코스 가이드")
# 상단 정보 카드
st.markdown('<div class="ios-card"><b>📅 일시:</b> 2026. 04. 20 (월) 14:00<br><b>📍 집결:</b> 금오산 잔디광장</div>', unsafe_allow_status=True)
# 지도 지점 표시
st.markdown("#### 🗺️ 미션 포인트")
map_data = pd.DataFrame({
'lat': [36.1083, 36.1105, 36.1130],
'lon': [128.3180, 128.3208, 128.3225]
})
st.map(map_data, zoom=14)
# 액티비티 상세
with st.expander("⚽ [미션 1] 배꼽마당 미니 골든벨"):
st.write("조원 합산 5회 골인 시 미션 성공!")
with st.expander("🎴 [미션 2] 뚝방길 하트평상 딱지치기"):
st.write("다른 조와 딱지치기 대결 (토너먼트)")
with st.expander("🍴 [식사] 느티나무 백숙"):
st.write("주소: 구미시 금오산상가길 89-12")
if st.button("카카오맵 실행"):
st.write("🔗 [길찾기](https://map.kakao.com/link/search/구미느티나무백숙)")
else:
st.title("👥 조원 명단")
group_info = {
"1조": ["박성식(조장)", "김대리", "이과장", "박사원"],
"2조": ["김본부", "이팀장", "최주임", "정사원"]
}
selected_group = st.selectbox("조 선택", list(group_info.keys()))
st.markdown(f'<div class="ios-card"><p style="color:#007AFF; font-weight:bold;">{selected_group} 멤버</p></div>', unsafe_allow_status=True)
for name in group_info[selected_group]:
st.write(f"👤 {name}")
# 푸터
st.caption("© 2026 LG Way Leadership Development")
