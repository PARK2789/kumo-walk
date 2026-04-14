import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# 1. 페이지 설정 및 상태 초기화
st.set_page_config(page_title="CEO 소통 산책", page_icon="🍏", layout="centered")

if 'view' not in st.session_state:
    st.session_state.view = 'main'
if 'target_mission' not in st.session_state:
    st.session_state.target_mission = None

# 2. 고해상도 디자인 시스템 CSS (보내주신 디자인 참고)
st.markdown("""
<style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    .stApp { background-color: #FFFFFF; font-family: 'Pretendard', sans-serif; }
    
    /* Hero Header Section */
    .hero-section {
        background: linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.3)), url('https://images.unsplash.com/photo-1441974231531-c6227db76b6e?auto=format&fit=crop&q=80&w=1000');
        background-size: cover;
        background-position: center;
        padding: 60px 25px;
        border-radius: 0 0 40px 40px;
        color: white;
        text-align: left;
        margin: -6rem -2rem 2rem -2rem;
    }
    .hero-title { font-weight: 800; font-size: 38px; line-height: 1.2; letter-spacing: -1.5px; }
    .hero-sub { font-size: 16px; opacity: 0.9; margin-top: 10px; font-weight: 400; }

    /* Color Blocks (이미지 스타일 반영) */
    .content-block {
        padding: 30px;
        border-radius: 24px;
        margin-bottom: 20px;
        color: white;
        position: relative;
        overflow: hidden;
        min-height: 180px;
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
        cursor: pointer;
        transition: transform 0.2s ease;
    }
    .content-block:hover { transform: translateY(-5px); }
    .block-orange { background-color: #E67E22; }
    .block-mint { background-color: #76C7C0; }
    .block-purple { background-color: #9B59B6; }
    .block-green { background-color: #27AE60; }
    
    .block-title { font-size: 24px; font-weight: 800; margin-bottom: 5px; }
    .block-sub { font-size: 14px; opacity: 0.9; }
    .block-arrow { position: absolute; top: 30px; right: 30px; font-size: 24px; }

    /* Info Section */
    .info-label { color: #8E8E93; font-weight: 600; font-size: 13px; text-transform: uppercase; margin-bottom: 5px; display: block; }
    .info-value { font-size: 18px; font-weight: 700; color: #1C1C1E; margin-bottom: 20px; }
    
    /* Buttons */
    .stButton>button {
        width: 100%; border-radius: 12px; background-color: #1C1C1E;
        color: white; font-weight: 600; border: none; height: 3.5em; margin-top: 10px;
    }
    .back-btn>button {
        background-color: transparent !important; color: #1C1C1E !important; border: 1px solid #E5E5EA !important;
    }
    
    /* Detail Page Mission Box */
    .mission-box {
        background-color: #F8F9FA; padding: 25px; border-radius: 20px; margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# 3. 고정 데이터 정의
locations = {
    "출발: 잔디광장": {
        "lat": 36.111006, "lon": 128.313156, "color": "green", "icon": "play",
        "theme": "block-green", "tag": "STARTING POINT",
        "mission_title": "새로운 연결의 시작",
        "description": "금오산 도립공원 잔디광장에서 CEO님과 함께하는 오프닝 행사가 진행됩니다.",
        "details": ["📅 15:30까지 필히 집결", "👥 조별 대항전 가이드 배부", "🥤 생수 및 간식 키트 수령"],
        "reward": "전원 기념 수건 증정"
    },
    "미션1: 배꼽마당": {
        "lat": 36.119797, "lon": 128.314458, "color": "blue", "icon": "flag",
        "theme": "block-orange", "tag": "ACTIVITY 01",
        "mission_title": "협동 미니 골든벨 슈팅",
        "description": "조원 전체의 단합력을 테스트합니다. 릴레이 슈팅으로 골을 성공시키세요.",
        "details": ["⚽ 조원 합산 5회 골인", "⏱️ 성공 시간 기록 측정", "🤝 불참 인원 없이 전원 참여"],
        "reward": "승리 조 가산점 100점"
    },
    "미션2: 하트평상": {
        "lat": 36.119397, "lon": 128.319959, "color": "red", "icon": "flag",
        "theme": "block-mint", "tag": "ACTIVITY 02",
        "mission_title": "운명의 딱지치기 대결",
        "description": "둑방길을 따라 걷다 마주치는 다른 조와의 1:1 진검승부!",
        "details": ["🎴 조별 대표 2인 선발", "🥇 3판 2선승제 토너먼트", "📣 조원들의 응원 필수"],
        "reward": "커피 기프티콘 (승리 조)"
    },
    "버드나무백숙": {
        "lat": 36.113301, "lon": 128.316201, "color": "purple", "icon": "cutlery",
        "theme": "block-purple", "tag": "DINNER TIME",
        "mission_title": "즐거운 만찬과 소통",
        "description": "건강한 백숙과 함께 오늘 하루의 산책을 마무리하는 따뜻한 시간입니다.",
        "details": ["🍗 한방 능이 백숙 제공", "💬 CEO님과의 자유 소통 Q&A", "🎁 행운의 경품 추첨"],
        "reward": "풍성한 저녁 식사"
    }
}

# --- 페이지 내비게이션 함수 ---
def go_to(view, target=None):
    st.session_state.view = view
    st.session_state.target_mission = target
    st.rerun()

# --- 화면 1: 메인 화면 ---
if st.session_state.view == 'main':
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <div class="hero-title">CEO<br>소통 산책</div>
        <div class="hero-sub">함께 걷는 금오산 올레길, 더 큰 미래를 그립니다.</div>
    </div>
    """, unsafe_allow_html=True)

    # 핵심 정보 섹션
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<span class="info-label">DATE & TIME</span>', unsafe_allow_html=True)
        st.markdown('<div class="info-value">04. 23 (목) 15:30</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<span class="info-label">LOCATION</span>', unsafe_allow_html=True)
        st.markdown('<div class="info-value">금오산 잔디광장</div>', unsafe_allow_html=True)

    # 지도 섹션
    st.markdown("#### 🗺️ 미션 코스 지도")
    st.caption("지도 위의 깃발을 클릭하면 상세 미션 페이지로 이동합니다.")
    m = folium.Map(location=[36.1150, 128.3160], zoom_start=14, tiles="cartodbpositron")
    for name, info in locations.items():
        folium.Marker(
            [info["lat"], info["lon"]],
            popup=name,
            icon=folium.Icon(color=info["color"], icon=info["icon"], prefix='fa')
        ).add_to(m)

    map_res = st_folium(m, width="100%", height=300)
    
    if map_res and map_res.get("last_object_clicked_popup"):
        clicked = map_res["last_object_clicked_popup"]
        if clicked in locations:
            go_to('detail', clicked)

    # 컬러 블록 메뉴 (보내주신 디자인 방식)
    st.markdown("#### 🚩 주요 프로그램")
    for name, info in locations.items():
        if st.button(f"👉 {name} 상세정보 보기", key=f"btn_{name}"):
            go_to('detail', name)
        st.markdown(f"""
        <div class="content-block {info['theme']}">
            <div class="block-arrow">↗</div>
            <div class="block-sub">{info['tag']}</div>
            <div class="block-title">{name}</div>
        </div>
        """, unsafe_allow_html=True)

    # 조원 확인
    st.divider()
    st.markdown("#### 👥 우리 조원 확인")
    group = st.selectbox("", ["선택하세요", "1조", "2조", "3조"], label_visibility="collapsed")
    group_data = {"1조": "박성식(조장), 김대리, 이과장, 최사원", "2조": "홍길동, 이팀장, 박주임, 정사원", "3조": "강본부, 유재석, 신사임당, 조대리"}
    if group != "선택하세요":
        st.success(f"👤 {group} 멤버: {group_data[group]}")

