import streamlit as st
import pandas as pd
from datetime import datetime
import time
import requests

# 1. 설정 (사용자 정보 및 구글 연동)
SHEET_ID = '1ixGEspMFYDK84_DDiPtbdPInKAOO6pImbuzm93xF_48'
SAVE_URL = 'https://script.google.com/macros/s/AKfycbw1BokrHiAQ2HFYXiSaGY48WSP4HXi1vIYh71zV9SM2j4U2Ttu8Bf0XA2SDZVYYz8Eohw/exec'
READ_URL = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv'

st.set_page_config(page_title="갓생 레이스 (저장소 연동)", layout="centered")

def format_time(seconds):
    h, m, s = int(seconds // 3600), int((seconds % 3600) // 60), int(seconds % 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

# --- 1. 로그인 시스템 ---
if 'user_id' not in st.session_state:
    st.title("🔐 공부방 입장")
    user = st.text_input("닉네임을 입력하세요 (예: 나, 룸메)")
    if st.button("입장하기"):
        if user:
            st.session_state.user_id = user
            st.rerun()
        else:
            st.warning("닉네임을 입력해야 합니다!")
    st.stop()

# --- 2. 데이터 불러오기 (구글 시트 연동) ---
@st.cache_data(ttl=5) # 5초마다 데이터 갱신 허용
def get_db_seconds(user_id):
    try:
        df = pd.read_csv(READ_URL)
        user_row = df[df['user_id'] == user_id]
        if not user_row.empty:
            return float(user_row['seconds'].values[0])
    except:
        pass
    return 0.0

# --- 3. 세션 초기화 ---
if 'total_seconds' not in st.session_state:
    st.session_state.total_seconds = get_db_seconds(st.session_state.user_id)
if 'is_running' not in st.session_state:
    st.session_state.is_running = False

# --- 4. 타이머 로직 ---
display_secs = st.session_state.total_seconds
if st.session_state.is_running:
    if 'start_stamp' not in st.session_state:
        st.session_state.start_stamp = time.time()
    elapsed = time.time() - st.session_state.start_stamp
    display_secs += elapsed

# --- 5. 화면 표시 ---
st.title(f"🔥 {st.session_state.user_id}의 갓생 레이스")
st.header(f"⏱️ {format_time(display_secs)}")

# 고스트 계산 (08:00 기준)
now = datetime.now()
ghost_passed = max(0, (now - now.replace(hour=8, minute=0, second=0, microsecond=0)).total_seconds())
ghost_secs = min(ghost_passed * 0.625, 36000)
st.write(f"🚀 과학고 페이스: {format_time(ghost_secs)}")
st.progress(min(display_secs / 36000, 1.0))

# --- 6. 제어 버튼 (핵심: 저장 기능) ---
c1, c2 = st.columns(2)
with c1:
    if not st.session_state.is_running:
        if st.button("▶️ 시작", use_container_width=True):
            # 시작할 때 최신 데이터를 다시 한번 불러옴 (동기화)
            st.session_state.total_seconds = get_db_seconds(st.session_state.user_id)
            st.session_state.start_stamp = time.time()
            st.session_state.is_running = True
            st.rerun()
    else:
        if st.button("⏸️ 일시 정지 & 저장", use_container_width=True):
            # 현재까지 흐른 시간 계산
            final_secs = st.session_state.total_seconds + (time.time() - st.session_state.start_stamp)
            # 구글 시트에 즉시 전송
            try:
                requests.get(f"{SAVE_URL}?user_id={st.session_state.user_id}&seconds={final_secs}")
                st.session_state.total_seconds = final_secs
                st.session_state.is_running = False
                st.success("기록이 안전하게 저장되었습니다!")
                st.rerun()
            except:
                st.error("저장 중 오류가 발생했습니다. 네트워크를 확인하세요.")

with c2:
    if st.button("🚪 로그아웃", use_container_width=True):
        del st.session_state.user_id
        st.rerun()

# 1초마다 화면 갱신
if st.session_state.is_running:
    time.sleep(1)
    st.rerun()
