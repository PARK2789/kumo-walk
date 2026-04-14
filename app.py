import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import base64
import os

# 1. 페이지 설정 및 상태 관리
st.set_page_config(page_title="CEO Talk+", page_icon="🍏", layout="centered")

if 'page' not in st.session_state:
    st.session_state.page = 'main'
if 'selected_item' not in st.session_state:
    st.session_state.selected_item = None

# 2. 이미지 base64 변환 (로컬 이미지 로드용)
def get_base64_img(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return ""

# 이미지 파일 로드 (파일명은 실제 저장소 파일명과 일치해야 합니다)
img_forest = get_base64_img("forest.jpg")
img_grass = get_base64_img("grass.jpg")
img_soccer = get_base64_img("soccer.jpg")
img_ddakji = get_base64_img("ddakji.jpg")
img_food = get_base64_img("food.jpg")

# 3. 조원 명단 로드 (members.csv 연동)
def load_member_data():
    if os.path.exists("members.csv"):
        try:
            df = pd.read_csv("members.csv")
            return dict(zip(df['조'], df['명단']))
        except:
            return None
    return None

# 4. 프리미엄 iOS 디자인 시스템 CSS
hero_bg = f"data:image/jpeg;base64,{img_forest}" if img_forest else ""

st.markdown(f"""
<style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    .stApp {{ background-color: #FFFFFF; font-family: 'Pretendard', sans-serif; }}
    
    /* 웅장한 히어로 섹션 */
    .hero-section {{
        background: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.4)), url('{hero_bg}');
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

    /* 프로그램 이미지 박스 */
    .prog-img-box {{
        width: 100%;
        height: 220px;
        border-radius: 28px;
        background-size: cover;
        background-position: center;
        margin-bottom: 12px;
        border: 1px solid rgba(0,0,0,0.05);
    }}
    
    /* 라벨 및 타이틀 */
    .prog-tag {{ font-size: 13px; font-weight: 700; color: #007AFF; margin-bottom: 4px; text-transform: uppercase; }}
    .prog-title {{ font-size: 22px; font-weight: 800; color: #1C1C1E; margin-bottom: 15px; }}

    /* 조원 결과 박스 */
    .member-box {{
        background-color: #F2F2F7;
        padding: 24px;
        border-radius: 24px;
        margin-top: 15px;
        border: 1px solid #E5E5EA;
        margin-bottom: 30px;
    }}

    /* 버튼 스타일 전면 수정 (코드가 글자로 안 나오게) */
    .stButton>button {{
        width: 100%; border-radius: 16px; background-color: #1C1C1E;
        color: white; font-weight: 600; border: none; height: 3.5em;
        font-size: 16px; transition: all 0.2s ease;
    }}
    .stButton>button:active {{ transform: scale(0.98); opacity: 0.9; }}
    
    .back-btn button {{
        background-color: #E5E5EA !important;
        color: #1C1C1E !important;
    }}
</style>
""", unsafe_allow_html=True)

# 5. 데이터 정의
locations = {
    "출발: 잔디광장": {
        "lat": 36.111006, "lon": 128.313156, "color": "green", "icon": "play",
        "bg": img_grass, "tag": "STARTING POINT",
        "detail_title": "새로운 연결의 시작",
        "desc": "금오산 도립공원 잔디광장에서 CEO님과 함께하는 오프닝 행사가 진행됩니다.",
        "points": ["📅 15:30까지 필히 집결", "👥 조별 대항전 가이드 배부", "🥤 생수 및 간식 키트 수령"]
    },
    "Activity1 : 목표달성 ’Goal-In’": {
        "lat": 36.119797, "lon": 128.314458, "color": "blue", "icon": "flag",
        "bg": img_soccer, "tag": "ACTIVITY 01",
        "detail_title": "협동 미니 골든벨 슈팅",
        "desc": "조원 전체의 단합력을 테스트합니다. 릴레이 슈팅으로 골을 성공시키세요.",
        "points": ["⚽ 조원 합산 5회 골인 성공", "⏱️ 성공 시간 기록 측정", "🤝 조원 간 응원 점수 반영"]
    },
    "Activity2 : Bottleneck 타파 ’딱지치기’": {
        "lat": 36.119397, "lon": 128.319959, "color": "red", "icon": "flag",
        "bg": img_ddakji, "tag": "ACTIVITY 02",
        "detail_title": "운명의 딱지치기 대결",
        "desc": "둑방길 하트평상에서 펼쳐지는 다른 조와의 1:1 진검승부!",
        "points": ["🎴 조별 대표 2인 선발", "🥇 3판 2선승제 토너먼트", "🎁 승리 조 커피 기프티콘 증정"]
    },
    "석식 : 버드나무 백숙": {
        "lat": 36.113301, "lon": 128.316201, "color": "purple", "icon": "cutlery",
        "bg": img_food, "tag": "DINNER TIME",
        "detail_title": "즐거운 만찬과 소통",
        "desc": "산책의 피로를 풀며 즐기는 건강한 보양식 시간입니다. CEO님과 자유롭게 대화하세요.",
        "points": ["🍗 한방 능이 백숙 제공", "💬 CEO님과의 자유 소통 Q&A", "🎁 행운의 경품 추첨"]
    }
}

# --- 로직: 내비게이션 ---
def navigate_to(page, target=None):
    st.session_state.page = page
    st.session_state.selected_item = target
    st.rerun()

# --- 화면 1: 메인 홈 ---
if st.session_state.page == 'main':
    # 상단 히어로 섹션
    st.markdown(f"""
    <div class="hero-section">
        <div class="hero-title">CEO Talk<sup>+</sup></div>
        <div class="hero-sub">금오산의 정취를 느끼며,<br>함께 걷는 우리의 미래.</div>
    </div>
    """, unsafe_allow_html=True)

    # [1] 조원 확인 (CSV 연동)
    st.markdown("#### 👥 우리 조원 확인")
    member_data = load_member_data()
    if member_data:
        selected_group = st.selectbox("소속 조를 선택하세요", ["조를 선택해 주세요"] + list(member_data.keys()), label_visibility="collapsed")
        if selected_group != "조를 선택해 주세요":
            st.markdown(f'<div class="member-box"><b>{selected_group} 멤버 명단</b><br>{member_data[selected_group]}</div>', unsafe_allow_html=True)
    else:
        st.warning("members.csv 파일을 찾을 수 없습니다.")

    # [2] 지도 섹션
    st.markdown("#### 🗺️ 코스 지도")
    st.caption("지도 위의 마커를 클릭하면 상세 페이지로 이동합니다.")
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
            navigate_to('detail', clicked)

    # [3] 프로그램 리스트
    st.markdown('<h4 style="margin-top:40px; margin-bottom:20px;">🚩 프로그램 상세 정보</h4>', unsafe_allow_html=True)
    for name, info in locations.items():
        bg_url = f"data:image/jpeg;base64,{info['bg']}" if info['bg'] else ""
        st.markdown(f"""
        <div style="margin-bottom: 40px;">
            <div class="prog-tag">{info['tag']}</div>
            <div class="prog-title">{name}</div>
            <div class="prog-img-box" style="background-image: url('{bg_url}');"></div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"{name} 상세보기", key=f"btn_{name}"):
            navigate_to('detail', name)

# --- 화면 2: 상세 정보 ---
elif st.session_state.page == 'detail':
    name = st.session_state.selected_item
    item = locations[name]
    
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("← 돌아가기"):
        navigate_to('main')
    st.markdown('</div>', unsafe_allow_html=True)

    bg_url = f"data:image/jpeg;base64,{item['bg']}" if item['bg'] else ""
    st.markdown(f"""
    <div style="background: linear-gradient(rgba(0,0,0,0.2), rgba(0,0,0,0.5)), url('{bg_url}'); 
                background-size: cover; background-position: center; height: 280px; 
                border-radius: 35px; margin: 25px 0; display: flex; align-items: flex-end; padding: 35px;">
        <div style="color: white;">
            <div style="font-size: 14px; font-weight: 700; opacity: 0.8;">{item['tag']}</div>
            <div style="font-size: 34px; font-weight: 900; letter-spacing: -1.5px;">{name}</div>
        </div>
    </div>
    <div style="background-color: #F8F9FA; padding: 30px; border-radius: 28px; border: 1px solid #E5E5EA; margin-top:20px;">
        <h3 style="margin-top:0;">{item['detail_title']}</h3>
        <p style="font-size: 17px; color: #3A3A3C; line-height: 1.6;">{item['desc']}</p>
        <hr style="border: 0; border-top: 1px solid #E5E5EA; margin: 25px 0;">
        <h5 style="margin-top:0; font-weight:800;">💡 주요 안내</h5>
        {"".join([f'<div style="margin-bottom:10px; font-size:15px;">✅ {p}</div>' for p in item['points']])}
    </div>
    """, unsafe_allow_html=True)

    if st.button("📍 길찾기 시작 (카카오맵)"):
        st.markdown(f"https://map.kakao.com/link/search/{name}")

# 푸터 수정
st.markdown("<br><p style='text-align:center; color:#C7C7CC; font-size:12px;'>© 2026 LG Innotek Talent Development Team</p>", unsafe_allow_html=True)

