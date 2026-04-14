```python
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# 1. 페이지 설정 및 상태 관리 (페이지 전환용)
st.set_page_config(page_title="CEO 소통 산책", page_icon="🍏", layout="centered")

if 'view' not in st.session_state:
    st.session_state.view = 'home'
if 'target' not in st.session_state:
    st.session_state.target = None

# 2. 프리미엄 iOS 디자인 시스템 CSS
st.markdown("""
<style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    .stApp { 
        background-color: #F2F2F7; 
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, sans-serif; 
    }
    
    /* 카드 디자인 */
    .premium-card {
        background-color: white; 
        padding: 24px; 
        border-radius: 24px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.03); 
        margin-bottom: 20px;
        border: 1px solid rgba(0,0,0,0.04);
    }
    
    /* 헤더 스타일 */
    .app-header { font-weight: 800; font-size: 34px; color: #1C1C1E; letter-spacing: -1.2px; margin-bottom: 5px; }
    .app-subtitle { color: #8E8E93; font-size: 17px; margin-bottom: 30px; }
    
    /* 뱃지 및 라벨 */
    .badge {
        padding: 5px 12px;
        border-radius: 10px;
        font-size: 12px;
        font-weight: 700;
        text-transform: uppercase;
        margin-bottom: 12px;
        display: inline-block;
    }
    .badge-blue { background-color: #E5F1FF; color: #007AFF; }
    .badge-purple { background-color: #F5E9FF; color: #AF52DE; }
    .badge-green { background-color: #E8F5E9; color: #34C759; }
    
    /* 버튼 커스텀 */
    .stButton>button {
        width: 100%; border-radius: 16px; background-color: #007AFF;
        color: white; font-weight: 600; border: none; height: 3.8em;
        font-size: 16px; transition: all 0.2s ease;
    }
    .stButton>button:active { transform: scale(0.98); opacity: 0.9; }
    
    /* 돌아가기 버튼 */
    div[data-testid="stButton"] button:has(div:contains("돌아가기")) {
        background-color: #E5E5EA !important;
        color: #1C1C1E !important;
    }

    /* 정보 텍스트 */
    .info-title { font-size: 22px; font-weight: 700; color: #1C1C1E; margin-bottom: 8px; }
    .info-desc { font-size: 16px; color: #3A3A3C; line-height: 1.6; }
</style>
""", unsafe_allow_html=True)

# 3. 데이터 정의 (좌표 고정)
locations = {
    "출발: 잔디광장": {
        "lat": 36.111006, "lon": 128.313156, "color": "green", "icon": "play",
        "type": "mission", "badge": "STARTING POINT",
        "goal": "전 조원 정시 집결 및 CEO 오프닝",
        "desc": "금오산 도립공원 잔디광장에 집결하여 소통 산책의 시작을 알립니다. CEO님의 격려사와 함께 조별 미션지가 배부됩니다.",
        "points": ["👟 복장 점검 (운동화 필수)", "🥤 개인별 생수 및 간식 수령", "📸 단체 기념사진 촬영"]
    },
    "미션1: 배꼽마당": {
        "lat": 36.119797, "lon": 128.314458, "color": "blue", "icon": "flag",
        "type": "mission", "badge": "MISSION 01",
        "goal": "협동 미니 골든벨 슈팅",
        "desc": "조원 전체의 단합력을 테스트하는 첫 번째 미션입니다. 지정된 구역에서 공을 차 골대에 넣는 릴레이 미션입니다.",
        "points": ["⚽ 조원 합산 5회 골인 성공", "⏱️ 기록에 따른 차등 점수 부여", "🤝 조원 간 응원 점수 추가 반영"]
    },
    "미션2: 뚝방길 하트평상": {
        "lat": 36.119397, "lon": 128.319959, "color": "red", "icon": "flag",
        "type": "mission", "badge": "MISSION 02",
        "goal": "운명의 딱지치기 대결",
        "desc": "풍경이 아름다운 뚝방길 하트평상 미션지! 대기 중인 운영진 혹은 다른 조와 펼치는 1:1 딱지치기 토너먼트입니다.",
        "points": ["🎴 조별 대표 2인 선발", "🥇 3판 2선승제 대결", "🎁 승리 조 전원에게 커피 쿠폰 증정"]
    },
    "버드나무백숙": {
        "lat": 36.113301, "lon": 128.316201, "color": "purple", "icon": "cutlery",
        "type": "food", "badge": "DINNER",
        "title": "풍성한 저녁 식사 및 소통",
        "desc": "금오산 맛집 '버드나무백숙'에서 즐기는 건강한 저녁 식사 시간입니다. 산책의 피로를 풀며 자유롭게 CEO님과 대화하는 자리입니다.",
        "points": ["🍗 주메뉴: 한방 능이 백숙", "💬 CEO 소통 Q&A 및 경품 추첨", "⏰ 18:00 식사 시작"]
    }
}

# --- 로직: 내비게이션 함수 ---
def navigate_to(page, target=None):
    st.session_state.view = page
    st.session_state.target = target
    st.rerun()

# --- 화면 1: 홈 (지도 및 요약) ---
if st.session_state.view == 'home':
    st.markdown('<h1 class="app-header">CEO 소통 산책</h1>', unsafe_allow_html=True)
    st.markdown('<p class="app-subtitle">금오산 올레길: 함께 걷는 길, 더 큰 미래</p>', unsafe_allow_html=True)

    # 일정 정보 카드
    st.markdown("""
    <div class="premium-card">
        <span class="badge badge-blue">Upcoming Event</span>
        <div class="info-title">2026. 04. 23 (목) 15:30</div>
        <p style="color:#8E8E93; margin:0; font-size:15px;">📍 금오산 도립공원 잔디광장 집결</p>
    </div>
    """, unsafe_allow_html=True)

    # 지도 섹션
    st.markdown("#### 🗺️ 코스 지도")
    st.caption("지도 위의 마커를 터치하여 미션 상세 내용을 확인하세요.")
    
    m = folium.Map(location=[36.1150, 128.3160], zoom_start=15, tiles="cartodbpositron")
    for name, info in locations.items():
        folium.Marker(
            [info["lat"], info["lon"]],
            popup=name,
            icon=folium.Icon(color=info["color"], icon=info["icon"], prefix='fa')
        ).add_to(m)

    map_res = st_folium(m, width="100%", height=380)

    # 클릭 시 페이지 이동
    if map_res and map_res.get("last_object_clicked_popup"):
        clicked_name = map_res["last_object_clicked_popup"]
        if clicked_name in locations:
            navigate_to('detail', clicked_name)

    # 조원 확인 카드
    st.divider()
    st.markdown("#### 👥 우리 조원 확인")
    with st.container():
        group = st.selectbox("소속 조를 선택하세요", ["선택 안함", "1조", "2조", "3조"], label_visibility="collapsed")
        group_data = {
            "1조": "박성식(조장), 김대리, 이과장, 최사원",
            "2조": "홍길동(조장), 이팀장, 박주임, 정사원",
            "3조": "강본부(조장), 유재석, 신사임당, 조대리"
        }
        if group != "선택 안함":
            st.markdown(f'<div class="premium-card" style="margin-top:10px; border-left: 6px solid #007AFF;"><b>{group} 인원:</b><br>{group_data[group]}</div>', unsafe_allow_html=True)

# --- 화면 2: 미션 상세 페이지 ---
elif st.session_state.view == 'detail':
    name = st.session_state.target
    info = locations[name]
    
    # 상단 뒤로가기 버튼
    if st.button("← 메인으로 돌아가기"):
        navigate_to('home')

    st.markdown(f'<h1 class="app-header" style="margin-top:25px;">{name}</h1>', unsafe_allow_html=True)
    
    # 메인 정보 카드
    badge_style = "badge-purple" if info['type'] == "food" else "badge-blue"
    st.markdown(f"""
    <div class="premium-card">
        <span class="badge {badge_style}">{info['badge']}</span>
        <div class="info-title">{info.get('goal', info.get('title'))}</div>
        <p class="info-desc">{info['desc']}</p>
    </div>
    """, unsafe_allow_html=True)

    # 체크리스트/포인트 카드들
    st.markdown("#### 📋 상세 안내")
    for point in info['points']:
        st.markdown(f'<div class="premium-card" style="padding:18px; margin-bottom:12px; border-radius:18px;">{point}</div>', unsafe_allow_html=True)

    # 하단 액션 버튼
    st.divider()
    if st.button("📍 이 지점으로 길찾기 (카카오맵)"):
        st.markdown(f"https://map.kakao.com/link/search/{name}")

# 푸터
st.markdown("<br><p style='text-align:center; color:#C7C7CC; font-size:12px;'>© 2026 LG Innotek Talent Development Team</p>", unsafe_allow_html=True)

```
