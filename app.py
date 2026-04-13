import streamlit as st
import pandas as pd
# 1. 설정 및 디자인
st.set_page_config(page_title="CEO 소통 산책", layout="centered")
# CSS 스타일 (들여쓰기 없이 한 줄로 처리)
st.markdown("<style>.stApp { background-color: #F2F2F7; } .ios-card { background-color: white; padding: 20px; border-radius: 18px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); margin-bottom: 15px; border: 0.5px solid #E5E5EA; }</style>", unsafe_allow_html=True)
# 2. 메인 타이틀
st.title("🏃‍♂️ CEO 소통 산책")
st.markdown("### 금오산 올레길 코스 가이드")
# 3. 요약 정보 카드
st.markdown('<div class="ios-card"><b>📅 일시:</b> 2026. 04. 20 (월) 14:00<br><b>📍 집결:</b> 금오산 잔디광장</div>', unsafe_allow_html=True)
# 4. 지도 표시
st.markdown("#### 🗺️ 미션 포인트")
# 지도 데이터 생성
map_df = pd.DataFrame({'lat': [36.1083, 36.1105, 36.1130], 'lon': [128.3180, 128.3208, 128.3225]})
st.map(map_df, zoom=14)
# 5. 조별 명단 (들여쓰기 없는 단순 텍스트)
st.divider()
st.markdown("#### 👥 조원 명단 확인")
st.info("1조: 박성식(조장), 김철수, 이영희, 최미나\n\n2조: 홍길동(조장), 박지민, 이윤지, 정본부")
# 6. 미션 상세
st.divider()
st.markdown("#### 🚩 미션 안내")
st.warning("⚽ 미션 1 (배꼽마당): 미니 골대에 공 차 넣기 (5회 성공)")
st.success("🎴 미션 2 (하트평상): 추억의 딱지치기 조별 대항전")
# 7. 식당 정보
st.divider()
st.markdown("#### 🍴 석식 장소: 느티나무 백숙")
st.write("주소: 구미시 금오산상가길 89-12")
st.markdown("[🔗 카카오맵 길찾기 링크](https://map.kakao.com/link/search/구미느티나무백숙)")
st.caption("© 2026 LG Way Leadership Development")
