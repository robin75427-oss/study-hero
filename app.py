import streamlit as st
import pandas as pd
from datetime import datetime
import time
import requests
from io import StringIO

# 1. 설정
SHEET_ID = '1ixGEspMFYDK84_DDiPtbdPInKAOO6pImbuzm93xF_48'
SAVE_URL = 'https://script.google.com/macros/s/AKfycbw1BokrHiAQ2HFYXiSaGY48WSP4HXi1vIYh71zV9SM2j4U2Ttu8Bf0XA2SDZVYYz8Eohw/exec'
READ_URL = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv'

st.set_page_config(page_title="갓생 레이스", layout="centered")

def format_time(seconds):
    try: s = float(seconds)
    except: s = 0.0
    h, m, sec = int(s // 3600), int((s % 3600) // 60), int(s % 60)
    return f"{h:02d}:{m:02d}:{sec:02d}"

# --- 1. 로그인 시스템 (가장 먼저 실행) ---
if 'user_id' not in st.session_state:
    st.title("🔐 공부방 입장")
    user = st.text_input("닉네임을 입력하세요 (예: 나)")
    if st.button("입장하기"):
        if user:
            st.session_state.user_id = user
            st.rerun()
    st.stop()

# --- 2. 데이터 불러오기 함수 ---
def get_db_seconds(user_id):
    try:
        res = requests.get(f"{READ_URL}&cachebust={time.time()}", timeout=5)
        df = pd.read_csv(StringIO(res.text))
        df.columns = ['user_id', 'seconds'] + list(df.columns[2:])
        user_row = df[df['user_id'].astype(str).str.strip() == str(user_id).strip()]
        if not user_row.empty:
            return float(user_row['seconds'].values[0])
    except: pass
    return 0.0

# --- 3. [중요] 변수 초기화 (에러 방지 핵심) ---
if 'is_running' not in st.session_state:
    st.session_state.is_running = False
if 'total_seconds' not in st.session_state:
    st.session_state.total_seconds = get_db_seconds(st.session_state.user_id)

# --- 4. 타이머 계산 (변수가 생성된 후 실행) ---
display_secs = float(st.session_state.total_seconds)
if st.session_state.is_running:
    if 'start_stamp' not in st.session_state:
        st.session_state.start_stamp = time.time()
    display_secs += (time.time() - st.session_state.start_stamp)

# --- 5. 화면 표시 및 제어 ---
st.title(f"🔥 {st.session_state.user_id}의 레이스")
st.header(f"⏱️ {format_time(display_secs)}")

c1, c2 = st.columns(2)
with c1:
    if not st.session_state.is_running:
        if st.button("▶️ 시작", use_container_width=True):
            st.session_state.start_stamp = time.time()
            st.session_state.is_running = True
            st.rerun()
    else:
        if st.button("⏸️ 정지 및 저장", use_container_width=True):
            final_secs = st.session_state.total_seconds + (time.time() - st.session_state.start_stamp)
            # 구글 시트 저장
            try: requests.get(f"{SAVE_URL}?user_id={st.session_state.user_id}&seconds={final_secs}", timeout=5)
            except: pass
            st.session_state.total_seconds = final_secs
            st.session_state.is_running = False
            st.success("저장 시도 완료!")
            st.rerun()

with c2:
    if st.button("🔄 동기화", use_container_width=True):
        st.session_state.total_seconds = get_db_seconds(st.session_state.user_id)
        st.rerun()

if st.session_state.is_running:
    time.sleep(1)
    st.rerun()
