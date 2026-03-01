import streamlit as st
from datetime import datetime

# 아이폰 사파리 최적화 디자인
st.set_page_config(page_title="갓생 레이스", layout="centered")

# 배경색 및 프로그레스 바 스타일
st.markdown("""<style>
    .stApp { background-color: #0e1117; color: white; }
    .stProgress > div > div > div > div { background-image: linear-gradient(to right, #2ed573, #7bed9f); }
    div.stButton > button { width: 100%; height: 3.5em; font-size: 20px; border-radius: 15px; background-color: #5352ed; color: white; border: none; font-weight: bold; }
</style>""", unsafe_allow_all_html=True)

st.title("🔥 갓생 추격 레이스")

# 1. 과학고 고스트 계산 (08:00 시작, 10시간 목표)
now = datetime.now()
start_time = now.replace(hour=8, minute=0, second=0, microsecond=0)
passed = max(0, (now - start_time).total_seconds())
ghost_time = min(passed * 0.625, 10 * 3600)

# 2. 내 공부 데이터 (세션 저장용)
if 'sec' not in st.session_state: st.session_state.sec = 0
if 'run' not in st.session_state: st.session_state.run = False

# 3. 화면 표시
st.subheader("🚀 과학고 고스트 페이스")
st.progress(ghost_time / 36000)
st.write(f"현재 {ghost_time/3600:.1f}시간 지점 돌파 중")

st.divider()

st.subheader("👤 나의 실시간 기록")
st.progress(min(st.session_state.sec / 36000, 1.0))
st.write(f"현재 {st.session_state.sec/3600:.1f}시간 공부 완료")

# 4. 버튼 제어
if st.button(st.session_state.run and "⏸️ 일시 정지" or "▶️ 공부 시작"):
    st.session_state.run = not st.session_state.run

# 실제 작동 느낌을 주기 위한 테스트 로직 (누를 때마다 15분 추가)
if st.session_state.run:
    st.session_state.sec += 900
    st.toast("기록이 추가되었습니다! 화면을 새로고침하면 반영됩니다.")
