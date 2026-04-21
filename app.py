import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import base64
import os
import json
import re

# 1. 페이지 설정
st.set_page_config(page_title="CEO Talk+", page_icon="🍏", layout="centered")

# 2. 세션 상태 관리
if 'view' not in st.session_state:
    st.session_state.view = 'home'
if 'target' not in st.session_state:
    st.session_state.target = None

# 3. 이미지 처리 함수 (캐싱 적용으로 속도 향상)
@st.cache_data
def get_base64_img(file_path):
    """이미지를 한 번만 읽어서 메모리에 저장 (버벅임 방지 핵심)"""
    if os.path.exists(file_path):
        try:
            with open(file_path, "rb") as f:
                data = f.read()
            return base64.b64encode(data).decode()
        except: pass
    return ""

def load_app_data():
    p_data = {}
    if os.path.exists("programs.json"):
        try:
            with open("programs.json", "r", encoding="utf-8") as f:
                p_data = json.load(f)
        except: pass
    
    m_data = {}
    if os.path.exists("members.csv"):
        try:
            df = pd.read_csv("members.csv")
            m_data = dict(zip(df['조'], df['명단']))
        except: pass
    return p_data, m_data

program_data, member_data = load_app_data()
img_forest = get_base64_img("forest.jpg")
hero_bg = f"data:image/jpeg;base64,{img_forest}" if img_forest else ""

# 4. 프리미엄 CSS (카드 높이 축소 및 최적화)
st.markdown(f"""
<style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    .stApp {{ font-family: 'Pretendard', sans-serif; }}
    
    /* 모바일 가로 고정 */
    html, body, [data-testid="stAppViewContainer"] {{
        overflow-x: hidden !important;
        width: 100% !important;
    }}

    .block-container {{
        padding-top: 1.5rem !important;
        padding-bottom: 4rem !important;
        max-width: 100% !important;
    }}

    /* 히어로 섹션 (높이 약간 조절) */
    .hero-section {{
        background: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.45)), url('{hero_bg}');
        background-size: cover; background-position: center;
        padding: 130px 25px 50px 25px; border-radius: 0 0 40px 40px;
        color: white; text-align: left; margin: -5rem -1rem 2rem -1rem;
    }}
    .hero-title {{ font-weight: 900; font-size: 42px; line-height: 1.1; letter-spacing: -2px; }}

    .info-box {{
        background-color: #F2F2F7; padding: 20px; border-radius: 24px;
        border: 1px solid #E5E5EA; margin-bottom: 18px;
    }}

    /* [요청] 프로그램 카드 높이 축소 (320px -> 220px) */
    .program-card {{
        position: relative; height: 220px; border-radius: 30px;
        margin-bottom: 8px; 
        overflow: hidden; background-size: cover;
        background-position: center; display: flex; flex-direction: column;
        justify-content: flex-end; padding: 25px; color: white;
        box-shadow: 0 8px 20px rgba(0,0,0,0.08);
    }}
    .card-overlay {{
        position: absolute; top: 0; left: 0; right: 0; bottom: 0;
        background: linear-gradient(to bottom, rgba(0,0,0,0) 30%, rgba(0,0,0,0.8) 100%);
        z-index: 1;
    }}
    .card-content {{ position: relative; z-index: 2; pointer-events: none; }}
    .card-tag {{ font-size: 12px; font-weight: 700; opacity: 0.9; margin-bottom: 3px; }}
    .card-title {{ font-size: 22px; font-weight: 800; letter-spacing: -0.8px; line-height: 1.2; }}

    /* 버튼 스타일 최적화 */
    .stButton>button {{
        width: 100%; border-radius: 16px; background-color: #1C1C1E;
        color: white; font-weight: 600; border: none; 
        height: 3em; 
        font-size: 15px;
        margin-bottom: 20px;
    }}
</style>
""", unsafe_allow_html=True)

# 5. 내비게이션 함수
def navigate_to(view, target=None):
    st.session_state.view = view
    st.session_state.target = target
    st.rerun()

