# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import base64
import os
import json
import re
import unicodedata

# 1. 페이지 설정
st.set_page_config(page_title="CEO Talk+", page_icon="🍏", layout="centered")

# 2. 세션 상태 관리
if 'view' not in st.session_state:
    st.session_state.view = 'home'
if 'target' not in st.session_state:
    st.session_state.target = None

# 3. 이미지 및 데이터 처리 (캐싱 적용으로 렉 제거)
@st.cache_data
def get_base64_img(file_path):
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

# 4. 프리미엄 CSS (요청하신 여백 및 버튼 스타일 유지)
st.markdown(f"""
<style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    .stApp {{ font-family: 'Pretendard', sans-serif; }}
    html, body, [data-testid="stAppViewContainer"] {{ overflow-x: hidden !important; width: 100% !important; }}
    .block-container {{ padding-top: 1.2rem !important; padding-bottom: 0.5rem !important; max-width: 100% !important; }}
    [data-testid="stVerticalBlock"] > div {{ gap: 0.25rem !important; }}
    .hero-section {{
        background: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.45)), url('{hero_bg}');
        background-size: cover; background-position: center;
        padding: 200px 25px 35px 25px; border-radius: 0 0 35px 35px;
        color: white; text-align: left; margin: -5rem -1rem 1rem -1rem;
    }}
    .hero-title {{ font-weight: 900; font-size: 38px; line-height: 1.1; letter-spacing: -2px; }}
    .info-box {{ background-color: #F2F2F7; padding: 14px 18px; border-radius: 20px; border: 1px solid #E5E5EA; margin-bottom: 6px; }}
    .program-card {{
        position: relative; height: 200px; border-radius: 25px; margin-bottom: 4px; 
        overflow: hidden; background-size: cover; background-position: center; 
        display: flex; flex-direction: column; justify-content: flex-end; padding: 20px; color: white;
    }}
    .card-overlay {{ position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: linear-gradient(to bottom, rgba(0,0,0,0) 30%, rgba(0,0,0,0.85) 100%); z-index: 1; }}
    .card-content {{ position: relative; z-index: 2; pointer-events: none; }}
    .card-title {{ font-size: 21px; font-weight: 800; letter-spacing: -0.8px; }}
    .stButton>button {{ width: 100%; border-radius: 14px; background-color: #1C1C1E; color: white; font-weight: 600; border: none; height: 2.8em; font-size: 14px; margin-bottom: 12px; }}
</style>
""", unsafe_allow_html=True)

def navigate_to(view, target=None):
    st.session_state.view = view
    st.session_state.target = target
    st.rerun()

# 5. 한글 및 HTML 태그 정규화 함수 (매칭 오류 해결용)
def normalize_name(text):
    if not text: return ""
    # HTML 태그 제거 (<br> 등)
    clean = re.sub(r'<[^>]+>', '', text)
    # 한글 인코딩 표준화 (NFC) 및 모든 공백 제거
    clean = "".join(unicodedata.normalize('NFC', clean).split())
    return clean

