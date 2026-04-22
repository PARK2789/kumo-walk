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

# 3. 이미지 및 데이터 처리 (캐싱 적용으로 버튼 클릭 시 렉 제거)
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

# 4. 프리미엄 CSS (사용자 요청 여백 및 버튼 스타일 유지)
st.markdown(f"""
<style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    .stApp {{ font-family: 'Pretendard', sans-serif; }}
    
    /* 모바일 가로 흔들림 방지 */
    html, body, [data-testid="stAppViewContainer"] {{
        overflow-x: hidden !important;
        width: 100% !important;
    }}

    /* 컨테이너 상하 여백 다이어트 */
    .block-container {{
        padding-top: 1.2rem !important;
        padding-bottom: 0.5rem !important;
        max-width: 100% !important;
    }}

    /* 위젯 간 기본 간격(Gap) 최소화 */
    [data-testid="stVerticalBlock"] > div {{
        gap: 0.25rem !important;
    }}

    /* 히어로 섹션 */
    .hero-section {{
        background: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.45)), url('{hero_bg}');
        background-size: cover; background-position: center;
        padding: 120px 25px 35px 25px; border-radius: 0 0 35px 35px;
        color: white; text-align: left; margin: -5rem -1rem 1rem -1rem;
    }}
    .hero-title {{ font-weight: 900; font-size: 38px; line-height: 1.1; letter-spacing: -2px; }}

    /* 정보 박스 */
    .info-box {{
        background-color: #F2F2F7; padding: 14px 18px; border-radius: 20px;
        border: 1px solid #E5E5EA; margin-bottom: 6px;
    }}

    /* 프로그램 카드 높이 축소 (200px) */
    .program-card {{
        position: relative; height: 200px; border-radius: 25px;
        margin-bottom: 4px; overflow: hidden; background-size: cover;
        background-position: center; display: flex; flex-direction: column;
        justify-content: flex-end; padding: 20px; color: white;
    }}
    .card-overlay {{
        position: absolute; top: 0; left: 0; right: 0; bottom: 0;
        background: linear-gradient(to bottom, rgba(0,0,0,0) 30%, rgba(0,0,0,0.85) 100%);
        z-index: 1;
    }}
    .card-content {{ position: relative; z-index: 2; pointer-events: none; }}
    .card-title {{ font-size: 21px; font-weight: 800; letter-spacing: -0.8px; }}

    /* 상세보기 및 돌아가기 버튼 (축소형 유지) */
    .stButton>button {{
        width: 100%; border-radius: 14px; background-color: #1C1C1E;
        color: white; font-weight: 600; border: none; 
        height: 2.8em; 
        font-size: 14px;
        margin-bottom: 12px;
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

    # 출발 안내
    st.markdown("#### 🚌 출발 안내")
    st.markdown(f"""
    <div class="info-box">
        <div style="font-weight:800; color:#007AFF; font-size:14px;">📍 구미 4공장 출발</div>
        <div style="font-size:15px; color:#1C1C1E; font-weight:600;">정문 앞 / 15:20까지 집결</div>
    </div>
    <div class="info-box">
        <div style="font-weight:800; color:#007AFF; font-size:14px;">📍 구미 1A 공장 출발</div>
        <div style="font-size:15px; color:#1C1C1E; font-weight:600;">매점 앞 / 15:35까지 집결</div>
    </div>
    """, unsafe_allow_html=True)

    # 조원 확인
    st.markdown("#### 👥 우리 조원 확인")
    if member_data:
        sel = st.selectbox("조 선택", ["조를 선택해 주세요"] + list(member_data.keys()), label_visibility="collapsed")
        if sel != "조를 선택해 주세요":
            st.markdown(f'<div class="info-box"><b>{sel} 멤버</b><br>{member_data[sel]}</div>', unsafe_allow_html=True)

    # 지도 안내 (텍스트 상시 표시 및 '딱지치기' 매칭 로직 강화)
    st.markdown("#### 🗺️ 주요 지점 안내")
    m = folium.Map(location=[36.1155, 128.3160], zoom_start=15, tiles="cartodbvoyager")
    
    for name, info in program_data.items():
        # 마커 팝업 설정
        popup_content = f'<div style="font-size:13px; font-weight:600; font-family:Pretendard; text-align:center;">{name}</div>'
        folium.Marker([info["lat"], info["lon"]], 
                      popup=folium.Popup(popup_content, max_width=150),
                      icon=folium.Icon(color=info["color"], icon=info["icon"], prefix='fa')).add_to(m)
        
        # 지도상 텍스트 라벨 (사용자 요청 기능 유지)
        label_html = f'''
            <div style="
                font-size: 11px; font-weight: 800; color: #1C1C1E; text-align: center; 
                background-color: rgba(255, 255, 255, 0.85); padding: 2px 6px;
                border-radius: 10px; border: 1px solid #E5E5EA; white-space: nowrap;
                font-family: Pretendard; box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            ">{name}</div>
        '''
        folium.Marker(
            [info["lat"], info["lon"]],
            icon=folium.features.DivIcon(
                icon_size=(100,20),
                icon_anchor=(50, -15),
                html=label_html
            )
        ).add_to(m)
    
    # 지도 렌더링
    map_res = st_folium(m, width="100%", height=300, key="home_map")
    
    # [수정] 딱지치기 등 특정 지점 클릭 시 이동이 안 되던 버그 해결
    if map_res and map_res.get("last_object_clicked_popup"):
        clicked_raw = map_res["last_object_clicked_popup"]
        # HTML 태그 제거 및 불필요한 공백/줄바꿈 완전 제거
        clicked_name = re.sub(r'<[^>]+>', '', clicked_raw).strip()
        
        # 정확한 매칭 및 포함 여부로 매칭성 강화
        match_key = None
        for key in program_data.keys():
            k_clean = key.strip()
            # 팝업 텍스트와 데이터 키값이 서로 포함관계에 있으면 매칭된 것으로 간주 (딱지치기 매칭 강화)
            if k_clean == clicked_name or k_clean in clicked_name or clicked_name in k_clean:
                match_key = key
                break
        
        if match_key:
            navigate_to('detail', match_key)

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
        if st.button(f"{name} 상세보기", key=f"btn_{name}"):
            navigate_to('detail', name)

    # 담당자 안내 (홈 하단 유지)
    st.markdown(f"""
    <div class="info-box" style="text-align:center; margin-top:20px;">
        <h6 style="margin:0; font-weight:800; color:#1C1C1E;">📞 행사 담당자 안내</h6>
        <p style="color:#3A3A3C; font-size:13px; margin:2px 0 0 0;">
            박성식 책임 (인재육성팀) <a href="tel:010-1234-5678" style="color:#007AFF; text-decoration:none; font-weight:700;">010-1234-5678</a>
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

