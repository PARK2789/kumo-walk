import streamlit as st
import pandas as pd

# 1. 페이지 설정 및 iOS 스타일 디자인
st.set_page_config(page_title="CEO 소통 산책", page_icon="🍏", layout="centered")

st.markdown("""
<style>
.stApp { background-color: #F2F2F7; }
.ios-card {
background-color: white; 
padding: 22px; 
border-radius: 20px; 
box-shadow: 0 4px 15px rgba(0,0,0,0.05); 
margin-bottom: 20px; 
border: 1px solid #E5E5EA;
}
.stButton>button {
width: 100%; 
border-radius: 15px; 
background-color: #007AFF; 
color: white; 
font-weight: 600; 
border: none; 
height: 3.5em;
}
h1 { font-weight: 800 !important; color: #1C1C1E !important; letter-spacing: -1px; }
</style>
""", unsafe_allow_html=True)

# 2. 메인 헤더
st.title("CEO 소통 산책")
st.markdown("<p style='color: #8E8E93; font-size: 18px; margin-top:-15px;'>함께 걷는 길, 더 큰 미래</p>", unsafe_allow_html=True)

# 3. 행사 요약 카드
st.markdown("""
<div class="ios-card">
<p style="color:#007AFF; font-weight:bold; margin:0; font-size:14px;">Schedule</p>
<h2 style="margin:8px 0; font-size:22px;">2026. 04. 20 (월) 14:00</h2>
<p style="color:#8E8E93; margin:0; font-size:15px;">📍 금오산 도립공원 잔디광장 집결</p>
</div>
""", unsafe_allow_html=True)

# 4. 인터랙티브 지도 (Activity 장소 표시)
st.markdown("#### 🗺️ 미션 지점 안내")
map_data = pd.DataFrame({
'lat': [36.1085, 36.1105, 36.1135],
'lon': [128.3185, 128.3205, 128.3235]
})
st.map(map_data, zoom=14)
st.caption("지도상의 마커: 잔디광장(출발) → 배꼽마당(미션1) → 하트평상(미션2)")

# 5. 액티비티 상세 가이드
st.markdown("#### 🚩 액티비티 가이드")
with st.expander("⚽ [미션 1] 배꼽마당 미니 골든벨"):
    st.write("조원들이 차례대로 미니 골대에 공을 차 넣습니다. 5회 성공 시 미션 완료!")

with st.expander("🎴 [미션 2] 뚝방길 하트평상 딱지치기"):
    st.write("다른 조와 딱지치기 대결을 펼치세요. 승리 조에게 특별 점수 부여!")

with st.expander("🍴 [식사] 느티나무 백숙"):
    st.write("주소: 경북 구미시 금오산상가길 89-12")
    st.markdown("[🔗 카카오맵으로 길찾기](https://map.kakao.com/link/search/구미느티나무백숙)")

# 6. 조별 인원 확인 (상단 메뉴 대신 직관적인 선택창)
st.divider()
st.markdown("#### 👥 조별 진행 인원 확인")
group_names = ["선택하세요", "1조", "2조", "3조"]
selected_group = st.selectbox("소속된 조를 고르시면 명단이 나타납니다.", group_names)

if selected_group == "1조":
    st.info("👤 멤버: 박성식(조장), 김철수, 이영희, 최미나")
elif selected_group == "2조":
    st.info("👤 멤버: 홍길동(조장), 박지민, 이윤지, 정본부")
elif selected_group == "3조":
    st.info("👤 멤버: 강호동(조장), 유재석, 신사임당, 이순신")

# 7. 푸터
st.divider()
st.markdown("<p style='text-align:center; color:#C7C7CC; font-size:12px;'>© 2026 LG Way Leadership Development</p>", unsafe_allow_html=True)
