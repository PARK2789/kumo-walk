```python
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# 1. 페이지 설정 및 세션 상태 초기화 (페이지 전환용)
st.set_page_config(page_title="CEO 소통 산책", page_icon="🍏", layout="centered")

if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'target' not in st.session_state:
    st.session_state.target = None

# 2. iOS 프리미엄 스타일 CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;800&display=swap');
    
    .stApp { background-color: #F2F2F7; font-family: 'Pretendard', sans-serif; }
    
    /* 깔끔한 카드 디자인 */
    .ios-card {
        background-color: white; 
        padding: 24px; 
        border-radius: 24px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.04); 
        margin-bottom: 20px;
        border: 1px solid rgba(0,0,0,0.03);
    }
    
    /* 타이틀 감성 */
    .main-title { font-weight: 800; font-size: 32px; color: #1C1C1E; letter-spacing: -1.5px; margin-bottom: 4px; }
    .sub-title { color: #8E8E93; font-size: 16px; margin-bottom: 24px; }
    
    /* 미션 라벨 */
    .label-blue { color: #007AFF; font-weight: 700; font-size: 12px; margin-bottom: 6px; display: block; }
    .label-purple { color: #AF52DE; font-weight: 700; font-size: 12px; margin-bottom: 6px; display: block; }
    
    /* 버튼 커스텀 */
    .stButton>button {
        width: 100%; border-radius: 16px; background-color: #007AFF;
        color: white; font-weight: 600; border: none; height: 3.6em;
        transition: transform 0.1s ease;
    }
    .stButton>button:active { transform: scale(0.97); }
    
    /* 돌아가기 버튼 전용 스타일 */
    div[data-testid="stButton"] > button.back-btn {
        background-color: #E5E5EA !important;
        color: #1C1C1E !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. 고정 데이터 정의
locations = {
    "출발: 잔디광장": {
        "lat": 36.111006, "lon": 128.313156, "color": "green", "icon": "play",
        "type": "mission", "tag": "STARTING POINT",
        "title": "행사 집결 및 출발",
        "desc": "금오산 도립공원 잔디광장에 집결해 주세요. 조별 명단을 확인하고 CEO님과 함께 소통 산책을 시작합니다.",
        "tips": ["👟 편안한 신발을 착용하세요.", "🥤 제공된 생수를 꼭 챙기세요.", "📸 조별 단체사진 촬영이 있습니다."]
    },
    "미션1: 배꼽마당": {
        "lat": 36.119797, "lon": 128.314458, "color": "blue", "icon": "flag",
        "type": "mission", "tag": "ACTIVITY 01",
        "title": "미니 골든벨 슈팅",
        "desc": "배꼽마당 광장에서 펼쳐지는 첫 번째 관문! 조원들이 순서대로 공을 차서 골대에 넣어야 합니다.",
        "tips": ["⚽ 조원 합산 5회 성공 시 통과", "⏱️ 성공 시간에 따라 가산점이 부여됩니다."]
    },
    "미션2: 뚝방길 하트평상": {
        "lat": 36.119397, "lon": 128.319959, "color": "red", "icon": "flag",
        "type": "mission", "tag": "ACTIVITY 02",
        "title": "추억의 딱지치기",
        "desc": "둑방길을 따라 걷다 보면 나오는 하트평상! 대기 중인 다른 조와 운명의 대결을 펼치세요.",
        "tips": ["🎴 조별 대표 2인이 출전합니다.", "🏆 승리 조에게는 저녁 식사 시 보너스 권이 증정됩니다."]
    },
    "버드나무백숙": {
        "lat": 36.113301, "lon": 128.316201, "color": "purple", "icon": "cutlery",
        "type": "food", "tag": "DINNER TIME",
        "title": "즐거운 저녁 식사",
        "desc": "산책 후 즐기는 맛있는 백숙 타임! CEO님과 자유롭게 대화하며 오늘 하루를 마무리하는 자리입니다.",
        "tips": ["🍗 메뉴: 한방 백숙 및 도토리묵", "⏰ 18:00부터 식사가 시작됩니다."]
    }
}

# --- 로직: 페이지 전환 함수 ---
def nav_to(page, target=None):
    st.session_state.page = page
    st.session_state.target = target
    st.rerun()

# --- 화면 1: 메인 홈 화면 ---
if st.session_state.page == 'home':
    st.markdown('<div class="main-title">CEO 소통 산책</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">금오산 올레길: 함께 걷는 길, 더 큰 미래</div>', unsafe_allow_html=True)

    # 상단 요약 카드
    st.markdown("""
    <div class="ios-card">
        <span class="label-blue">Schedule</span>
        <div style="font-size:20px; font-weight:700;">2026. 04. 23 (목) 15:30</div>
        <div style="color:#8E8E93; font-size:14px; margin-top:4px;">📍 금오산 도립공원 잔디광장 집결</div>
    </div>
    """, unsafe_allow_html=True)

    # 지도 섹션
    st.markdown("#### 🗺️ 올레길 코스 지도")
    st.caption("지도 위의 마커를 클릭하면 상세 페이지로 이동합니다.")
    
    m = folium.Map(location=[36.1150, 128.3160], zoom_start=15, tiles="cartodbpositron")
    for name, info in locations.items():
        folium.Marker(
            [info["lat"], info["lon"]],
            popup=name,
            icon=folium.Icon(color=info["color"], icon=info["icon"], prefix='fa')
        ).add_to(m)

    map_data = st_folium(m, width="100%", height=380)

    # 마커 클릭 시 페이지 이동
    if map_data and map_data.get("last_object_clicked_popup"):
        clicked_name = map_data["last_object_clicked_popup"]
        if clicked_name in locations:
            nav_to('detail', clicked_name)

    # 조원 확인 카드
    st.divider()
    st.markdown("#### 👥 우리 조원 확인")
    selected_group = st.selectbox("소속 조를 선택하세요", ["선택 안함", "1조", "2조", "3조"], label_visibility="collapsed")
    group_info = {
        "1조": "박성식(조장), 김대리, 이과장, 최사원",
        "2조": "홍길동(조장), 이팀장, 박주임, 정사원",
        "3조": "강본부(조장), 유재석, 신사임당, 조대리"
    }
    if selected_group != "선택 안함":
        st.markdown(f'<div class="ios-card" style="margin-top:10px; border-left: 5px solid #007AFF;"><b>{selected_group} 멤버:</b><br>{group_info[selected_group]}</div>', unsafe_allow_html=True)

# --- 화면 2: 상세 미션/장소 화면 ---
elif st.session_state.page == 'detail':
    target_name = st.session_state.target
    data = locations[target_name]
    
    # 상단 내비게이션 (뒤로가기)
    if st.button("← 메인 화면으로 돌아가기", key="back_btn"):
        nav_to('home')

    st.markdown(f'<div class="main-title" style="margin-top:20px;">{target_name}</div>', unsafe_allow_html=True)
    
    # 상세 내용 카드
    label_class = "label-purple" if data['type'] == "food" else "label-blue"
    st.markdown(f"""
    <div class="ios-card">
        <span class="{label_class}">{data['tag']}</span>
        <div style="font-size:24px; font-weight:700; margin-bottom:12px;">{data['title']}</div>
        <div style="color:#3A3A3C; line-height:1.6; font-size:16px;">{data['desc']}</div>
    </div>
    """, unsafe_allow_html=True)

    # 추가 안내 가이드 (카드 형태)
    st.markdown("#### 💡 진행 안내")
    for tip in data['tips']:
        st.markdown(f'<div class="ios-card" style="padding:16px; margin-bottom:10px; border-radius:18px;">{tip}</div>', unsafe_allow_html=True)

    # 길찾기 버튼
    st.divider()
    if st.button("📍 이 장소로 길찾기 (카카오맵)"):
        st.markdown(f"[클릭하여 지도로 이동](https://map.kakao.com/link/search/{target_name})")

# 공통 푸터
st.markdown("<br><p style='text-align:center; color:#C7C7CC; font-size:12px;'>© 2026 LG Way Leadership Development</p>", unsafe_allow_html=True)

```