# --- 화면 렌더링 ---
if st.session_state.view == 'home':
    # [HOME]
    st.markdown(f"""
    <div class="hero-section">
        <div class="hero-title">CEO Talk⁺</div>
        <div style="font-size: 17px; opacity: 0.9; margin-top: 8px;">함께 걷는 금오산 올레길,<br>우리가 그리는 새로운 미래.</div>
    </div>
    """, unsafe_allow_html=True)

    # 1. 출발 안내
    st.markdown("#### 🚌 출발 안내")
    st.markdown(f"""
    <div class="info-box">
        <div style="font-weight:800; color:#007AFF; font-size:14px; margin-bottom:6px;">📍 구미 4공장 출발</div>
        <div style="font-size:16px; color:#1C1C1E; font-weight:600;">탑승 장소: 정문 앞</div>
        <div style="font-size:15px; color:#3A3A3C; margin-top:2px;">출발 시간: <b>15:20까지 집결</b></div>
    </div>
    <div class="info-box">
        <div style="font-weight:800; color:#007AFF; font-size:14px; margin-bottom:6px;">📍 구미 1A 공장 출발</div>
        <div style="font-size:16px; color:#1C1C1E; font-weight:600;">탑승 장소: 매점 앞</div>
        <div style="font-size:15px; color:#3A3A3C; margin-top:2px;">출발 시간: <b>15:35까지 집결</b></div>
        <div style="font-size:12px; color:#8E8E93; margin-top:6px;">※ ID Card 태깅 & 출입게이트 통과 후 대기</div>
    </div>
    """, unsafe_allow_html=True)

    # 2. 조원 확인
    st.markdown("#### 👥 우리 조원 확인")
    if member_data:
        sel = st.selectbox("조 선택", ["조를 선택해 주세요"] + list(member_data.keys()), label_visibility="collapsed")
        if sel != "조를 선택해 주세요":
            st.markdown(f'<div class="info-box"><b>{sel} 멤버 명단</b><br>{member_data[sel]}</div>', unsafe_allow_html=True)

    # 3. 지도 안내
    st.markdown("#### 🗺️ 주요 지점 안내")
    m = folium.Map(location=[36.1155, 128.3160], zoom_start=15, tiles="cartodbvoyager")
    for name, info in program_data.items():
        popup_html = f'<div style="font-size: 13px; font-weight: 600; font-family: Pretendard; color: #1C1C1E; text-align: center; width: 100px;">{name}</div>'
        folium.Marker([info["lat"], info["lon"]], 
                      popup=folium.Popup(popup_html, max_width=150),
                      icon=folium.Icon(color=info["color"], icon=info["icon"], prefix='fa')).add_to(m)
    
    map_res = st_folium(m, width="100%", height=350, key="home_map")
    if map_res and map_res.get("last_object_clicked_popup"):
        clicked = re.sub('<[^<]+?>', '', map_res["last_object_clicked_popup"]).strip()
        if clicked in program_data: navigate_to('detail', clicked)

    # 4. 프로그램 가이드 (Refresh 항목 제외)
    st.markdown('<h4 style="margin-top:40px; margin-bottom:20px;">🚩 프로그램 가이드</h4>', unsafe_allow_html=True)
    for name, info in program_data.items():
        if "Refresh" in name or "휴식" in name:
            continue
            
        img_raw = get_base64_img(info.get("bg_file", ""))
        bg_url = f"data:image/jpeg;base64,{img_raw}" if img_raw else ""
        st.markdown(f"""
        <div class="program-card" style="background-image: url('{bg_url}');">
            <div class="card-overlay"></div>
            <div class="card-content">
                <div class="card-tag">{info.get('tag')}</div>
                <div class="card-title">{name}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"{name} 상세보기", key=f"btn_{name}"):
            navigate_to('detail', name)

    st.markdown(f"""
    <div class="info-box" style="text-align:center; margin-top:30px;">
        <h5 style="margin-top:0; font-weight:800; color:#1C1C1E;">📞 행사 담당자 안내</h5>
        <p style="color:#3A3A3C; font-size:14px; line-height:1.5; margin-bottom:0;">
            <b>박성식 책임 (인재육성팀)</b><br>
            <a href="tel:010-1234-5678" style="color:#007AFF; text-decoration:none; font-weight:700;">010-1234-5678</a>
        </p>
    </div>
    """, unsafe_allow_html=True)

elif st.session_state.view == 'detail':
    # [DETAIL]
    name = st.session_state.target
    item = program_data.get(name, {})
    
    img_raw = get_base64_img(item.get("bg_file", ""))
    bg_url = f"data:image/jpeg;base64,{img_raw}" if img_raw else ""
    st.markdown(f"""
    <div style="background: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.5)), url('{bg_url}'); 
                background-size: cover; background-position: center; height: 50px; 
                border-radius: 30px; margin: 15px 0; display: flex; align-items: flex-end; padding: 30px;">
        <div style="color: white;">
            <div style="font-size: 13px; font-weight: 700; opacity: 0.8;">{item.get('tag')}</div>
            <div style="font-size: 30px; font-weight: 900; line-height: 1.1;">{name}</div>
        </div>
    </div>
    <div style="background-color: #F8F9FA; padding: 30px; border-radius: 25px; border: 1px solid #E5E5EA;">
        <h3 style="margin-top:0; font-weight:800; font-size: 22px;">{item.get('detail_title')}</h3>
        <p style="font-size: 17px; color: #3A3A3C; line-height: 1.6;">{item.get('desc')}</p>
        <hr style="border: 0; border-top: 1px solid #E5E5EA; margin: 25px 0;">
        {"".join([f'<div style="margin-bottom:10px; font-size:16px;">• {p}</div>' for p in item.get('points', [])])}
    </div>
    <div style="margin-top:30px;"></div>
    """, unsafe_allow_html=True)

    if st.button("← 메인 화면으로 돌아가기"):
        navigate_to('home')

st.markdown("<br><p style='text-align:center; color:#C7C7CC; font-size:11px;'>© 2026 LG Innotek Talent Development Team</p>", unsafe_allow_html=True)

