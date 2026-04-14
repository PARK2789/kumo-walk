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

# 2. 이미지 base64 변환 (로컬 이미지 로드 및 회색 화면 방지)
def get_base64_img(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return ""

# 파일명 매칭 (저장소에 이 이름들로 사진 파일이 있어야 함)
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
        background: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.45)), url('{hero_bg}');
        background-size: cover;
        background-position: center;
        padding: 180px 30px 80px 30px;
        border-radius: 0 0 60px 60px;
        color: white;
        text-align: left;
        margin: -6rem -2rem 2.5rem -2rem;
    }}
    .hero-title {{ font-weight: 900; font-size: 48px; line-height: 1.1; letter-spacing: -2.5px; }}
    .hero-sub {{ font-size: 19px; opacity: 0.95; margin-top: 15px; font-weight: 400; }}

    /* 프로그램 이미지 박스 */
    .prog-img-box {{
        width: 100%;
        height: 240px;
        border-radius: 32px;
        background-size: cover;
        background-position: center;
        margin-bottom: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.06);
        border: 1px solid rgba(0,0,0,0.03);
    }}
    
    /* 라벨 및 타이틀 */
    .prog-tag {{ font-size: 13px; font-weight: 700; color: #007AFF; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 1px; }}
    .prog-title {{ font-size: 24px; font-weight: 800; color: #1C1C1E; margin-bottom: 15px; letter-spacing: -0.5px; }}

    /* 조원 결과 박스 */
    .member-box {{
        background-color: #F2F2F7;
        padding: 24px;
        border-radius: 24px;
        margin-top: 15px;
        border: 1px solid #E5E5EA;
        margin-bottom: 35px;
    }}

    /* 버튼 스타일 (디자인 정상화) */
    .stButton>button {{
        width: 100%; border-radius: 18px; background-color: #1C1C1E;
        color: white; font-weight: 600; border: none; height: 3.8em;
        font-size: 16px; transition: all 0.2s ease;
    }}
    .stButton>button:active {{ transform: scale(0.98); opacity: 0.9; }}
    
    .back-btn button {{
        background-color: #F2F2F7 !important;
        color: #1C1C1E !important;
        border: 1px solid #E5E5EA !important;
    }}
</style>
""", unsafe_allow_html=True)

# 5. 데이터 및 정밀 올레길 경로 좌표
# 실제 금오산 저수지 산책로 굴곡을 따라가는 정밀 포인트
olle_actual_path = [
    [36.111006, 128.313156], [36.1115, 128.3129], [36.1121, 128.3127], [36.1128, 128.3126], 
    [36.1136, 128.3126], [36.1145, 128.3127], [36.1153, 128.3128], [36.1162, 128.3129], 
    [36.1171, 128.3130], [36.1180, 128.3132], [36.1189, 128.3136], [36.1195, 128.3140],
    [36.119797, 128.314458], # Activity 1: 배꼽마당
    [36.1200, 128.3151], [36.1201, 128.3159], [36.1201, 128.3168], [36.1201, 128.3177], 
    [36.1200, 128.3186], [36.1198, 128.3194], [36.119397, 128.319959], # Activity 2: 하트평상
    [36.1188, 128.3198], [36.1181, 128.3197], [36.1173, 128.3195], [36.1164, 128.3192], 
    [36.1156, 128.3188], [36.1149, 128.3182], [36.1143, 128.3175], [36.1138, 128.3168], 
    [36.113301, 128.316201]  # 석식: 버드나무 백숙
]

locations = {
    "출발: 잔디광장": {
        "lat": 36.111006, "lon": 128.313156, "color": "green", "icon": "play",
        "bg": img_grass, "tag": "STARTING POINT",
        "title": "새로운 연결의 시작", "desc": "금오산 도립공원 잔디광장에서 CEO님과 함께하는 오프닝 행사가 진행됩니다.",
        "points": ["📅 15:30까지 필히 집결", "👥 조별 대항전 가이드 배부", "🥤 생수 및 간식 키트 수령"]
    },
    "Activity1 : 목표달성 ’Goal-In’": {
        "lat": 36.119797, "lon": 128.314458, "color": "blue", "icon": "flag",
        "bg": img_soccer, "tag": "ACTIVITY 01",
        "title": "협동 미니 골든벨 슈팅", "desc": "조원 전체의 단합력을 테스트합니다. 릴레이 슈팅으로 골을 성공시키세요.",
        "points": ["⚽ 조원 합산 5회 골인 성공", "⏱️ 성공 시간 기록 측정", "🤝 조원 간 응원 점수 반영"]
    },
    "Activity2 : Bottleneck 타파 ’딱지치기’": {
        "lat": 36.119397, "lon": 128.319959, "color": "red", "icon": "flag",
        "bg": img_ddakji, "tag": "ACTIVITY 02",
        "title": "운명의 딱지치기 대결", "desc": "둑방길 하트평상에서 펼쳐지는 다른 조와의 1:1 진검승부!",
        "points": ["🎴 조별 대표 2인 선발", "🥇 3판 2선승제 토너먼트", "🎁 승리 조 커피 기프티콘 증정"]
    },
    "석식 : 버드나무 백숙": {
        "lat": 36.113301, "lon": 128.316201, "color": "purple", "icon": "cutlery",
        "bg": img_food, "tag": "DINNER TIME",
        "title": "풍성한 만찬과 소통", "desc": "산책의 피로를 풀며 즐기는 건강한 보양식 시간입니다. CEO님과 자유롭게 대화하세요.",
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
        <div class="hero-sub">금오산 올레길의 정취를 느끼며,<br>함께 걷는 우리의 미래.</div>
    </div>
    """, unsafe_allow_html=True)

    # [1] 조원 확인 (CSV 연동)
    st.markdown("#### 👥 우리 조원 확인")
    member_data = load_member_data()
    if member_data:
        selected_group = st.selectbox("조를 선택하세요", ["조를 선택해 주세요"] + list(member_data.keys()), label_visibility="collapsed")
        if selected_group != "조를 선택해 주세요":
            st.markdown(f'<div class="member-box"><b>{selected_group} 멤버 명단</b><br>{member_data[selected_group]}</div>', unsafe_allow_html=True)
    else:
        st.warning("members.csv 파일을 확인해주세요.")

    # [2] 정교한 지도 섹션 (실제 올레길 경로 반영)
    st.markdown("#### 🗺️ 올레길 산책 코스")
    st.caption("파란색 실선이 실제 금오산 올레길 산책로를 따라가는 경로입니다.")
    
    # CartoDB Voyager 스타일
    m = folium.Map(location=[36.1155, 128.3160], zoom_start=15, tiles="cartodbvoyager")
    
    # 실제 산책로를 정교하게 하이라이트 (굵은 블루 라인)
    folium.PolyLine(
        locations=olle_actual_path,
        color="#007AFF",
        weight=6,
        opacity=0.8
    ).add_to(m)
    
    for name, info in locations.items():
        folium.Marker(
            [info["lat"], info["lon"]],
            popup=name,
            icon=folium.Icon(color=info["color"], icon=info["icon"], prefix='fa')
        ).add_to(m)
        
    map_res = st_folium(m, width="100%", height=380)
    
    if map_res and map_res.get("last_object_clicked_popup"):
        clicked = map_res["last_object_clicked_popup"]
        if clicked in locations:
            navigate_to('detail', clicked)

    # [3] 프로그램 리스트
    st.markdown('<h4 style="margin-top:40px; margin-bottom:20px;">🚩 프로그램 상세 정보</h4>', unsafe_allow_html=True)
    for name, info in locations.items():
        bg_url = f"data:image/jpeg;base64,{info['bg']}" if info['bg'] else ""
        st.markdown(f"""
        <div style="margin-top: 10px;">
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
    <div style="background: linear-gradient(rgba(0,0,0,0.15), rgba(0,0,0,0.5)), url('{bg_url}'); 
                background-size: cover; background-position: center; height: 320px; 
                border-radius: 40px; margin: 25px 0; display: flex; align-items: flex-end; padding: 40px;">
        <div style="color: white;">
            <div style="font-size: 14px; font-weight: 700; opacity: 0.8; letter-spacing: 1px;">{item['tag']}</div>
            <div style="font-size: 38px; font-weight: 900; letter-spacing: -1.5px;">{name}</div>
        </div>
    </div>
    <div style="background-color: #F8F9FA; padding: 35px; border-radius: 30px; border: 1px solid #E5E5EA; margin-top:20px;">
        <h3 style="margin-top:0; font-weight:800;">{item['title']}</h3>
        <p style="font-size: 18px; color: #3A3A3C; line-height: 1.7;">{item['desc']}</p>
        <hr style="border: 0; border-top: 1px solid #E5E5EA; margin: 30px 0;">
        <h5 style="margin-top:0; font-weight:800;">📝 상세 가이드</h5>
        {"".join([f'<div style="margin-bottom:12px; font-size:16px;">✅ {p}</div>' for p in item['points']])}
    </div>
    """, unsafe_allow_html=True)

    if st.button("📍 이 지점 길찾기 (카카오맵)"):
        st.markdown(f"https://map.kakao.com/link/search/{name}")

# 푸터 (LG Innotek Talent Development Team)
st.markdown("<br><p style='text-align:center; color:#C7C7CC; font-size:12px;'>© 2026 LG Innotek Talent Development Team</p>", unsafe_allow_html=True)

