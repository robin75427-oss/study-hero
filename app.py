import streamlit as st
from datetime import datetime
import time

# 1. 페이지 설정
st.set_page_config(page_title="과학고 추격기", layout="centered")

# 2. 시간을 시:분:초 형식으로 변환하는 함수
def format_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

st.title("🔥 과학고 벤치마킹 스톱워치")

# 3. 고스트(과학고) 시간 계산
now = datetime.now()
start_time = now.replace(hour=8, minute=0, second=0, microsecond=0)
passed_seconds = max(0, (now - start_time).total_seconds())
# 과학고는 16시간 중 10시간 공부(초당 약 0.1736초 누적)
ghost_current_seconds = min(passed_seconds * 0.625, 10 * 3600)

# 4. 타이머 상태 관리
if 'start_time_stamp' not in st.session_state:
    st.session_state.start_time_stamp = None
if 'total_seconds' not in st.session_state:
    st.session_state.total_seconds = 0.0
if 'is_running' not in st.session_state:
    st.session_state.is_running = False

# 실행 중일 때 현재 흐른 시간 계산
if st.session_state.is_running:
    current_elapsed = time.time() - st.session_state.start_time_stamp
    my_current_seconds = st.session_state.total_seconds + current_elapsed
else:
    my_current_seconds = st.session_state.total_seconds

# 5. 화면 표시 (시:분:초 레이아웃)
st.write("---")
col_g, col_m = st.columns(2)

with col_g:
    st.metric("🚀 과학고 페이스", format_time(ghost_current_seconds))
    st.progress(min(ghost_current_seconds / 36000, 1.0))

with col_m:
    st.metric("⏱️ 나의 공부 시간", format_time(my_current_seconds))
    st.progress(min(my_current_seconds / 36000, 1.0))

# 6. 제어 버튼
st.write("---")
c1, c2 = st.columns(2)

with c1:
    if not st.session_state.is_running:
        if st.button("▶️ 공부 시작", use_container_width=True):
            st.session_state.start_time_stamp = time.time()
            st.session_state.is_running = True
            st.rerun()
    else:
        if st.button("⏸️ 일시 정지", use_container_width=True):
            st.session_state.total_seconds += time.time() - st.session_state.start_time_stamp
            st.session_state.is_running = False
            st.rerun()

with c2:
    if st.button("🔄 리셋", use_container_width=True):
        st.session_state.total_seconds = 0.0
        st.session_state.is_running = False
        st.session_state.start_time_stamp = None
        st.rerun()

# 7. 실시간 업데이트 (1초마다 새로고침)
if st.session_state.is_running:
    time.sleep(1)
    st.rerun()

# 8. 격차 분석
gap = ghost_current_seconds - my_current_seconds
if gap > 0:
    st.warning(f"⚠️ 과학고 학생보다 **{format_time(gap)}** 뒤처져 있습니다!")
else:
    st.success(f"✅ 과학고 학생보다 **{format_time(abs(gap))}** 앞서고 있습니다!")
