import streamlit as st
from datetime import datetime

# 1. 페이지 설정 (가장 상단에 위치해야 함)
st.set_page_config(page_title="갓생 레이스", layout="centered")

# 2. 에러 방지를 위해 스타일 코드를 최대한 간결하게 수정
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: white; }
    div.stButton > button { 
        width: 100%; 
        height: 3em; 
        border-radius: 15px; 
        background-color: #5352ed; 
        color: white; 
        font-weight: bold;
        border: none;
    }
</style>
""", unsafe_allow_all_html=True)

st.title("🔥 갓생 추격 레이스")

# 3. 과학고 고스트 계산 (08:00 시작, 10시간 목표)
now = datetime.now()
start_time = now.replace(hour=8, minute=0, second=0, microsecond=0)
passed_seconds = (now - start_time).total_seconds()
passed_seconds = max(0, passed_seconds)

# 과학고는 하루 16시간 중 10시간 공부한다고 가정 (비율 0.625)
ghost_time_secs = min(passed_seconds * 0.625, 10 * 3600)

# 4. 내 공부 데이터 (세션 저장용)
if 'sec' not in st.session_state:
    st.session_state.sec = 0.0
if 'run' not in st.session_state:
    st.session_state.run = False

# 5. 화면 표시
st.subheader("🚀 과학고 고스트 페이스")
st.progress(min(ghost_time_secs / 36000, 1.0))
st.write(f"현재 {ghost_time_secs/3600:.1f}시간 지점 통과 중")

st.divider()

st.subheader("👤 나의 실시간 기록")
st.progress(min(st.session_state.sec / 36000, 1.0))
st.write(f"현재 {st.session_state.sec/3600:.1f}시간 공부 완료")

# 6. 버튼 제어
label = "⏸️ 일시 정지" if st.session_state.run else "▶️ 공부 시작"
if st.button(label):
    st.session_state.run = not st.session_state.run

# 작동 확인을 위해 버튼 누를 때마다 15분씩 추가되도록 설정
if st.session_state.run:
    st.session_state.sec += 900
    st.toast("시간이 업데이트되었습니다! 화면을 새로고침하세요.")