# --- 화면 2: 상세 화면 ---
elif st.session_state.view == 'detail':
    name = st.session_state.target_mission
    info = locations[name]

    # 뒤로가기 버튼
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("← 돌아가기"):
        go_to('main')
    st.markdown('</div>', unsafe_allow_html=True)

    # 상세 페이지 상단 디자인
    st.markdown(f"""
    <div style="margin-top: 20px;">
        <span class="info-label">{info['tag']}</span>
        <h1 style="font-weight: 800; font-size: 34px; margin-bottom: 10px;">{name}</h1>
        <p style="font-size: 18px; color: #48484A; line-height: 1.5;">{info['mission_title']}</p>
    </div>
    """, unsafe_allow_html=True)

    # 미션 상세 내용 블록
    st.markdown(f"""
    <div class="mission-box">
        <h4 style="margin-top:0;">📋 가이드 안내</h4>
        <p style="color: #3A3A3C;">{info['description']}</p>
        <hr style="border: 0; border-top: 1px solid #E5E5EA; margin: 20px 0;">
        <h4 style="margin-top:0;">💡 주요 체크포인트</h4>
        {"".join([f'<div style="margin-bottom:8px;">✅ {item}</div>' for item in info['details']])}
    </div>
    """, unsafe_allow_html=True)

    # 보상 정보 카드
    st.markdown(f"""
    <div class="content-block {info['theme']}" style="min-height: 120px; margin-top: 20px;">
        <div class="block-sub">REWARD / BENEFIT</div>
        <div class="block-title">🎁 {info['reward']}</div>
    </div>
    """, unsafe_allow_html=True)

    # 길찾기 링크
    if st.button("📍 이 위치로 길찾기 (카카오맵)"):
        st.markdown(f"https://map.kakao.com/link/search/{name}")

# 푸터
st.markdown("<br><p style='text-align:center; color:#C7C7CC; font-size:12px;'>© 2026 LG Way Leadership Development</p>", unsafe_allow_html=True)

