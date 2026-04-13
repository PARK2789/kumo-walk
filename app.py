import streamlit as st
import pandas as pd
# 1. 페이지 설정 및 디자인 커스텀 (iOS 스타일)
st.set_page_config(page_title="CEO 소통산책", page_icon="🍏", layout="centered")
st.markdown("""
<style>
/* 전체 배경색 */
.stApp { background-color: #F2F2F7; }
/* 카드 스타일 UI */
.ios-card {
background-color: white;
padding: 20px;
border-radius: 20px;
box-shadow: 0 4px 15px rgba(0,0,0,0.05);
margin-bottom: 15px;
}
/* 버튼 스타일 */
.stButton>button {
width: 100%;
border-radius: 15px;
border: none;
height: 3.5em;
font-weight: 600;
background-color: #007AFF; /* iOS Blue */
color: white;
}
/* 타이틀 감성 */
h1 { font-weight: 800 !important; color: #1C1C1E !important; }
h3 { color: #8E8E93 !important; font-size: 16px !important; }
</style>
""", unsafe_allow_status=True)
# 2. 사이드바 / 페이지 전환 로직
page = st.sidebar.radio("메뉴 이동", ["🏠 행사 안내", "👥 조원 명단 확인"])
# --- PAGE 1: 행사 안내 ---
if page == "🏠 행사 안내":
st.title("CEO 소통 산책")
st.markdown("### Geumosan Olle-gil Walking")
# 상단 요약 카드
st.markdown(f"""
<div class="ios-card">
<p style="margin:0; font-size:14px; color:#007AFF; font-weight:bold;">Scedule</p>
<p style="margin:5px 0; font-size:18px; font-weight:bold;">2026. 04. 20 (월) 14:00</p>
<p style="margin:0; font-size:14px; color:#8E8E93;">금오산 잔디광장 집결</p>
</div>
""", unsafe_allow_status=True)
# 지도 섹션
st.markdown("#### 🗺️ 미션 지점 안내")
# 금오산 올레길 주요 포인트 좌표 (예시 데이터)
map_data = pd.DataFrame({
'lat': [36.1085, 36.1105, 36.1135], # 잔디광장, 배꼽마당, 뚝방길
'lon': [128.3185, 128.3205, 128.3235],
'name': ['📍 출발: 잔디광장', '⚽ 미션1: 배꼽마당', '🎴 미션2: 하트평상']
})
st.map(map_data, zoom=14)
st.caption("지도상의 위치를 확인하며 이동해 주세요.")
# 액티비티 상세 (클릭형 버튼)
st.markdown("#### 🚩 액티비티 가이드")
with st.expander("⚽ [미션 1] 배꼽마당 미니 골든벨"):
st.write("조원들이 차례대로 미니 골대에 공을 차 넣습니다. 5회 성공 시 스탬프 획득!")
with st.expander("🎴 [미션 2] 뚝방길 딱지치기"):
st.write("하트평상에서 대기 중인 다른 조와 딱지치기 대결을 펼치세요.")
with st.expander("🍴 [식사] 느티나무 백숙"):
st.write("경북 구미시 금오산상가길 89-12")
if st.button("카카오맵 실행"):
st.write("🔗 [길찾기 링크](https://map.kakao.com/link/search/구미느티나무백숙)")
# --- PAGE 2: 조원 명단 ---
else:
st.title("👥 조원 명단")
st.markdown("### 우리 조원을 확인해보세요")
# 예시 데이터 (실제 명단으로 수정 가능)
group_data = {
"1조": ["박성식(조장)", "김철수", "이영희", "최미나"],
"2조": ["정본부", "홍길동", "박지민", "이윤지"],
"3조": ["이부장", "강호동", "유재석", "신사임당"]
}
selected_group = st.selectbox("조를 선택하세요", list(group_data.keys()))
st.markdown(f"""
<div class="ios-card">
<p style="font-size:20px; font-weight:bold; color:#007AFF; margin-bottom:15px;">{selected_group} 멤버</p>
{"<hr style='border:0.1px solid #F2F2F7;'>".join([f"<p style='margin:10px 0;'>👤 {member}</p>" for member in group_data[selected_group]])}
</div>
""", unsafe_allow_status=True)
if st.button("🏠 메인으로 돌아가기"):
st.info("왼쪽 메뉴에서 '행사 안내'를 선택해 주세요.")
# 푸터
st.markdown("<br><p style='text-align:center; color:#C7C7CC; font-size:12px;'>© 2026 LG Way Leadership Development</p>", unsafe_allow_status=True)
