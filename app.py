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

# --- [초강력 스크롤 초기화 스크립트] ---
# 페이지 전환 시점에 호출되어 브라우저의 모든 스크롤 포인트를 강제로 최상단으로 올립니다.
def scroll_to_top():
    st.markdown(
        """
        <div id="scroll-anchor"></div>
        <script>
            function performScroll() {
                // 1. 스트림릿 메인 컨테이너 타겟팅
                var mainSections = window.parent.document.querySelectorAll('section.main');
                mainSections.forEach(function(section) {
                    section.scrollTo({top: 0, behavior: 'auto'});
                });
                
                // 2. 일반 윈도우 스크롤 타겟팅
                window.parent.scrollTo(0, 0);
                window.scrollTo(0, 0);
            }
            // 화면 렌더링 시간을 고려하여 100ms 지연 실행 (가장 확실한 방법)
            setTimeout(performScroll, 100);
        </script>
        """,
        unsafe_allow_html=True
    )

# 세션 상태 관리
if 'view' not in st.session_state:
    st.session_state.view = 'home'
if 'target' not in st.session_state:
    st.session_state.target = None

# 2. 이미지 base64 변환
def get_base64_img(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return ""

img_forest = get_base64_img("forest.jpg")

# 3. 데이터 로드
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

# 4. 디자인 시스템 CSS
hero_bg = f"data:image/jpeg;base64,{img_forest}" if img_forest else ""

st.markdown(f"""
<style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    .stApp {{ background-color: #FFFFFF; font-family: 'Pretendard', sans-serif; }}
    
    /* 상단 여백 잘림 방지 보정 */
    .block-container {{ padding-top: 1rem !important; padding-bottom: 5rem !important; }}
    
    /* 히어로 섹션 */
    .hero-section {{
        background: linear-gradient(rgba(0,0,0,0.15), rgba(0,0,0,0.45)), url('{hero_bg}');
        background-size: cover; background-position: center;
        padding: 160px 30px 60px 30px; border-radius: 0 0 50px 50px;
        color: white; text-align: left; margin: -5rem -2rem 2.5rem -2rem;
    }}
    .hero-title {{ font-weight: 900; font-size: 48px; line-height: 1.1; letter-spacing: -2.5px; }}

    /* 프로그램 카드 (이미지 풀 적용) */
    .program-card {{
        position: relative; height: 320px; border-radius: 35px;
        margin-bottom: 25px; overflow: hidden; background-size: cover;
        background-position: center; display: flex; flex-direction: column;
        justify-content: flex-end; padding: 35px; color: white;
        box-shadow: 0 12px 30px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.1);
    }}
    .card-overlay {{
        position: absolute; top: 0; left: 0; right: 0; bottom: 0;
        background: linear-gradient(to bottom, rgba(0,0,0,0) 40%, rgba(0,0,0,0.85) 100%);
        z-index: 1;
    }}
    .card-content {{ position: relative; z-index: 2; pointer-events: none; }}
    .card-tag {{ font-size: 13px; font-weight: 700; color: #FFFFFF; opacity: 0.9; margin-bottom: 6px; letter-spacing: 1px; }}
    .card-title {{ font-size: 26px; font-weight: 800; letter-spacing: -1.2px; line-height: 1.2; }}

    .member-box {{
        background-color: #F2F2F7; padding: 22px; border-radius: 25px;
        border: 1px solid #E5E5EA; margin-bottom: 35px;
    }}

    .contact-section {{
        background-color: #F8F9FA; padding: 25px; border-radius: 25px;
        border: 1px solid #E5E5EA; margin-top: 40px; text-align: center;
    }}

    .stButton>button {{
        width: 100%; border-radius: 18px; background-color: #1C1C1E;
        color: white; font-weight: 600; border: none; height: 3.8em; font-size: 15px;
    }}
    
    div[data-testid="stLinkButton"] > a {{
        width: 100% !important; border-radius: 18px !important; background-color: #FEE500 !important;
        color: #191919 !important; font-weight: 700 !important; border: none !important; 
        height: 3.8em !important; display: flex !important; align-items: center !important; 
        justify-content: center !important; text-decoration: none !important; font-size: 15px !important;
    }}
</style>
""", unsafe_allow_html=True)

# --- 로직: 내비게이션 ---
def navigate_to(view, target=None):
    st.session_state.view = view
    st.session_state.target = target
    st.rerun()

# --- 화면 1: 홈 (Home) ---
if st.session_state.view == 'home':
    scroll_to_top() # 최상단 이동 실행
    
    st.markdown(f"""
    <div class="hero-section">
        <div class="hero-title">CEO Talk<sup>+</sup></div>
        <div style="font-size: 19px; opacity: 0.9; margin-top: 15px;">함께 걷는 금오산 올레길,<br>우리가 그리는 새로운 미래.</div>
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
        popup_style = f'<div style="font-size: 13px; font-weight: 600; font-family: Pretendard; color: #1C1C1E; text-align: center; padding: 2px;">{name}</div>'
        folium.Marker([info["lat"], info["lon"]], 
                      popup=folium.Popup(popup_style, max_width=150),
                      icon=folium.Icon(color=info["color"], icon=info["icon"], prefix='fa')).add_to(m)
    
    map_res = st_folium(m, width="100%", height=380, key="main_map")
    if map_res and map_res.get("last_object_clicked_popup"):
        clicked = map_res["last_object_clicked_popup"]
        clean_name = re.sub('<[^<]+?>', '', clicked).strip()
        if clean_name in program_data: navigate_to('detail', clean_name)

    st.markdown('<h4 style="margin-top:40px; margin-bottom:20px;">🚩 프로그램 가이드</h4>', unsafe_allow_html=True)
    for name, info in program_data.items():
        img_data = get_base64_img(info["bg_file"])
        bg_url = f"data:image/jpeg;base64,{img_data}" if img_data else ""
        st.markdown(f"""
        <div class="program-card" style="background-image: url('{bg_url}');">
            <div class="card-overlay"></div>
            <div class="card-content">
                <div class="card-tag">{info['tag']}</div>
                <div class="card-title">{name}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"{name} 상세보기", key=f"btn_{name}"):
            navigate_to('detail', name)

    st.markdown(f"""
    <div class="contact-section">
        <h5 style="margin-top:0; font-weight:800; color:#1C1C1E;">📞 행사 담당자 안내</h5>
        <p style="color:#3A3A3C; font-size:15px; line-height:1.6; margin-bottom:0;">
            불편 사항이나 문의 사항은 아래로 연락주세요.<br>
            <b>박성식 책임 (인재육성팀)</b><br>
            <a href="tel:010-1234-5678" style="color:#007AFF; text-decoration:none; font-weight:700;">010-1234-5678</a>
        </p>
    </div>
    """, unsafe_allow_html=True)

# --- 화면 2: 상세 정보 (Detail) ---
elif st.session_state.view == 'detail':
    scroll_to_top() # 상세 페이지 진입 시 최상단 강제 이동
    
    name = st.session_state.target
    item = program_data.get(name, {})
    
    if st.button("← 돌아가기"): navigate_to('home')

    img_data = get_base64_img(item.get("bg_file", ""))
    bg_url = f"data:image/jpeg;base64,{img_data}" if img_data else ""
    st.markdown(f"""
    <div style="background: linear-gradient(rgba(0,0,0,0.15), rgba(0,0,0,0.5)), url('{bg_url}'); 
                background-size: cover; background-position: center; height: 350px; 
                border-radius: 40px; margin: 20px 0; display: flex; align-items: flex-end; padding: 40px;">
        <div style="color: white;">
            <div style="font-size: 14px; font-weight: 700; opacity: 0.8; letter-spacing: 1px;">{item.get('tag')}</div>
            <div style="font-size: 34px; font-weight: 900; letter-spacing: -1.5px; line-height: 1.1;">{name}</div>
        </div>
    </div>
    <div style="background-color: #F8F9FA; padding: 30px; border-radius: 30px; border: 1px solid #E5E5EA; margin-top:15px;">
        <h3 style="margin-top:0; font-weight:800; font-size: 22px;">{item.get('detail_title')}</h3>
        <p style="font-size: 17px; color: #3A3A3C; line-height: 1.6;">{item.get('desc')}</p>
        <hr style="border: 0; border-top: 1px solid #E5E5EA; margin: 25px 0;">
        <h5 style="margin-top:0; font-weight:800; font-size: 18px;">📝 상세 가이드</h5>
        {"".join([f'<div style="margin-bottom:10px; font-size:16px;">✅ {p}</div>' for p in item.get('points', [])])}
    </div>
    <div style="margin-top:20px;"></div>
    """, unsafe_allow_html=True)

    nav_name = item.get('nav_name', name)
    lat, lon = item.get('lat'), item.get('lon')
    kakao_url = f"https://map.kakao.com/link/to/{nav_name},{lat},{lon}"
    st.link_button("📍 이 지점 길찾기 (카카오맵)", kakao_url)

st.markdown("<br><p style='text-align:center; color:#C7C7CC; font-size:11px;'>© 2026 LG Innotek Talent Development Team</p>", unsafe_allow_html=True)
