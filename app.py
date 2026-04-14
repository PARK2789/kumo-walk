import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# 1. 페이지 설정 및 상태 관리
st.set_page_config(page_title="CEO 소통 산책", page_icon="🍏", layout="centered")

if 'view' not in st.session_state:
    st.session_state.view = 'main'
if 'target_mission' not in st.session_state:
    st.session_state.target_mission = None

# 2. 하이엔드 디자인 시스템 CSS
st.markdown("""
<style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    .stApp { background-color: #FFFFFF; font-family: 'Pretendard', sans-serif; }
    
    /* 1. Enlarge Hero Section */
    .hero-section {
        background: linear-gradient(rgba(0,0,0,0.2), rgba(0,0,0,0.5)), url('https://images.unsplash.com/photo-1441974231531-c6227db76b6e?auto=format&fit=crop&q=80&w=1200');
        background-size: cover;
        background-position: center;
        padding: 120px 30px 60px 30px; /* 크기 확대 */
        border-radius: 0 0 50px 50px;
        color: white;
        text-align: left;
        margin: -6rem -2rem 2rem -2rem;
    }
    .hero-title { font-weight: 800; font-size: 42px; line-height: 1.1; letter-spacing: -2px; }
    .hero-sub { font-size: 18px; opacity: 0.9; margin-top: 15px; font-weight: 400; letter-spacing: -0.5px; }

    /* 2. Program Cards with Image Backgrounds */
    .program-card {
        position: relative;
        padding: 40px 25px 25px 25px;
        border-radius: 30px;
        margin-bottom: 20px;
        color: white;
        height: 220px;
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
        background-size: cover;
        background-position: center;
        overflow: hidden;
        border: none;
    }
    .card-overlay {
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: linear-gradient(to bottom, rgba(0,0,0,0.1), rgba(0,0,0,0.7));
        z-index: 1;
    }
    .card-content { position: relative; z-index: 2; }
    .card-title { font-size: 26px; font-weight: 800; margin-bottom: 5px; letter-spacing: -1px; }
    .card-tag { font-size: 13px; font-weight: 600; opacity: 0.8; margin-bottom: 5px; text-transform: uppercase; }
    .card-arrow {
        position: absolute; top: 25px; right: 25px; 
        font-size: 24px; z-index: 3; color: white; opacity: 0.8;
    }

    /* 3. Group Check Styling (iOS Style) */
    .group-box {
        background-color: #F2F2F7;
        padding: 20px;
        border-radius: 20px;
        margin-bottom: 30px;
    }

    /* Native Buttons hidden but functional */
    .stButton>button {
        background-color: #1C1C1E; color: white; border-radius: 15px;
        font-weight: 600; width: 100%; height: 3.5em; border: none;
    }
    .back-btn>button { background-color: #E5E5EA !important; color: #1C1C1E !important; }
</style>
""", unsafe_allow_html=True)

# 3. 데이터 정의 (고정 좌표 및 배경 이미지)
locations = {
    "출발: 잔디광장": {
        "lat": 36.111006, "lon": 128.313156, "color": "green", "icon": "play",
        "bg_img": "https://images.unsplash.com/photo-1500382017468-9049fee74a62?q=80&w=1000",
        "tag": "STARTING POINT",
        "mission_title": "새로운 연결의 시작",
        "description": "금오산 도립공원 잔디광장에서 CEO님과 함께하는 오프닝 행사가 진행됩니다.",
        "details": ["📅 15:30까지 필히 집결", "👥 조별 대항전 가이드 배부", "🥤 생수 및 간식 키트 수령"],
        "reward": "전원 기념 수건 증정"
    },
    "미션1: 배꼽마당": {
        "lat": 36.119797, "lon": 128.314458, "color": "blue", "icon": "flag",
        "bg_img": "https://images.unsplash.com/photo-1574629810360-7efbbe195018?q=80&w=1000",
        "tag": "ACTIVITY 01",
        "mission_title": "협동 미니 골든벨 슈팅",
        "description": "조원 전체의 단합력을 테스트합니다. 릴레이 슈팅으로 골을 성공시키세요.",
        "details": ["⚽ 조원 합산 5회 골인", "⏱️ 성공 시간 기록 측정", "🤝 불참 인원 없이 전원 참여"],
        "reward": "승리 조 가산점 100점"
    },
    "미션2: 하트평상": {
        "lat": 36.119397, "lon": 128.319959, "color": "red", "icon": "flag",
        "bg_img": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=1000",
        "tag": "ACTIVITY 02",
        "mission_title": "운명의 딱지치기 대결",
        "description": "둑방길을 따라 걷다 마주치는 다른 조와의 1:1 진검승부!",
        "details": ["🎴 조별 대표 2인 선발", "🥇 3판 2선승제 토너먼트", "📣 조원들의 응원 필수"],
        "reward": "커피 기프티콘 (승리 조)"
    },
    "버드나무백숙": {
        "lat": 36.113301, "lon": 128.316201, "color": "purple", "icon": "cutlery",
        "bg_img": "https://images.unsplash.com/photo-1598515214211-89d3c73ae83b?q=80&w=1000",
        "tag": "DINNER TIME",
        "mission_title": "즐거운 만찬과 소통",
        "description": "건강한 백숙과 함께 오늘 하루의 산책을 마무리하는 따뜻한 시간입니다.",
        "details": ["🍗 한방 능이 백숙 제공", "💬 CEO님과의 자유 소통 Q&A", "🎁 행운의 경품 추첨"],
        "reward": "풍성한 저녁 식사"
    }
}

