import streamlit as st
import pandas as pd
# 1. 페이지 설정 (iOS 스타일 디자인)
st.set_page_config(page_title="CEO 소통 산책", page_icon="🍏", layout="centered")
# CSS 커스텀 디자인 (iOS 감성 적용)
st.markdown("""
<style>
.stApp { background-color: #F2F2F7; }
.ios-card {
background-color: white;
padding: 22px;
border-radius: 20px;
box-shadow: 0 4px 12px rgba(0,0,0,0.05);
margin-bottom: 20px;
border: 0.5px solid #E5E5EA;
}
.stButton>button {
width: 100%;
border-radius: 12px;
background-color: #007AFF;
color: white;
font-weight: 600;
border: none;
height: 3.5em;
}
h1 { font-weight: 800 !important; letter-spacing: -0.5px; }
</style>
""", unsafe_allow_status=True)
# 2. 사이드바 메뉴 (페이지 전환)
page = st.sidebar.radio("메뉴 선택", ["🏠 행사 안내", "👥 조원 명단 확인"])
# --- PAGE 1: 행사 안내 ---
if page == "🏠 행사 안내":
    st.title("CEO 소통 산책")
st.markdown("### 금오산 올레길 코스 안내")
# 상단 요약 카드
st.markdown("""
<div class="ios-card">
<p style="margin:0; font-size:14px; color:#007AFF; font-weight:bold;">Scedule</p>
<p style="margin:5px 0; font-size:19px; font-weight:bold;">2026. 04. 20 (월) 14:00</p>
<p style="margin:0; font-size:14px; color:#8E8E93;">금오산 잔디광장 집결</p>
</div>
""", unsafe_allow_status=True)
# 3. 지도 표시 (Activity 장소 표시)
st.markdown("#### 🗺️ 미션 지점 안내")
# 금오산 올레길 실제 포인트 근사치 (잔디광장, 배꼽마당, 뚝방길 평상)
map_data = pd.DataFrame({
'lat': [36.1083, 36.1105, 36.1130],
'lon': [128.3180, 128.3208, 128.3225],
'name': ['📍 출발: 잔디광장', '⚽ 미션1: 배꼽마당', '🎴 미션2: 하트평상']
})
st.map(map_data, color="#007AFF", zoom=14)
st.caption("지도상의 파란 점이 주요 미션 포인트입니다.")
# 4. 액티비티 상세 가이드
st.markdown("#### 🚩 액티비티 상세")
with st.expander("⚽ [미션 1] 배꼽마당 미니 골든벨"):
    st.write("**장소:** 올레길 초입 배꼽마당")
st.info("조원들과 협력하여 미니 골대에 공을 차 넣으세요! (5회 성공 미션)")
with st.expander("🎴 [미션 2] 뚝방길 하트평상 딱지치기"):
    st.write("**장소:** 올레길 뚝방길 하트모양 평상")
st.info("추억의 딱지치기! 상대 조의 딱지를 넘기면 점수를 획득합니다.")
with st.expander("🍴 [식사] 느티나무 백숙"):
    st.write("**주소:** 경북 구미시 금오산상가길 89-12")
if st.button("카카오맵으로 식당 찾기"):
    st.markdown("[🔗 여기를 클릭하여 지도로 이동](https://map.kakao.com/link/search/구미느티나무백숙)")
# --- PAGE 2: 조원 명단 확인 ---
else:
    st.title("👥 조원 명단")
st.markdown("### 우리 조 멤버를 확인하세요")
# 조별 데이터 예시 (성식님이 내용을 수정하시면 됩니다)
group_info = {
"1조": ["박성식(조장)", "김대리", "이과장", "박사원"],
"2조": ["김본부", "이팀장", "최주임", "정사원"],
"3조": ["최이사", "강부장", "조대리", "윤사원"]
}
selected_group = st.selectbox("본인의 조를 선택하세요", list(group_info.keys()))
st.markdown(f"""
<div class="ios-card">
<p style="font-size:18px; font-weight:bold; color:#007AFF; margin-bottom:15px;">{selected_group} 명단</p>
{"<hr style='border:0; height:1px; background:#F2F2F7; margin:10px 0;'>".join([f"<p style='margin:12px 0; font-weight:500;'>👤 {name}</p>" for name in group_info[selected_group]])}
</div>
""", unsafe_allow_status=True)
if st.button("🏠 행사 안내로 돌아가기"):
    st.write("사이드바(왼쪽 화살표)에서 메뉴를 변경해 주세요.")
# 푸터
st.markdown("<br><p style='text-align:center; color:#C7C7CC; font-size:12px;'>© 2026 LG Way Leadership Development</p>", unsafe_allow_status=True)
