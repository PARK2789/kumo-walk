import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# 1. 페이지 설정 및 iOS 스타일 디자인
st.set_page_config(page_title="CEO 소통 산책", page_icon="🍏", layout="centered")

st.markdown("""
<style>
    .stApp { background-color: #F2F2F7; }
    .ios-card {
        background-color: white; padding: 22px; border-radius: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 20px;
        border: 1px solid #E5E5EA;
    }
    .stButton>button {
        width: 100%; border-radius: 15px; background-color: #007AFF;
        color: white; font-weight: 600; border: none; height: 3.5em;
    }
    h1 { font-weight: 800 !important; color: #1C1C1E !important; letter-spacing: -1px; }
    .mission-header { color: #007AFF; font-weight: bold; font-size: 18px; margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

# 2. 메인 헤더
st.title("CEO 소통 산책")
st.markdown("<p style='color: #8E8E93; font-size: 16px; margin-top:-15px;'>금오산 올레길: 함께 걷는 길, 더 큰 미래</p>", unsafe_allow_html=True)

# 3. 일정 요약 카드
st.markdown("""
<div class="ios-card">
    <p style="color:#007AFF; font-weight:bold; margin:0; font-size:12px;">Schedule</p>
    <h2 style="margin:5px 0; font-size:20px;">2026. 04. 23 (목) 15:30</h2>
    <p style="color:#8E8E93; margin:0; font-size:14px;">📍 금오산 도립공원 잔디광장 집결</p>
</div>
""", unsafe_allow_html=True)

# 4. ★ 좌표 설정 구역 (이곳의 숫자를 PC에서 딴 숫자로 바꾸세요) ★
# lat: 위도, lon: 경도
locations = [
    {
        "name": "출발: 잔디광장", 
        "lat": 36.111006, "lon": 128.313156, 
        "color": "green", "icon": "home", 
        "mission": "🏃‍♂️ 16:00까지 조별로 집결해주세요!"
    },
    {
        "name": "Activity1 장소: 배꼽마당", 
        "lat": 36.119797, "lon": 128.314458, 
        "color": "blue", "icon": "flag", 
        "mission": "⚽ **[미션 1] 미니 골든벨 슈팅**\n\n조원 전원이 골대에 공을 차 넣으세요! (5회 성공 미션)"
    },
    {
        "name": "Activity2 장소: 뚝방길 하트평상", 
        "lat": 36.119397, "lon": 128.319959, 
        "color": "red", "icon": "flag", 
        "mission": "🎴 **[미션 2] 추억의 딱지치기**\n\n상대 조의 딱지를 넘기면 미션 클리어! 승리 조 점수 부여!"
    },
    {
        "name": "석식장소: 버드나무 백숙", 
        "lat": 36.113301, "lon": 128.316201, 
        "color": "purple", "icon": "flag", 
        "mission": "🎴 **오늘 행사의 마무리를 함께해요"
    }

]

st.markdown("#### 🗺️ 올레길 미션 지도")
st.caption("지도 위 깃발 마커를 클릭하면 상세 미션이 아래에 나타납니다.")

# 지도 생성 및 마커 배치
m = folium.Map(location=[36.1105, 128.3210], zoom_start=15)
for loc in locations:
    folium.Marker(
        [loc["lat"], loc["lon"]],
        popup=loc["name"],
        tooltip=loc["name"],
        icon=folium.Icon(color=loc["color"], icon=loc["icon"], prefix='fa')
    ).add_to(m)

# 지도 렌더링
map_data = st_folium(m, width=700, height=400)

# 5. 미션 표시 로직
st.markdown("#### 🚩 클릭한 지점의 미션")
if map_data and map_data.get("last_object_clicked_popup"):
    clicked_name = map_data["last_object_clicked_popup"]
    for loc in locations:
        if loc["name"] == clicked_name:
            st.info(f"📍 **{loc['name']}**\n\n{loc['mission']}")
            break
else:
    st.warning("지도의 깃발 마커를 클릭해 주세요!")

# 6. 조원 명단 확인
st.divider()
st.markdown("#### 👥 조원 명단 확인")
group = st.selectbox("우리 조를 선택하세요", ["선택 안함", "1조", "2조", "3조", "4조", "5조", "6조"])

group_data = {
    "1조": "박성식(조장), 김대리, 이과장, 최사원",
    "2조": "홍길동(조장), 이팀장, 박주임, 정사원",
    "3조": "강본부(조장), 유재석, 신사임당, 조대리",
    "4조": "",
    "5조": "",
    "6조": ""
}

if group != "선택 안함":
    st.success(f"👤 **{group} 멤버:**\n\n{group_data[group]}")

# 7. 푸터
st.divider()
with st.expander("🍴 석식 장소: 버드나 백숙"):
    st.write("경북 구미시 공원로 26")
    st.markdown("[🔗 카카오맵 길찾기](https://map.kakao.com/link/search/구미버드나무백숙)")

st.caption("© 2026 LG Way Leadership Development")

