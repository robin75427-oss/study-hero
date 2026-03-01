import streamlit as st
import pandas as pd
from datetime import datetime
import time
import requests

# 1. 설정
SHEET_ID = '1ixGEspMFYDK84_DDiPtbdPInKAOO6pImbuzm93xF_48'
SAVE_URL = 'https://script.google.com/macros/s/AKfycbw1BokrHiAQ2HFYXiSaGY48WSP4HXi1vIYh71zV9SM2j4U2Ttu8Bf0XA2SDZVYYz8Eohw/exec'
# 캐시 방지를 위해 URL에 랜덤 값을 붙임
READ_URL = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv'

st.set_page_config(page_title="갓생 레이스", layout="centered")

def format_time(seconds):
    try:
        # seconds가 숫자인지 확인하고 아니면 0으로 처리
        secs = float(seconds) if seconds is not None else 0.0
    except:
        secs = 0.0
    h, m, s = int(secs // 3600), int((secs % 3600) // 60), int(secs % 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

# --- 1. 로그인 시스템 ---
if 'user_id' not in st.session_state:
    st.title("🔐 공부방 입장")
    user = st.text_input("닉네임을 입력하세요 (예: 나)")
    if st.button("입장하기"):
        if user:
            st.session_state.user_id = user
            st.rerun()
    st.stop()

# --- 2. 데이터 불러오기 ---
def get_db_seconds(user_id):
    try:
        # 구글 시트 캐시를 피하기 위해 시간 파라미터 추가
        res = requests.get(f"{READ_URL}&cachebust={time.time()}")
        from io import StringIO
        df = pd.read_csv(StringIO(res.text))
        
        user_row = df[df['user_id'].astype(str) == str(user_id)]
        if not user_row.empty:
            val = user_row['seconds'].values[0]
            return float(val) if pd.notna(val) else 0.0
    except:
        pass
    return 0.0

# --- 3. 세션 초기화 ---
if 'total_seconds' not in st.session_state:
    st.session_state.total_seconds = get_db_seconds(st.session_state.user_id)
if 'is_running' not in st.session_state:
    st.session_state.is_running = False

# --- 4. 타이머 계산 ---
current_secs = float(st.session_state.total_seconds)
if st.session_state.is_running:
    if 'start_stamp' not in st.session_state:
        st.session_state.start_stamp = time.time()
    current_secs += (time.time() - st.session_state.start_stamp)

# --- 5. 화면 표시 ---
st.title(f"🔥 {st.session_state.user_id}의 레이스")
st.header(f"⏱️ {format_time(current_secs)}")

# 제어 버튼
c1, c2 = st.columns(2)
with c1:
    if not st.session_state.is_running:
        if st.button("▶️ 시작", use_container_width=True):
            st.session_state.total_seconds = get_db_seconds(st.session_state.user_id)
            st.session_state.start_stamp = time.time()
            st.session_state.is_running = True
            st.rerun()
    else:
        if st.button("⏸️ 정지 및 저장", use_container_width=True):
            final_secs = st.session_state.total_seconds + (time.time() - st.session_state.start_stamp)
            # 저장 요청
            requests.get(f"{SAVE_URL}?user_id={st.session_state.user_id}&seconds={final_secs}")
            st.session_state.total_seconds = final_secs
            st.session_state.is_running = False
            st.success("저장 완료!")
            st.rerun()

with c2:
    if st.button("🔄 새로고침", use_container_width=True):
        st.session_state.total_seconds = get_db_seconds(st.session_state.user_id)
        st.rerun()

if st.session_state.is_running:
    time.sleep(1)
    st.rerun()
