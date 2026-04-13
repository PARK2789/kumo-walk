import streamlit as st
import pandas as pd
# 페이지 설정
st.set_page_config(page_title="CEO 소통 산책", layout="centered")
# CSS 스타일 (iOS 감성)
st.markdown("""
<style>
.stApp { background-color: #F2F2F7; }
.ios-card { background-color: white; padding: 20px; border-radius: 18px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); margin-bottom: 15px; border: 0.5px solid #E5E5EA; }
</style>
""", unsafe_allow_status=True)
# 메인 화면
st.title("🏃‍♂️ CEO 소통 산책")
st.markdown("### 금오산 올레길 코스 가이드")
# 1. 지도 포인트
st.markdown("#### 🗺️ 미션 포인트 안내")
map_data = pd.DataFrame({'lat': [36.1083, 36.1105, 36.1130], 'lon': [128.3180, 128.3208, 128.3225]})
st.map(map_data, zoom=14)
# 2. 조별 명단 (들여쓰기 최소화 구조)
st.divider()
st.markdown("#### 👥 조원 명단 확인")
with st.expander("여기를 눌러 우리 조원을 확인하세요"):
st.write("**1조:** 박성식(조장), 김철수, 이영희, 최미나")
st.write("**2조:** 홍길동(조장), 박지민, 이윤지, 정본부")
# 3. 액티비티 상세
st.divider()
st.markdown("#### 🚩 미션 상세 내용")
col1, col2 = st.columns(2)
with col1:
st.info("**⚽ 미션 1 (배꼽마당)**\n\n미니 골대에 공 차 넣기!")
with col2:
st.success("**🎴 미션 2 (하트평상)**\n\n추억의 딱지치기 대결!")
# 4. 식당 정보
with st.expander("🍴 석식 장소: 느티나무 백숙"):
st.write("주소: 구미시 금오산상가길 89-12")
st.markdown("[🔗 카카오맵 길찾기](https://map.kakao.com/link/search/구미느티나무백숙)")
st.caption("© 2026 LG Way Leadership Development")
