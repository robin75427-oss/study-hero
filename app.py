import streamlit as st
import pandas as pd
import time
import requests
from io import StringIO

# 1. 설정 (보내주신 최종 URL 적용)
SHEET_ID = '1ixGEspMFYDK84_DDiPtbdPInKAOO6pImbuzm93xF_48'
SAVE_URL = 'https://script.google.com/macros/s/AKfycbw_sxh3L0AujjUuMELS1njvOtenY2olu_Wqhw_Wjxggt2O7zitg-E-cbW7rRFdbunQ7nA/exec'
READ_URL = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv'

st.set_page_config(page_title="갓생 레이스", layout="centered")

def format_time(seconds):
    try: s = float(seconds)
    except: s = 0.0
    h, m, sec = int(s // 3600), int((s % 3600) // 60), int(s % 60)
    return f"{h:02d}:{m:02d}:{sec:02d}"

# --- 1. 로그인 ---
if 'user_id' not in st.session_state:
    st.title("🔐 공부방 입장")
    user = st.text_input("닉네임을 입력하세요 (예: WON)")
    if st.button("입장하기"):
        if user:
            st.session_state.user_id = user.strip()
            st.rerun()
    st.stop()

# --- 2. 데이터 불러오기 ---
def get_db_seconds(user_id):
    try:
        # 캐시 방지를 위해 시간값 추가
        res = requests.get(f"{READ_URL}&t={time.time()}", timeout=10)
        df = pd.read_csv(StringIO(res.text))
        df.columns = ['user_id', 'seconds'] + list(df.columns[2:])
        user_row = df[df['user_id'].astype(str).str.strip() == str(user_id)]
        if not user_row.empty:
            return float(user_row['seconds'].values[0])
    except: pass
    return 0.0

# --- 3. 세션 초기화 ---
if 'is_running' not in st.session_state:
    st.session_state.is_running = False
if 'total_seconds' not in st.session_state:
    st.session_state.total_seconds = get_db_seconds(st.session_state.user_id)

# --- 4. 타이머 로직 ---
display_secs = float(st.session_state.total_seconds)
if st.session_state.is_running:
    if 'start_stamp' not in st.session_state:
        st.session_state.start_stamp = time.time()
    display_secs += (time.time() - st.session_state.start_stamp)

# --- 5. 화면 표시 ---
st.title(f"🔥 {st.session_state.user_id}의 레이스")
st.header(f"⏱️ {format_time(display_secs)}")

# 제어 버튼
c1, c2 = st.columns(2)
with c1:
    if not st.session_state.is_running:
        if st.button("▶️ 시작", use_container_width=True):
            # 시작할 때 시트의 최신 시간을 다시 가져옴 (동기화)
            st.session_state.total_seconds = get_db_seconds(st.session_state.user_id)
            st.session_state.start_stamp = time.time()
            st.session_state.is_running = True
            st.rerun()
    else:
        if st.button("⏸️ 정지 및 저장", use_container_width=True):
            final_secs = st.session_state.total_seconds + (time.time() - st.session_state.start_stamp)
            
            # 구글 시트에 데이터 전송 (성공 여부 상관없이 세션 유지)
            try:
                # 403 에러 방지를 위한 파라미터 구조
                requests.get(f"{SAVE_URL}?user_id={st.session_state.user_id}&seconds={final_secs}", timeout=10)
                st.success("시트에 기록되었습니다!")
            except:
                st.warning("네트워크 불안정으로 시트 저장은 실패했으나, 앱 내에는 기록되었습니다.")
            
            st.session_state.total_seconds = final_secs
            st.session_state.is_running = False
            time.sleep(1)
            st.rerun()

with c2:
    if st.button("🔄 동기화", use_container_width=True):
        st.session_state.total_seconds = get_db_seconds(st.session_state.user_id)
        st.rerun()

if st.session_state.is_running:
    time.sleep(1)
    st.rerun()
