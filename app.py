import streamlit as st
from datetime import datetime

# 1. 페이지 설정 (가장 먼저 와야 함)
st.set_page_config(page_title="갓생 레이스", layout="centered")

# 2. 에러 방지를 위해 디자인 코드를 조금 더 단순화해서 적용
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    div.stButton > button { 
        width: 100%; 
        height: 3.5em; 
        border-radius: 15px; 
        background-color: #5352ed; 
        color: white; 
        font-weight: bold; 
    }
    </style>
    """, unsafe_allow_all_html=True)

st.title("🔥 갓생 추격 레이스")

# 3. 과학고 고스트 계산 (08:00 시작, 10시간 목표)
now = datetime.now()
start_time = now.replace(hour=8, minute=0, second=0, microsecond=0)
passed = (now - start_time).total_seconds()
passed = max(0, passed)
# 과학고는 16시간 활동 중 10시간 공부한다고 가정 (비율 0.625)
ghost_time = min(passed * 0.625, 10 * 3600)

# 4. 내 공부 데이터 (세션 저장용)
if 'sec' not in st.session_state:
    st.session_state.sec = 0.0
if 'run' not in st.session_state:
    st.session_state.run = False

# 5. 화면 표시
st.subheader("🚀 과학고 고스트 페이스")
st.progress(min(ghost_time / 36000, 1.0))
st.write(f"현재 {ghost_time/3600:.1f}시간 지점 돌파 중")

st.divider()

st.subheader("👤 나의 실시간 기록")
st.progress(min(st.session_state.sec / 36000, 1.0))
st.write(f"현재 {st.session_state.sec/3600:.1f}시간 공부 완료")

# 6. 버튼 제어
btn_label = "⏸️ 일시 정지" if st.session_state.run else "▶️ 공부 시작"
if st.button(btn_label):
    st.session_state.run = not st.session_state.run

# 클릭 시마다 시간 추가 (테스트용 15분 추가)
if st.session_state.run:
    st.session_state.sec += 900
    st.toast("기록이 추가되었습니다! 화면을 새로고침(F5) 하세요.")
