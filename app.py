import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
# 1. 페이지 설정 및 iOS 스타일 (들여쓰기 최소화)
st.set_page_config(page_title="CEO 소통 산책", page_icon="🍏", layout="centered")
st.markdown("""
<style>
.stApp { background-color: #F2F2F7; }
.ios-card {
background-color: white; padding: 20px; border-radius: 20px;
box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 20px;
border: 1px solid #E5E5EA;
}
.stButton>button {
width: 100%; border-radius: 15px; background-color: #007AFF;
color: white; font-weight: 600; border: none; height: 3.5em;
}
h1 { font-weight: 800 !important; color: #1C1C1E !important; letter-spacing: -1px; }
</style>
""", unsafe_allow_html=True)
# 2. 메인 헤더
st.title("CEO 소통 산책")
st.markdown("<p style='color: #8E8E93; font-size: 16px; margin-top:-15px;'>금오산 올레길: 함께 걷는 길, 더 큰 미래</p>", unsafe_allow_html=True)
# 3. 행사 요약 카드
st.markdown("""
<div class="ios-card">
<p style="color:#007AFF; font-weight:bold; margin:0; font-size:12px;">Scedule</p>
<h2 style="margin:5px 0; font-size:20px;">2026. 04. 20 (월) 14:00</h2>
<p style="color:#8E8E93; margin:0; font-size:14px;">📍 금오산 잔디광장 집결</p>
</div>
""", unsafe_allow_html=True)
# 4. 지도 데이터 설정 (구미 금오산 올레길 실제 좌표 근사치)
# 배꼽마당(초입), 뚝방길(하트평상)
locations = [
{"name": "출발: 잔디광장", "lat": 36.1105, "lon": 128.3182, "icon": "home", "color": "green", "desc": "🏃‍♂️ 14:00까지 집결해 주세요!"},
{"name": "미션1: 배꼽마당", "lat": 36.1118, "lon": 128.3185, "icon": "flag", "color": "blue", "desc": "⚽ **[미션 1] 미니 골든벨 슈팅**\n\n조원 전원이 골대에 공을 차 넣으세요! (5회 성공 미션)"},
{"name": "미션2: 뚝방길 하트평상", "lat": 36.1082, "lon": 128.3245, "icon": "flag", "color": "red", "desc": "🎴 **[미션 2] 추억의 딱지치기**\n\n다른 조와 대결하여 딱지를 뒤집으세요!"}
]
st.markdown("#### 🗺️ 올레길 미션 지도 (깃발 클릭)")
st.caption("지도 위 깃발을 클릭하면 미션 내용이 아래에 나타납니다.")
# 5. Folium 지도 생성
m = folium.Map(location=[36.1100, 128.3210], zoom_start=15, tiles="OpenStreetMap")
for loc in locations:
    folium.Marker(
    [loc["lat"], loc["lon"]],
    popup=loc["name"],
    tooltip=loc["name"],
    icon=folium.Icon(color=loc["color"], icon=loc["icon"], prefix='fa')
    ).add_to(m)
# 지도 띄우기 및 클릭 감지
map_out = st_folium(m, width=700, height=400)
# 6. 클릭 결과에 따른 미션 표시
st.markdown("#### 🚩 선택된 지점 미션")
# 사용자가 마커를 클릭했을 때
if map_out and map_out.get("last_object_clicked_popup"):
   selected_name = map_out["last_object_clicked_popup"]
# 데이터 매칭
found = False
for loc in locations:
   if loc["name"] == selected_name:
      st.info(f"📍 **{loc['name']}**\n\n{loc['desc']}")
      found = True
break
else:
   st.warning("지도의 깃발 마커를 클릭해 주세요.")
# 7. 조원 명단 확인 섹션 (상단 탭 기능 대체)
st.divider()
st.markdown("#### 👥 조별 진행 인원 확인")
group_choice = st.selectbox("우리 조를 선택하세요", ["선택 안함", "1조", "2조", "3조"])
if group_choice == "1조":
   st.info("👤 박성식(조장), 김철수, 이영희, 최미나")
elif group_choice == "2조":
     st.info("👤 홍길동(조장), 박지민, 이윤지, 정본부")
elif group_choice == "3조":
     st.info("👤 강호동(조장), 유재석, 신사임당, 이순신")
# 8. 푸터 및 기타 정보
st.divider()
with st.expander("🍴 석식 장소 안내"):
     st.write("**느티나무 백숙** (구미시 금오산상가길 89-12)")
     st.markdown("[🔗 카카오맵 길찾기](https://map.kakao.com/link/search/구미느티나무백숙)")
     st.caption("© 2026 LG Way Leadership Development")
