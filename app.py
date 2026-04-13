import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# 1. 페이지 설정 및 디자인
st.set_page_config(page_title="CEO 소통 산책", page_icon="🍏", layout="centered")

st.markdown("""
<style>
    .stApp { background-color: #F2F2F7; }
    .ios-card {
        background-color: white; padding: 20px; border-radius: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 20px;
        border: 1px solid #E5E5EA;
    }
    h1 { font-weight: 800 !important; color: #1C1C1E !important; letter-spacing: -1px; }
</style>
""", unsafe_allow_html=True)

# 2. 메인 타이틀
st.title("CEO 소통 산책")
st.markdown("<p style='color: #8E8E93; font-size: 16px; margin-top:-15px;'>금오산 올레길: 함께 걷는 길, 더 큰 미래</p>", unsafe_allow_html=True)

# 3. 일정 요약 카드
st.markdown("""
<div class="ios-card">
    <p style="color:#007AFF; font-weight:bold; margin:0; font-size:12px;">Schedule</p>
    <h2 style="margin:5px 0; font-size:20px;">2026. 04. 20 (월) 14:00</h2>
    <p style="color:#8E8E93; margin:0; font-size:14px;">📍 금오산 도립공원 잔디광장 집결</p>
</div>
""", unsafe_allow_html=True)

# 4. 지도 설정 (실제 좌표 근사치)
st.markdown("#### 🗺️ 미션 지도 (깃발 클릭)")
st.caption("지도 위 깃발을 클릭하면 미션 내용이 아래에 나타납니다.")

# 지도 중심점 (금오산 저수지)
m = folium.Map(location=[36.1100, 128.3210], zoom_start=15)

# 지점 데이터
locs = [
    {"name": "출발: 잔디광장", "lat": 36.1105, "lon": 128.3182, "color": "green", "icon": "home", "mission": "🏃‍♂️ 14:00까지 잔디광장에 집결하여 조 편성을 완료해 주세요!"},
    {"name": "미션1: 배꼽마당", "lat": 36.1118, "lon": 128.3185, "color": "blue", "icon": "flag", "mission": "⚽ **[미션 1] 미니 골든벨 슈팅**\n\n조원 전원이 골대에 공을 차 넣으세요! (5회 성공 미션)"},
    {"name": "미션2: 하트평상", "lat": 36.1082, "lon": 128.3245, "color": "red", "icon": "flag", "mission": "🎴 **[미션 2] 추억의 딱지치기**\n\n다른 조와 대결하여 딱지를 뒤집으세요! 승리 조 점수 부여!"}
]

# 깃발 마커 추가
for l in locs:
    folium.Marker(
        [l["lat"], l["lon"]],
        popup=l["name"],
        tooltip=l["name"],
        icon=folium.Icon(color=l["color"], icon=l["icon"], prefix='fa')
    ).add_to(m)

# 지도 렌더링
map_data = st_folium(m, width=700, height=400)

# 5. 미션 내용 표시 (지도 클릭 연동)
st.markdown("#### 🚩 지점별 미션 내용")
if map_data and map_data.get("last_object_clicked_popup"):
    clicked_name = map_data["last_object_clicked_popup"]
    found_mission = "선택한 지점의 정보를 찾을 수 없습니다."
    for l in locs:
        if l["name"] == clicked_name:
            found_mission = l["mission"]
            st.info(f"📍 **{l['name']}**\n\n{found_mission}")
else:
    st.warning("지도의 깃발 마커를 클릭해 주세요!")

# 6. 조별 인원 확인 (iOS 스타일)
st.divider()
st.markdown("#### 👥 조별 진행 인원 확인")
group = st.selectbox("우리 조를 선택하세요", ["선택 안함", "1조", "2조", "3조"])

if group == "1조":
    st.success("👤 멤버: 박성식(조장), 김대리, 이과장, 박사원")
elif group == "2조":
    st.success("👤 멤버: 홍길동(조장), 이팀장, 최주임, 정사원")
elif group == "3조":
    st.success("👤 멤버: 강본부(조장), 유재석, 신사임당, 조대리")

# 7. 푸터 및 길찾기
st.divider()
with st.expander("🍴 석식 장소: 느티나무 백숙"):
    st.write("주소: 구미시 금오산상가길 89-12")
    st.markdown("[🔗 카카오맵 길찾기 시작](https://map.kakao.com/link/search/구미느티나무백숙)")

st.caption("© 2026 LG Way Leadership Development")

