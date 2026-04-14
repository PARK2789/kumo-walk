import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import base64
import os

# 1. 페이지 설정 및 상태 관리
st.set_page_config(page_title="CEO 소통 산책", page_icon="🍏", layout="centered")

if 'page' not in st.session_state:
    st.session_state.page = 'main'
if 'selected_item' not in st.session_state:
    st.session_state.selected_item = None

# 2. 이미지 base64 변환 함수 (회색 화면 방지 및 배경 이미지 주입)
def get_base64_img(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return ""

# 파일명 및 확장자 매칭 (성식님의 요청 반영)
img_forest = get_base64_img("forest.jpg")
img_grass = get_base64_img("grass.jpg")   # .png에서 .jpg로 변경
img_soccer = get_base64_img("soccer.jpg")
img_ddakji = get_base64_img("ddakji.jpg")
img_food = get_base64_img("food.jpg")

# 3. 하이엔드 디자인 시스템 CSS (dotcle.kr 스타일)
hero_bg = f"url('data:image/jpeg;base64,{img_forest}')" if img_forest else "#2D5A27"

st.markdown(f"""
<style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    .stApp {{ background-color: #FFFFFF; font-family: 'Pretendard', sans-serif; }}
    
    /* Hero Header: 웅장한 상단 이미지 섹션 */
    .hero-section {{
        background: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.4)), {hero_bg};
        background-size: cover;
        background-position: center;
        padding: 180px 30px 80px 30px;
        border-radius: 0 0 60px 60px;
        color: white;
        text-align: left;
        margin: -6rem -2rem 2.5rem -2rem;
    }}
    .hero-title {{ font-weight: 900; font-size: 46px; line-height: 1.1; letter-spacing: -2px; }}
    .hero-sub {{ font-size: 19px; opacity: 0.9; margin-top: 15px; font-weight: 400; }}

    /* Program Card: 이미지 배경 + 우측 상단 화살표 */
    .image-card {{
        position: relative;
        height: 260px;
        border-radius: 35px;
        margin-bottom: 20px;
        overflow: hidden;
        background-size: cover;
        background-position: center;
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
        padding: 35px;
        color: white;
        cursor: pointer;
        transition: transform 0.3s ease;
    }}
    .image-card:hover {{ transform: scale(1.02); }}
    .card-overlay {{
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: linear-gradient(to bottom, rgba(0,0,0,0) 20%, rgba(0,0,0,0.8) 100%);
        z-index: 1;
    }}
    .card-content {{ position: relative; z-index: 2; }}
    .card-tag {{ font-size: 13px; font-weight: 700; opacity: 0.8; margin-bottom: 6px; letter-spacing: 1px; }}
    .card-title {{ font-size: 30px; font-weight: 800; letter-spacing: -1.2px; }}
    .card-arrow {{
        position: absolute; top: 35px; right: 35px; 
        font-size: 30px; z-index: 3; font-weight: 300;
    }}

    /* 조원 확인 박스 */
    .group-result {{
        background-color: #F2F2F7;
        padding: 24px;
        border-radius: 24px;
        margin-top: 15px;
        border: 1px solid #E5E5EA;
    }}

    /* 버튼 스타일 */
    .stButton>button {{
        background-color: #1C1C1E; color: white; border-radius: 18px;
        font-weight: 600; width: 100%; height: 4em; border: none; font-size: 16px;
    }}
    .back-btn>button {{ background-color: #E5E5EA !important; color: #1C1C1E !important; }}

    /* 상세 페이지 헤더 */
    .detail-header-img {{
        height: 300px; border-radius: 40px; background-size: cover; background-position: center;
        margin: 20px 0; position: relative; display: flex; align-items: flex-end; padding: 40px;
    }}
</style>
""", unsafe_allow_html=True)

# 4. 데이터 정의 (좌표 및 이미지 매칭)
locations = {
    "출발: 잔디광장": {
        "lat": 36.111006, "lon": 128.313156, "color": "green", "icon": "play",
        "bg_base64": img_grass, "tag": "STARTING POINT",
        "mission_title": "새로운 연결의 시작",
        "desc": "금오산 도립공원 잔디광장 전용 포토존 앞에서 집결합니다.",
        "details": ["📅 15:30 정시 집결 및 CEO 오프닝", "👥 조별 대항전 가이드북 수령", "🥤 생수 및 간식 키트 증정"],
        "reward": "전원 금오산 기념 타월 증정"
    },
    "미션1: 배꼽마당": {
        "lat": 36.119797, "lon": 128.314458, "color": "blue", "icon": "flag",
        "bg_base64": img_soccer, "tag": "ACTIVITY 01",
        "mission_title": "협동 미니 골든벨 슈팅",
        "desc": "조원 전체의 단합력을 테스트합니다. 릴레이 슈팅으로 골인 미션을 완수하세요.",
        "details": ["⚽ 조원 전원 합산 5회 골인", "⏱️ 성공 시간 측정 (가산점 부여)", "🤝 전원 참여 시 추가 점수"],
        "reward": "승리 조 가산점 100점"
    },
    "미션2: 하트평상": {
        "lat": 36.119397, "lon": 128.319959, "color": "red", "icon": "flag",
        "bg_base64": img_ddakji, "tag": "ACTIVITY 02",
        "mission_title": "운명의 딱지치기 대결",
        "desc": "둑방길 하트평상에서 펼쳐지는 1:1 진검승부! 상대 조의 딱지를 넘기세요.",
        "details": ["🎴 조별 대표 2인 선발 대결", "🥇 3판 2선승제 토너먼트", "📣 응원 점수 실시간 반영"],
        "reward": "스타벅스 기프티콘 (승리 조)"
    },
    "버드나무백숙": {
        "lat": 36.113301, "lon": 128.316201, "color": "purple", "icon": "cutlery",
        "bg_base64": img_food, "tag": "DINNER TIME",
        "mission_title": "풍성한 만찬과 소통",
        "desc": "산책의 피로를 풀며 즐기는 건강한 보양식 시간입니다.",
        "details": ["🍗 한방 능이 백숙 및 도토리묵", "💬 CEO님과의 자유 소통 Q&A", "🎁 행운의 경품 추첨"],
        "reward": "최고급 한방 백숙 만찬"
    }
}

def navigate(page, target=None):
    st.session_state.page = page
    st.session_state.selected_item = target
    st.rerun()

# --- 화면 1: 메인 화면 ---
if st.session_state.page == 'main':
    # [Hero Section]
    st.markdown(f"""
    <div class="hero-section">
        <div class="hero-title">CEO<br>소통 산책</div>
        <div class="hero-sub">금오산의 정취를 느끼며,<br>함께 걷는 우리의 미래.</div>
    </div>
    """, unsafe_allow_html=True)

    # [조원 확인 - 상단 배치]
    st.markdown("#### 👥 우리 조원 확인")
    group_choice = st.selectbox("", ["소속 조를 선택해 주세요", "1조", "2조", "3조"], label_visibility="collapsed")
    group_data = {"1조": "박성식(조장), 김대리, 이과장, 최사원", "2조": "홍길동, 이팀장, 박주임, 정사원", "3조": "강본부, 유재석, 신사임당, 조대리"}
    if group_choice != "소속 조를 선택해 주세요":
        st.markdown(f'<div class="group-result"><b>{group_choice} 멤버 명단</b><br>{group_data[group_choice]}</div>', unsafe_allow_html=True)
    
    # [세련된 지도 - Voyager 스타일]
    st.markdown('<h4 style="margin-top:30px;">🗺️ 미션 코스 지도</h4>', unsafe_allow_html=True)
    st.caption("지도 위의 깃발을 터치하여 미션 내용을 확인하세요.")
    m = folium.Map(location=[36.1155, 128.3160], zoom_start=14, tiles="cartodbvoyager")
    for name, info in locations.items():
        folium.Marker([info["lat"], info["lon"]], popup=name,
                      icon=folium.Icon(color=info["color"], icon=info["icon"], prefix='fa')).add_to(m)
    map_res = st_folium(m, width="100%", height=350)
    
    if map_res and map_res.get("last_object_clicked_popup"):
        clicked = map_res["last_object_clicked_popup"]
        if clicked in locations: navigate('detail', clicked)

    # [프로그램 카드 - 이미지 배경]
    st.markdown('<h4 style="margin-top:40px; margin-bottom:20px;">🚩 주요 프로그램</h4>', unsafe_allow_html=True)
    for name, info in locations.items():
        bg_data = f"data:image/jpeg;base64,{info['bg_base64']}" if info['bg_base64'] else ""
        st.markdown(f"""
        <div class="image-card" style="background-image: url('{bg_data}');">
            <div class="card-overlay"></div>
            <div class="card-arrow">↗</div>
            <div class="card-content">
                <div class="card-tag">{info['tag']}</div>
                <div class="card-title">{name}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"{name} 상세보기", key=f"btn_{name}"):
            navigate('detail', name)

# --- 화면 2: 상세 화면 ---
elif st.session_state.page == 'detail':
    name = st.session_state.selected_item
    item = locations[name]
    
    if st.button("← 메인 화면으로 돌아가기"): navigate('main')

    bg_detail = f"data:image/jpeg;base64,{item['bg_base64']}" if item['bg_base64'] else ""
    st.markdown(f"""
    <div class="detail-header-img" style="background-image: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.6)), url('{bg_detail}');">
        <div style="color: white; z-index: 2;">
            <div style="font-size: 14px; font-weight: 700; opacity: 0.8; letter-spacing: 1.5px;">{item['tag']}</div>
            <div style="font-size: 40px; font-weight: 900; letter-spacing: -1.5px;">{name}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"### {item['mission_title']}")
    st.markdown(f"""
    <div style="background-color: #F8F9FA; padding: 30px; border-radius: 30px; border: 1px solid #E5E5EA; margin-top:20px;">
        <p style="font-size: 18px; color: #3A3A3C; line-height: 1.6;">{item['desc']}</p>
        <hr style="border: 0; border-top: 1px solid #E5E5EA; margin: 25px 0;">
        <h5 style="margin-top:0; font-weight:800;">💡 가이드라인</h5>
        {"".join([f'<div style="margin-bottom:12px; font-size:16px;">✅ {line}</div>' for line in item['details']])}
    </div>
    <div style="background-color: #1C1C1E; color: white; padding: 30px; border-radius: 30px; margin-top: 25px;">
        <div style="font-size: 12px; font-weight: 700; opacity: 0.6; text-transform: uppercase;">MISSION REWARD</div>
        <div style="font-size: 28px; font-weight: 900; margin-top: 10px;">🎁 {item['reward']}</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("📍 이 지점으로 길찾기 (카카오맵)"):
        st.markdown(f"https://map.kakao.com/link/search/{name}")

st.markdown("<br><p style='text-align:center; color:#C7C7CC; font-size:12px;'>© 2026 LG Way Leadership Development</p>", unsafe_allow_html=True)

