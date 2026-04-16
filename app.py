import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import base64
import os
import json
import re

# 1. 페이지 설정 (최상단 고정)
st.set_page_config(page_title="CEO Talk+", page_icon="🍏", layout="centered")

# 2. 세션 상태 관리
if 'view' not in st.session_state:
    st.session_state.view = 'home'
if 'target' not in st.session_state:
    st.session_state.target = None

# 3. 이미지 base64 변환
def get_base64_img(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return ""

img_forest = get_base64_img("forest.jpg")

# 4. 데이터 로드
def load_json_data():
    if os.path.exists("programs.json"):
        with open("programs.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def load_member_data():
    if os.path.exists("members.csv"):
        try:
            df = pd.read_csv("members.csv")
            return dict(zip(df['조'], df['명단']))
        except: return None
    return None

program_data = load_json_data()

# 5. 프리미엄 디자인 CSS (모바일 레이아웃 최적화)
hero_bg = f"data:image/jpeg;base64,{img_forest}" if img_forest else ""

st.markdown(f"""
<style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    .stApp {{ background-color: #FFFFFF; font-family: 'Pretendard', sans-serif; }}
    
    /* 상단 잘림 방지 (모바일 안전 영역) */
    .block-container {{ padding-top: 3rem !important; padding-bottom: 5rem !important; }}
    
    .hero-section {{
        background: linear-gradient(rgba(0,0,0,0.15), rgba(0,0,0,0.45)), url('{hero_bg}');
        background-size: cover; background-position: center;
        padding: 180px 30px 60px 30px; border-radius: 0 0 50px 50px;
        color: white; text-align: left; margin: -7rem -2rem 2.5rem -2rem;
    }}
    .hero-title {{ font-weight: 900; font-size: 48px; line-height: 1.1; letter-spacing: -2.5px; }}

    .program-card {{
        position: relative; height: 350px; border-radius: 40px;
        margin-bottom: 25px; overflow: hidden; background-size: cover;
        background-position: center; display: flex; flex-direction: column;
        justify-content: flex-end; padding: 40px; color: white;
        box-shadow: 0 15px 35px rgba(0,0,0,0.12);
        border: 1px solid rgba(255,255,255,0.1);
    }}
    .card-overlay {{
        position: absolute; top: 0; left: 0; right: 0; bottom: 0;
        background: linear-gradient(to bottom, rgba(0,0,0,0) 40%, rgba(0,0,0,0.8) 100%);
        z-index: 1;
    }}
    .card-content {{ position: relative; z-index: 2; pointer-events: none; }}
    .card-tag {{ font-size: 14px; font-weight: 700; color: #FFFFFF; opacity: 0.9; margin-bottom: 8px; letter-spacing: 1px; }}
    .card-title {{ font-size: 28px; font-weight: 800; letter-spacing: -1.2px; line-height: 1.2; }}

    .member-box {{
        background-color: #F2F2F7; padding: 24px; border-radius: 28px;
        border: 1px solid #E5E5EA; margin-bottom: 40px;
    }}

    .stButton>button {{
        width: 100%; border-radius: 20px; background-color: #1C1C1E;
        color: white; font-weight: 600; border: none; height: 4em; font-size: 16px;
    }}
    .stButton>button:active {{ transform: scale(0.98); }}
</style>
""", unsafe_allow_html=True)

# --- 로직: 내비게이션 ---
def navigate_to(view, target=None):
    st.session_state.view = view
    st.session_state.target = target
    st.rerun()

# 전체 앱을 하나의 컨테이너로 감싸고, view 상태에 따라 key를 변경하여 DOM 강제 재생성
app_container = st.container(
   key=f"page-{st.session_state.view}-{st.session_state.target}"
)

with app_container:
    # --- 화면 1: 홈 (Home) ---
    if st.session_state.view == 'home':
        force_mobile_scroll_reset() # 화면 진입 시 즉시 강제 초기화
        
        st.markdown(f"""
        <div class="hero-section">
            <div class="hero-title">CEO Talk<sup>+</sup></div>
            <div style="font-size: 20px; opacity: 0.9; margin-top: 15px;">함께 걷는 금오산 올레길,<br>우리가 그리는 새로운 미래.</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### 👥 우리 조원 확인")
        member_data = load_member_data()
        if member_data:
            selected_group = st.selectbox("조를 선택하세요", ["조를 선택해 주세요"] + list(member_data.keys()), label_visibility="collapsed")
            if selected_group != "조를 선택해 주세요":
                st.markdown(f'<div class="member-box"><b>{selected_group} 멤버 명단</b><br>{member_data[selected_group]}</div>', unsafe_allow_html=True)

        st.markdown("#### 🗺️ 주요 지점 안내")
        m = folium.Map(location=[36.1155, 128.3160], zoom_start=15, tiles="cartodbvoyager")
        for name, info in program_data.items():
            popup_html = f'<div style="font-size: 13px; font-weight: 600; font-family: Pretendard; color: #1C1C1E; text-align: center; padding: 3px;">{name}</div>'
            folium.Marker([info["lat"], info["lon"]], 
                          popup=folium.Popup(popup_html, max_width=150),
                          icon=folium.Icon(color=info["color"], icon=info["icon"], prefix='fa')).add_to(m)
        
        map_res = st_folium(m, width="100%", height=380, key="main_map")
        if map_res and map_res.get("last_object_clicked_popup"):
            clicked = map_res["last_object_clicked_popup"]
            clean_name = re.sub('<[^<]+?>', '', clicked).strip()
            if clean_name in program_data: navigate_to('detail', clean_name)

        st.markdown('<h4 style="margin-top:50px; margin-bottom:25px;">🚩 프로그램 가이드</h4>', unsafe_allow_html=True)
        for name, info in program_data.items():
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

    # --- 화면 2: 상세 정보 (Detail) ---
    elif st.session_state.view == 'detail':
        
        name = st.session_state.target
        item = program_data.get(name, {})
        
        if st.button("← 메인 화면으로 돌아가기"): navigate_to('home')

        img_raw = get_base64_img(item.get("bg_file", ""))
        bg_url = f"data:image/jpeg;base64,{img_raw}" if img_raw else ""
        st.markdown(f"""
        <div style="background: linear-gradient(rgba(0,0,0,0.15), rgba(0,0,0,0.5)), url('{bg_url}'); 
                    background-size: cover; background-position: center; height: 350px; 
                    border-radius: 40px; margin: 25px 0; display: flex; align-items: flex-end; padding: 40px;">
            <div style="color: white;">
                <div style="font-size: 14px; font-weight: 700; opacity: 0.8; letter-spacing: 1px;">{item.get('tag')}</div>
                <div style="font-size: 34px; font-weight: 900; letter-spacing: -1.5px; line-height: 1.1;">{name}</div>
            </div>
        </div>
        <div style="background-color: #F8F9FA; padding: 35px; border-radius: 30px; border: 1px solid #E5E5EA; margin-top:20px;">
            <h3 style="margin-top:0; font-weight:800; font-size: 24px;">{item.get('detail_title')}</h3>
            <p style="font-size: 18px; color: #3A3A3C; line-height: 1.7;">{item.get('desc')}</p>
            <hr style="border: 0; border-top: 1px solid #E5E5EA; margin: 30px 0;">
            <h5 style="margin-top:0; font-weight:800; font-size: 18px;">📝 상세 가이드</h5>
            {"".join([f'<div style="margin-bottom:12px; font-size:16px;">✅ {p}</div>' for p in item.get('points', [])])}
        </div>
        <div style="margin-top:25px;"></div>
        """, unsafe_allow_html=True)

        nav_name = item.get('nav_name', name)
        lat, lon = item.get('lat'), item.get('lon')
        kakao_url = f"https://map.kakao.com/link/to/{nav_name},{lat},{lon}"
        st.link_button("📍 이 지점 길찾기 (카카오맵)", kakao_url)

st.markdown("<br><p style='text-align:center; color:#C7C7CC; font-size:12px;'>© 2026 LG Innotek Talent Development Team</p>", unsafe_allow_html=True)

