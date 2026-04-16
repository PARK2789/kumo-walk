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

# --- [모바일 스크롤 강제 리셋: 최종 솔루션] ---
def apply_mobile_scroll_reset():
    # 페이지 상태(view, target)가 바뀔 때마다 고유한 ID 생성
    unique_view_id = f"v-{st.session_state.view}-{st.session_state.target}".replace(" ", "-")
    
    # 1. 최상단에 물리적 앵커 설치
    # 2. JS로 해당 앵커를 '즉시' 화면에 맞춤 (scrollIntoView)
    # 3. Streamlit 메인 컨테이너 직접 제어
    st.markdown(f"""
        <div id="anchor-{unique_view_id}" style="position: absolute; top: -150px; left: 0;"></div>
        <script>
            (function() {{
                const reset = () => {{
                    const anchor = window.parent.document.getElementById("anchor-{unique_view_id}");
                    if (anchor) {{
                        anchor.scrollIntoView({{block: "start", behavior: "instant"}});
                    }}
                    const main = window.parent.document.querySelector(".main");
                    if (main) main.scrollTop = 0;
                    window.parent.scrollTo(0, 0);
                }};
                reset();
                // 모바일 렌더링 타이밍을 고려해 0.1초 뒤 한 번 더 강제 실행
                setTimeout(reset, 100);
            }})();
        </script>
    """, unsafe_allow_html=True)

# 세션 상태 관리
if 'view' not in st.session_state:
    st.session_state.view = 'home'
if 'target' not in st.session_state:
    st.session_state.target = None

# 2. 이미지 로드 함수
def get_base64_img(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return ""

img_forest = get_base64_img("forest.jpg")

# 3. 데이터 로드 (JSON/CSV)
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

# 4. 프리미엄 디자인 CSS
hero_bg = f"data:image/jpeg;base64,{img_forest}" if img_forest else ""

st.markdown(f"""
<style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    .stApp {{ background-color: #FFFFFF; font-family: 'Pretendard', sans-serif; }}
    
    /* 최상단 여백 잘림 방지 (안전 영역) */
    .block-container {{ padding-top: 3.5rem !important; padding-bottom: 6rem !important; }}
    
    .hero-section {{
        background: linear-gradient(rgba(0,0,0,0.15), rgba(0,0,0,0.45)), url('{hero_bg}');
        background-size: cover; background-position: center;
        padding: 180px 30px 70px 30px; border-radius: 0 0 50px 50px;
        color: white; text-align: left; margin: -7.5rem -2rem 2.5rem -2rem;
    }}
    .hero-title {{ font-weight: 900; font-size: 50px; line-height: 1.1; letter-spacing: -2.5px; }}

    /* 프로그램 카드 - 이미지 전체 적용 디자인 */
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
        background: linear-gradient(to bottom, rgba(0,0,0,0) 40%, rgba(0,0,0,0.85) 100%);
        z-index: 1;
    }}
    .card-content {{ position: relative; z-index: 2; pointer-events: none; }}
    .card-tag {{ font-size: 14px; font-weight: 700; color: #FFFFFF; opacity: 0.9; margin-bottom: 8px; letter-spacing: 1px; }}
    .card-title {{ font-size: 30px; font-weight: 800; letter-spacing: -1.2px; line-height: 1.2; }}

    .member-box {{
        background-color: #F2F2F7; padding: 24px; border-radius: 28px;
        border: 1px solid #E5E5EA; margin-bottom: 40px;
    }}

    .stButton>button {{
        width: 100%; border-radius: 20px; background-color: #1C1C1E;
        color: white; font-weight: 600; border: none; height: 4em; font-size: 16px;
    }}
    
    div[data-testid="stLinkButton"] > a {{
        width: 100% !important; border-radius: 20px !important; background-color: #FEE500 !important;
        color: #191919 !important; font-weight: 700 !important; border: none !important; 
        height: 4em !important; display: flex !important; align-items: center !important; 
        justify-content: center !important; text-decoration: none !important; font-size: 16px !important;
    }}
</style>
""", unsafe_allow_html=True)

# --- 로직: 내비게이션 ---
def navigate_to(view, target=None):
    st.session_state.view = view
    st.session_state.target = target
    st.rerun()

# 전체 화면을 고유 키로 감싸서 브라우저가 매번 새 페이지로 인식하게 함
current_page_key = f"page-{st.session_state.view}-{st.session_state.target}"

with st.container(key=current_page_key):
    # 페이지 진입 시 스크롤 리셋 스크립트 주입
    apply_mobile_scroll_reset()

    # --- 화면 1: 홈 (Home) ---
    if st.session_state.view == 'home':
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

        # 담당자 연락처
        st.markdown(f"""
        <div style="background-color:#F8F9FA; padding:30px; border-radius:30px; border:1px solid #E5E5EA; margin-top:50px; text-align:center;">
            <h5 style="margin-top:0; font-weight:800; color:#1C1C1E;">📞 행사 담당자 안내</h5>
            <p style="color:#3A3A3C; font-size:15px; line-height:1.6; margin-bottom:0;">
                불편 사항은 아래로 연락주세요.<br>
                <b>박성식 책임 (인재육성팀)</b><br>
                <a href="tel:010-1234-5678" style="color:#007AFF; text-decoration:none; font-weight:700;">010-1234-5678</a>
            </p>
        </div>
        """, unsafe_allow_html=True)

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

