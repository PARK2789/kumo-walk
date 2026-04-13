import streamlit as st
import pandas as pd
# 1. 설정 및 디자인 (iOS 감성)
st.set_page_config(page_title="CEO 소통 산책", page_icon="🍏", layout="centered")
st.markdown("<style>.stApp { background-color: #F2F2F7; } .ios-card { background-color: white; padding: 25px; border-radius: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 20px; border: 1px solid #E5E5EA; } .stButton>button { width: 100%; border-radius: 15px; background-color: #007AFF; color: white; font-weight: 600; border: none; height: 3.8em; }</style>", unsafe_allow_html=True)
# 2. 메인 타이틀
st.title("CEO 소통 산책")
st.markdown("<p style='color: #8E8E93; font-size: 18px;'>함께 걷는 길, 더 큰 미래</p>", unsafe_allow_html=True)
# 3. 행사 요약 카드 (들여쓰기 없음)
st.markdown('<div class="ios-card"><p style="color:#007AFF; font-weight:bold; margin:0;">Schedule</p><h2 style="margin:5px 0;">2026. 04. 20 (월) 14:00</h2><p style="color:#8E8E93; margin:0;">금오산 도립공원 잔디광장 집결</p></div>', unsafe_allow_html=True)
# 4. 지도 (Activity 장소 표시)
st.markdown("#### 🗺️ 미션 지점 안내")
map_data = pd.DataFrame({'lat': [36.1085, 36.1105, 36.1135], 'lon': [128.3185, 128.3205, 128.3235]})
st.map(map_data, zoom=14)
# 5. 액티비티 상세 (Expander 대신 가독성 좋은 텍스트 카드 사용)
st.markdown("#### 🚩 액티비티 가이드")
st.success("**⚽ 미션 1 (배꼽마당):** 미니 골든벨 슈팅! 5회 성공 시 완료")
st.warning("**🎴 미션 2 (하트평상):** 추억의 딱지치기 조별 대항전")
st.info("**🍴 석식 장소:** 느티나무 백숙 (구미시 금오산상가길 89-12)")
# 6. 조원 명단 확인 (가장 안전한 버튼 방식)
st.divider()
st.markdown("#### 👥 조별 진행 인원 확인")
show_group = st.selectbox("확인하고 싶은 조를 선택하세요", ["선택하세요", "1조", "2조", "3조"])
# 선택에 따른 명단 표시 (들여쓰기 최소화)
if show_group == "1조":
st.write("👤 박성식(조장), 김대리, 이과장, 최사원")
if show_group == "2조":
st.write("👤 홍길동(조장), 박지민, 이윤지, 정본부")
if show_group == "3조":
st.write("👤 강호동(조장), 유재석, 신사임당, 이순신")
# 7. 카카오맵 버튼
st.divider()
if st.button("📍 식당 카카오맵 길찾기"):
st.markdown("[지도로 이동하려면 여기를 클릭하세요](https://map.kakao.com/link/search/구미느티나무백숙)")
st.caption("© 2026 LG Way Leadership Development")