# --- 로직: 내비게이션 함수 ---
def go_to(view, target=None):
    st.session_state.view = view
    st.session_state.target_mission = target
    st.rerun()

# --- 화면 1: 메인 홈 ---
if st.session_state.view == 'main':
    # [1] Enlarge Hero Header
    st.markdown("""
    <div class="hero-section">
        <div class="hero-title">CEO<br>소통 산책</div>
        <div class="hero-sub">금오산 올레길의 바람을 담아,<br>함께 걷는 우리의 미래.</div>
    </div>
    """, unsafe_allow_html=True)

    # [2] Group Check (Moved Up)
    st.markdown("#### 👥 우리 조원 확인")
    group = st.selectbox("", ["소속 조를 선택해 주세요", "1조", "2조", "3조"], label_visibility="collapsed")
    group_data = {"1조": "박성식(조장), 김대리, 이과장, 최사원", "2조": "홍길동, 이팀장, 박주임, 정사원", "3조": "강본부, 유재석, 신사임당, 조대리"}
    if group != "소속 조를 선택해 주세요":
        st.markdown(f'<div class="group-box"><b>{group} 멤버 명단</b><br>{group_data[group]}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="margin-bottom:30px;"></div>', unsafe_allow_html=True)

    # [3] Mission Map (Sophisticated Voyager Tiles)
    st.markdown("#### 🗺️ 미션 코스 지도")
    st.caption("지도 위의 마커를 터치하여 상세 미션 내용을 확인하세요.")
    # CartoDB Voyager: 더 세련되고 정보가 풍부한 프리미엄 타일
    m = folium.Map(location=[36.1155, 128.3160], zoom_start=14, tiles="cartodbvoyager")
    for name, info in locations.items():
        folium.Marker(
            [info["lat"], info["lon"]],
            popup=name,
            icon=folium.Icon(color=info["color"], icon=info["icon"], prefix='fa')
        ).add_to(m)

    map_res = st_folium(m, width="100%", height=350)
    
    if map_res and map_res.get("last_object_clicked_popup"):
        clicked = map_res["last_object_clicked_popup"]
        if clicked in locations:
            go_to('detail', clicked)

    # [4] Program Cards with Background Images
    st.markdown("#### 🚩 프로그램 상세 정보")
    for name, info in locations.items():
        # HTML Card Design
        st.markdown(f"""
        <div class="program-card" style="background-image: url('{info['bg_img']}');">
            <div class="card-overlay"></div>
            <div class="card-arrow">↗</div>
            <div class="card-content">
                <div class="card-tag">{info['tag']}</div>
                <div class="card-title">{name}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        # Clickable Button overlayed
        if st.button(f"{name} 상세보기", key=f"btn_{name}"):
            go_to('detail', name)

# --- 화면 2: 상세 정보 ---
elif st.session_state.view == 'detail':
    name = st.session_state.target_mission
    info = locations[name]

    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("← 돌아가기"):
        go_to('main')
    st.markdown('</div>', unsafe_allow_html=True)

    # Detail Header with Image
    st.markdown(f"""
    <div style="background: linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.3)), url('{info['bg_img']}'); 
                background-size: cover; background-position: center; height: 250px; 
                border-radius: 30px; margin: 20px 0; display: flex; align-items: flex-end; padding: 30px;">
        <div style="color: white;">
            <div style="font-size: 14px; font-weight: 600; opacity: 0.8;">{info['tag']}</div>
            <div style="font-size: 34px; font-weight: 800;">{name}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"### {info['mission_title']}")
    
    # Mission Detail Box
    st.markdown(f"""
    <div style="background-color: #F8F9FA; padding: 25px; border-radius: 25px; border: 1px solid #E5E5EA;">
        <p style="font-size: 17px; color: #3A3A3C; line-height: 1.6;">{info['description']}</p>
        <hr style="border: 0; border-top: 1px solid #E5E5EA; margin: 25px 0;">
        <h5 style="margin-top:0;">💡 주요 체크포인트</h5>
        {"".join([f'<div style="margin-bottom:10px; font-size:15px;">✅ {item}</div>' for item in info['details']])}
    </div>
    """, unsafe_allow_html=True)

    # Reward Block
    st.markdown(f"""
    <div style="background-color: #1C1C1E; color: white; padding: 25px; border-radius: 25px; margin-top: 20px;">
        <div style="font-size: 12px; font-weight: 600; opacity: 0.6; text-transform: uppercase;">REWARD / BENEFIT</div>
        <div style="font-size: 24px; font-weight: 800; margin-top: 5px;">🎁 {info['reward']}</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("📍 길찾기 시작 (카카오맵)"):
        st.markdown(f"https://map.kakao.com/link/search/{name}")

# 푸터
st.markdown("<br><p style='text-align:center; color:#C7C7CC; font-size:12px;'>© 2026 LG Innotek Talent Development Team</p>", unsafe_allow_html=True)
