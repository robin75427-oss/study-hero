import streamlit as st
from datetime import datetime
import time

# 1. 페이지 설정
st.set_page_config(page_title="과학고 추격기", layout="centered")

def format_time(seconds):
    h, m, s = int(seconds // 3600), int((seconds % 3600) // 60), int(seconds % 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

st.title("🔥 절대 멈추지 않는 타이머")

# --- 핵심 로직: 폰이 꺼져도 유지되는 계산법 ---
if 'total_seconds' not in st.session_state:
    st.session_state.total_seconds = 0.0  # 이전에 저장된 누적 시간
if 'is_running' not in st.session_state:
    st.session_state.is_running = False
if 'start_time_stamp' not in st.session_state:
    st.session_state.start_time_stamp = None

# 현재 시점의 공부 시간 계산
if st.session_state.is_running:
    # (현재 시간 - 시작 버튼 누른 시각)을 계산하므로 폰이 꺼져도 상관없음
    elapsed_now = time.time() - st.session_state.start_time_stamp
    current_my_secs = st.session_state.total_seconds + elapsed_now
else:
    current_my_secs = st.session_state.total_seconds

# 과학고 고스트 계산 (08:00 기준)
now = datetime.now()
ghost_passed = max(0, (now - now.replace(hour=8, minute=0, second=0, microsecond=0)).total_seconds())
ghost_secs = min(ghost_passed * 0.625, 36000)

# --- 화면 표시 ---
c1, c2 = st.columns(2)
c1.metric("🚀 과학고 고스트", format_time(ghost_secs))
c2.metric("⏱️ 나의 공부 시간", format_time(current_my_secs))

# --- 제어 버튼 ---
st.divider()
if not st.session_state.is_running:
    if st.button("▶️ 공부 시작 (폰 꺼져도 기록됨)", use_container_width=True):
        # 시작하는 순간의 '절대 시각'을 기록
        st.session_state.start_time_stamp = time.time()
        st.session_state.is_running = True
        st.rerun()
else:
    if st.button("⏸️ 일시 정지 & 저장", use_container_width=True):
        # 정지하는 순간 지금까지 흐른 시간을 누적 시간에 합산
        st.session_state.total_seconds += (time.time() - st.session_state.start_time_stamp)
        st.session_state.is_running = False
        st.rerun()

if st.button("🔄 리셋"):
    st.session_state.total_seconds = 0.0
    st.session_state.is_running = False
    st.rerun()

# 1초마다 화면 갱신 (화면이 켜져있을 때만 째깍거림)
if st.session_state.is_running:
    time.sleep(1)
    st.rerun()