# --- 화면 렌더링 ---
if st.session_state.view == 'home':
    st.markdown(f"""
    <div class="hero-section"><div class="hero-title">CEO Talk⁺</div><div style="font-size: 17px; opacity: 0.9; margin-top: 8px;">함께 걷는 금오산 올레길,<br>우리가 그리는 새로운 미래.</div></div>
    """, unsafe_allow_html=True)

    st.markdown("#### 🚌 출발 안내")
    st.markdown(f"""
    <div class="info-box">
        <div style="font-weight:800; color:#007AFF; font-size:17px; margin-bottom:8px;">📍 구미 4공장 출발</div>
        <div style="font-size:15px; color:#1C1C1E; font-weight:600;">탑승 장소: 정문 앞</div>
        <div style="font-size:15px; color:#3A3A3C; font-weight:600; margin-top:4px;">출발 시간: <b>15:20까지 집결</b></div>
    </div>
    <div class="info-box">
        <div style="font-weight:800; color:#007AFF; font-size:17px; margin-bottom:8px;">📍 구미 1A 공장 출발</div>
        <div style="font-size:15px; color:#1C1C1E; font-weight:600;">탑승 장소: 매점 앞</div>
        <div style="font-size:15px; color:#3A3A3C; font-weight:600; margin-top:4px;">출발 시간: <b>15:35까지 집결</b></div>
        <div style="font-size:15px; color:#8E8E93; margin-top:8px;">※ ID Card 태깅 & 출입게이트 통과 후 대기</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### 👥 우리 조원 확인")
    if member_data:
        sel = st.selectbox("조 선택", ["조를 선택해 주세요"] + list(member_data.keys()), label_visibility="collapsed")
        if sel != "조를 선택해 주세요":
            st.markdown(f'<div class="info-box"><b>{sel} 멤버</b><br>{member_data[sel]}</div>', unsafe_allow_html=True)

    st.markdown("#### 🗺️ 주요 지점 안내")
    m = folium.Map(location=[36.1155, 128.3160], zoom_start=15, tiles="cartodbvoyager")
    for name, info in program_data.items():
        # name에 <br>이 포함되어 있어도 팝업은 그대로 출력
        popup_html = f'<div style="font-size:13px; font-weight:600; font-family:Pretendard; text-align:center;">{name}</div>'
        folium.Marker([info["lat"], info["lon"]], 
                      popup=folium.Popup(popup_html, max_width=150),
                      icon=folium.Icon(color=info["color"], icon=info["icon"], prefix='fa')).add_to(m)
        label_html = f'<div style="font-size: 11px; font-weight: 800; color: #1C1C1E; text-align: center; background-color: rgba(255, 255, 255, 0.85); padding: 2px 6px; border-radius: 10px; border: 1px solid #E5E5EA; white-space: nowrap; font-family: Pretendard; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">{name}</div>'
        folium.Marker([info["lat"], info["lon"]], icon=folium.features.DivIcon(icon_size=(100,20), icon_anchor=(50, -15), html=label_html)).add_to(m)
    
    map_res = st_folium(m, width="100%", height=300, key="home_map")
    
    # [핵심 수정] 지도 클릭 감지 로직 (프로그램 이름 안의 <br> 태그 무시 처리)
    if map_res and map_res.get("last_object_clicked_popup"):
        clicked_raw = map_res["last_object_clicked_popup"]
        clicked_normalized = normalize_name(clicked_raw)
        
        for key in program_data.keys():
            if normalize_name(key) == clicked_normalized:
                navigate_to('detail', key)
                break

    st.markdown('<h4 style="margin-top:25px; margin-bottom:8px;">🚩 프로그램 가이드</h4>', unsafe_allow_html=True)
    for name, info in program_data.items():
        if "Refresh" in name or "휴식" in name: continue
        img_raw = get_base64_img(info.get("bg_file", ""))
        bg_url = f"data:image/jpeg;base64,{img_raw}" if img_raw else ""
        st.markdown(f"""
        <div class="program-card" style="background-image: url('{bg_url}');">
            <div class="card-overlay"></div>
            <div class="card-content">
                <div style="font-size:11px; font-weight:700; opacity:0.8;">{info.get('tag')}</div>
                <div class="card-title">{name}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"상세보기", key=f"btn_{name}"):
            navigate_to('detail', name)

    st.markdown(f"""
    <div class="info-box" style="text-align:center; margin-top:20px;">
        <h6 style="margin:0; font-weight:800; color:#1C1C1E;">📞 담당자 안내</h6>
        <p style="color:#3A3A3C; font-size:13px; margin:2px 0 0 0;">
            인재육성팀장 김선화 <a href="tel:010-4488-5567" style="color:#007AFF; text-decoration:none; font-weight:700;">010-4488-5567</a>
        </p>
    </div>
    """, unsafe_allow_html=True)

elif st.session_state.view == 'detail':
    name = st.session_state.target
    item = program_data.get(name, {})
    img_raw = get_base64_img(item.get("bg_file", ""))
    bg_url = f"data:image/jpeg;base64,{img_raw}" if img_raw else ""
    
    st.markdown(f"""
    <div style="background: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.5)), url('{bg_url}'); 
                background-size: cover; background-position: center; height: 150px; 
                border-radius: 25px; margin: 0 0 8px 0; display: flex; align-items: flex-end; padding: 20px;">
        <div style="color: white;">
            <div style="font-size: 11px; font-weight: 700; opacity: 0.8;">{item.get('tag')}</div>
            <div style="font-size: 24px; font-weight: 900; line-height: 1.1;">{name}</div>
        </div>
    </div>
    <div style="background-color: #F8F9FA; padding: 16px 20px; border-radius: 22px; border: 1px solid #E5E5EA;">
        <h3 style="margin-top:0; margin-bottom:8px; font-weight:800; font-size: 20px;">{item.get('detail_title')}</h3>
        <p style="font-size: 15px; color: #3A3A3C; line-height: 1.5; margin-bottom: 10px;">{item.get('desc')}</p>
        <hr style="border: 0; border-top: 1px solid #E5E5EA; margin: 10px 0;">
        <h5 style="margin-top:0; margin-bottom:6px; font-weight:800; font-size: 17px;">📝 상세 가이드</h5>
        {"".join([f'<div style="margin-bottom:6px; font-size:15px;">• {p}</div>' for p in item.get('points', [])])}
    </div>
    <div style="margin-top:10px;"></div>
    """, unsafe_allow_html=True)

    if st.button("← 메인 화면으로 돌아가기"):
        navigate_to('home')

st.markdown("<p style='text-align:center; color:#C7C7CC; font-size:11px; margin-top:10px;'>© 2026 LG Innotek Talent Development Team</p>", unsafe_allow_html=True)

