import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import base64
import os

# 1. 페이지 설정
st.set_page_config(page_title="CEO Talk+", page_icon="🍏", layout="centered")

# 세션 상태 초기화
if 'page' not in st.session_state:
    st.session_state.page = 'main'
if 'selected_item' not in st.session_state:
    st.session_state.selected_item = None

# 2. 이미지 처리 (base64 인코딩으로 회색 화면 방지)
def get_base64_img(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return ""

img_forest = get_base64_img("forest.jpg")
img_grass = get_base64_img("grass.jpg")
img_soccer = get_base64_img("soccer.jpg")
img_ddakji = get_base64_img("ddakji.jpg")
img_food = get_base64_img("food.jpg")

# 3. 조원 명단 로드
def load_members():
    if os.path.exists("members.csv"):
        try:
            df = pd.read_csv("members.csv")
            return dict(zip(df['조'], df['명단']))
        except: return None
    return None

# 4. 프리미엄 디자인 CSS (dotcle.kr 스타일 반영)
hero_bg = f"data:image/jpeg;base64,{img_forest}" if img_forest else ""

st.markdown(f"""
<style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    .stApp {{ background-color: #FFFFFF; font-family: 'Pretendard', sans-serif; }}
    
    /* Hero Header */
    .hero-section {{
        background: linear-gradient(rgba(0,0,0,0.2), rgba(0,0,0,0.4)), url('{hero_bg}');
        background-size: cover; background-position: center;
        padding: 200px 30px 100px 30px; border-radius: 0 0 60px 60px;
        color: white; text-align: left; margin: -6rem -2rem 3rem -2rem;
    }}
    .hero-title {{ font-weight: 900; font-size: 52px; line-height: 1.1; letter-spacing: -2.5px; }}
    .hero-sub {{ font-size: 20px; opacity: 0.9; margin-top: 15px; font-weight: 400; }}

    /* 카드 스타일 */
    .prog-card-container {{ margin-bottom: 50px; border-radius: 35px; overflow: hidden; }}
    .prog-img-box {{
        width: 100%; height: 260px; background-size: cover; background-position: center;
        border-radius: 35px; margin-bottom: 15px; box-shadow: 0 12px 30px rgba(0,0,0,0.06);
    }}
    .prog-tag {{ font-size: 13px; font-weight: 700; color: #007AFF; margin-bottom: 6px; letter-spacing: 1px; }}
    .prog-title {{ font-size: 26px; font-weight: 800; color: #1C1C1E; margin-bottom: 15px; }}

    /* 조원 결과 박스 */
    .member-box {{
        background-color: #F2F2F7; padding: 26px; border-radius: 28px;
        border: 1px solid #E5E5EA; margin-bottom: 40px;
    }}

    /* 버튼 프리미엄 스타일 */
    .stButton>button {{
        width: 100%; border-radius: 20px; background-color: #1C1C1E;
        color: white; font-weight: 600; border: none; height: 4em;
        font-size: 16px; transition: all 0.2s ease;
    }}
    .stButton>button:active {{ transform: scale(0.98); }}
    .back-btn button {{ background-color: #F2F2F7 !important; color: #1C1C1E !important; }}
</style>
""", unsafe_allow_html=True)

# 5. 데이터 및 실제 올레길 경로 좌표
locations = {
    "출발: 잔디광장": {
        "lat": 36.111006, "lon": 128.313156, "color": "green", "icon": "play",
        "bg": img_grass, "tag": "STARTING POINT",
        "mission_title": "새로운 연결의 시작",
        "desc": "금오산 도립공원 잔디광장에서 CEO님과 함께하는 오프닝 행사가 진행됩니다.",
        "points": ["📅 15:30 정시 집결", "👥 조별 가이드북 수령", "🥤 생수 및 리프레시 키트 증정"]
    },
    "Activity1 : 목표달성 ’Goal-In’": {
        "lat": 36.119797, "lon": 128.314458, "color": "blue", "icon": "flag",
        "bg": img_soccer, "tag": "ACTIVITY 01",
        "mission_title": "협동 미니 골든벨 슈팅",
        "desc": "조원 전체의 단합력을 테스트합니다. 릴레이 슈팅 미션을 완수하세요.",
        "points": ["⚽ 조원 전원 합산 5회 골인", "⏱️ 성공 시간 측정", "📣 응원 점수 실시간 반영"]
    },
    "Activity2 : Bottleneck 타파 ’딱지치기’": {
        "lat": 36.119397, "lon": 128.319959, "color": "red", "icon": "flag",
        "bg": img_ddakji, "tag": "ACTIVITY 02",
        "mission_title": "운명의 딱지치기 대결",
        "desc": "둑방길 하트평상에서 펼쳐지는 1:1 진검승부!",
        "details": ["🎴 조별 대표 2인 대결", "🥇 3판 2선승제 토너먼트"],
        "reward": "커피 기프티콘 증정"
    },
    "석식 : 버드나무 백숙": {
        "lat": 36.113301, "lon": 128.316201, "color": "purple", "icon": "cutlery",
        "bg": img_food, "tag": "DINNER TIME",
        "mission_title": "풍성한 만찬과 소통",
        "desc": "산책의 피로를 풀며 즐기는 건강한 보양식 시간입니다.",
        "points": ["🍗 한방 능이 백숙 만찬", "💬 CEO님과의 자유 소통"]
    }
}

# 실제 금오산 저수지 올레길 산책로를 따라가는 정밀 좌표
olle_path = [
    [36.111006, 128.313156], [36.1118, 128.3131], [36.1128, 128.3132], [36.1141, 128.3134],
    [36.1155, 128.3134], [36.1170, 128.3132], [36.1182, 128.3133], [36.1192, 128.3137],
    [36.119797, 128.314458], # 배꼽마당
    [36.1199, 128.3155], [36.1200, 128.3168], [36.1201, 128.3182], [36.1200, 128.3195],
    [36.119397, 128.319959], # 하트평상 (둑길)
    [36.1180, 128.3198], [36.1165, 128.3195], [36.1152, 128.3190], [36.1143, 128.3181],
    [36.113301, 128.316201]  # 버드나무백숙
]

# 내비게이션 함수
def navigate(page, target=None):
    st.session_state.page = page
    st.session_state.selected_item = target
    st.rerun()

# --- 화면 1: 메인 화면 ---
if st.session_state.page == 'main':
    # 히어로 섹션
    st.markdown(f"""
    <div class="hero-section">
        <div class="hero-title">CEO Talk<sup>+</sup></div>
        <div class="hero-sub">금오산 올레길의 정취를 느끼며,<br>함께 걷는 우리의 미래.</div>
    </div>
    """, unsafe_allow_html=True)

    # [1] 조원 확인
    st.markdown("#### 👥 우리 조원 확인")
    member_data = load_members()
    if member_data:
        choice = st.selectbox("조를 선택하세요", ["조를 선택해 주세요"] + list(member_data.keys()), label_visibility="collapsed")
        if choice != "조를 선택해 주세요":
            st.markdown(f'<div class="member-box"><b>{choice} 멤버 명단</b><br>{member_data[choice]}</div>', unsafe_allow_html=True)
    else: st.warning("members.csv 파일을 확인해주세요.")

    # [2] 정밀 지도 (올레길 실제 경로 반영)
    st.markdown("#### 🗺️ 올레길 산책 코스")
    st.caption("파란색 라인이 실제 산책로 경로입니다. 마커를 클릭해 미션을 확인하세요.")
    m = folium.Map(location=[36.1155, 128.3160], zoom_start=15, tiles="cartodbvoyager")
    
    # 실제 올레길 산책로 하이라이트
    folium.PolyLine(olle_path, color="#007AFF", weight=6, opacity=0.8).add_to(m)
    
    for name, info in locations.items():
        folium.Marker([info["lat"], info["lon"]], popup=name,
                      icon=folium.Icon(color=info["color"], icon=info["icon"], prefix='fa')).add_to(m)
    map_res = st_folium(m, width="100%", height=400)
    if map_res and map_res.get("last_object_clicked_popup"):
        clicked = map_res["last_object_clicked_popup"]
        if clicked in locations: navigate('detail', clicked)

    # [3] 프로그램 카드
    st.markdown('<h4 style="margin-top:50px; margin-bottom:25px;">🚩 프로그램 안내</h4>', unsafe_allow_html=True)
    for name, info in locations.items():
        bg_url = f"data:image/jpeg;base64,{info['bg']}" if info['bg'] else ""
        st.markdown(f"""
        <div class="prog-card-container">
            <div class="prog-tag">{info['tag']}</div>
            <div class="prog-title">{name}</div>
            <div class="prog-img-box" style="background-image: url('{bg_url}');"></div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"{name} 상세보기", key=f"btn_{name}"): navigate('detail', name)

# --- 화면 2: 상세 화면 ---
elif st.session_state.page == 'detail':
    name = st.session_state.selected_item
    item = locations[name]
    if st.button("← 돌아가기"): navigate('main')
    
    bg_url = f"data:image/jpeg;base64,{item['bg']}" if item['bg'] else ""
    st.markdown(f"""
    <div style="background: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.5)), url('{bg_url}'); 
                background-size: cover; background-position: center; height: 320px; 
                border-radius: 40px; margin: 25px 0; display: flex; align-items: flex-end; padding: 40px;">
        <div style="color: white;">
            <div style="font-size: 14px; font-weight: 700; opacity: 0.8; letter-spacing: 1.5px;">{item['tag']}</div>
            <div style="font-size: 38px; font-weight: 900; letter-spacing: -1.5px;">{name}</div>
        </div>
    </div>
    <div style="background-color: #F8F9FA; padding: 35px; border-radius: 35px; border: 1px solid #E5E5EA;">
        <h3 style="margin-top:0; font-weight:800;">{item['mission_title']}</h3>
        <p style="font-size: 18px; color: #3A3A3C; line-height: 1.7;">{item['desc']}</p>
        <hr style="border: 0; border-top: 1px solid #E5E5EA; margin: 30px 0;">
        <h5 style="margin-top:0; font-weight:800;">📝 상세 가이드</h5>
        {"".join([f'<div style="margin-bottom:12px; font-size:16px;">✅ {p}</div>' for p in item.get('points', [])])}
    </div>
    """, unsafe_allow_html=True)
    if st.button("📍 이 지점 길찾기 (카카오맵)"):
        st.markdown(f"https://map.kakao.com/link/search/{name}")

st.markdown("<br><p style='text-align:center; color:#C7C7CC; font-size:12px;'>© 2026 LG Innotek Talent Development Team</p>", unsafe_allow_html=True)

