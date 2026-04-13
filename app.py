import streamlit as st
import pandas as pd
# 페이지 설정
st.set_page_config(page_title="CEO 소통행사 안내", layout="wide")
# 1. 메인 섹션
st.title("🏃‍♂️ CEO와 함께하는 금오산 소통 산책")
st.subheader("'함께 걷는 길, 더 큰 미래'")
col1, col2 = st.columns(2)
with col1:
   # 이 부분이 들여쓰기가 되어 있어야 합니다.
   st.info("📅 **일시:** 2026년 4월 ○○일(월)\n\n📍 **장소:** 금오산 도립공원 및 올레길")
with col2:
   # 이 부분도 마찬가지입니다.
   st.success("👥 **대상:** 전 임직원 (조별 진행)")
st.divider()
# 2. 시간대별 행사 내용 (Timeline)
st.markdown("### ⏰ 행사 일정")
schedule = {
   "시간": ["14:00 - 14:30", "14:30 - 16:30", "16:30 - 18:30"],
   "내용": ["잔디광장 집결 및 조 편성", "올레길 산책 및 Activity 수행", "석식 및 소통의 시간"]
}
st.table(pd.DataFrame(schedule))
st.divider()
# 3. 전체 산책 코스 안내
st.markdown("### 🗺️ 전체 산책 코스")
st.markdown("""
**[이동 경로]**
잔디광장(출발) ➡️ 올레길 입구(좌측 방향) ➡️ 부작교 ➡️ 뚝방길 ➡️ 느티나무 백숙(도착)
""")
# 4. 인터랙티브 Activity & 장소 안내
st.markdown("### 🚩 주요 지점 (탭을 클릭하세요)")
tab1, tab2, tab3 = st.tabs(["📍 Activity 1", "📍 Activity 2", "🍴 석식 장소"])
with tab1:
   st.markdown("#### [배꼽마당] 슈팅! 미니 골든벨")
   st.write("⚽ **게임 방법:** 조원들이 차례대로 미니 골대에 공을 차 넣습니다.")
   st.write("🎯 **성공 조건:** 정해진 횟수 이상 골인 시 미션 성공!")
   if st.button("배꼽마당 위치 확인"):
       st.info("금오산 올레길 초입 부근 배꼽마당 광장으로 오세요.")
with tab2:
   st.markdown("#### [뚝방길 하트평상] 추억의 딱지치기")
   st.write("🎴 **게임 방법:** 종이 딱지로 상대방의 딱지를 넘기는 게임입니다.")
   st.write("💪 **성공 조건:** 조 대항 승리 또는 미션 개수 달성!")
   if st.button("하트평상 위치 확인"):
       st.info("뚝방길 구간 중간에 위치한 하트 모양 평상을 찾으세요.")
with tab3:
   st.markdown("#### [도착지] 느티나무 백숙")
   st.markdown("**주소:** 경상북도 구미시 금오산상가길 89-12 (남통동)") # 실제 주소 반영 가능
   st.markdown("**메뉴:** 한방백숙, 닭볶음탕 등")
   if st.button("식당 정보 상세 보기"):
       st.success("식당: 느티나무 백숙 / 연락처: 054-452-6126")
# 5. 하단 안내
st.divider()
st.caption("본 웹페이지는 행사 참석자 안내를 위해 제작되었습니다. 문의: 성식님 (인사팀)")
