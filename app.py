import streamlit as st
import pandas as pd
import time
import requests
from io import StringIO
from datetime import datetime

# 1. 설정 (보내주신 최신 URL 적용 완료)
SHEET_ID = '1ixGEspMFYDK84_DDiPtbdPInKAOO6pImbuzm93xF_48'
SAVE_URL = 'https://script.google.com/macros/s/AKfycbydhMNDRRarWca7CTzugOkfS3p9OvZLT4pPMqzJHlsrXctJ8_5JvNdAD7eXq5VoMfjJ/exec'
READ_URL = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv'

st.set_page_config(page_title="갓생 레이스", layout="centered")

# 시간 표시 형식 변환 함수
def format_time(seconds):
    try: s = float(seconds)
    except: s = 0.0
    h, m, sec = int(s // 3600), int((s % 3600) // 60), int(s % 60)
    return f"{h:02d}:{m:02d}:{sec:02d}"

# --- 1. 로그인 시스템 ---
if 'user_id' not in st.session_state:
    st.title("🔐 공부방 입장")
    user = st.text_input("닉네임을 입력하세요 (시트 A2에 있는 이름)")
    if st.button("입장하기"):
        if user:
            st.session_state.user_id = user.strip()
            st.rerun()
    st.stop()

# --- 2. 데이터 불러오기 함수 ---
def get_db_seconds(user_id):
    try:
        res = requests.get(f"{READ_URL}&cachebust={time.time()}", timeout=5)
        df = pd.read_csv(StringIO(res.text))
        df.columns = ['user_id', 'seconds'] + list(df.columns[2:])
        user_row = df[df['user_id'].astype(str).str.strip() == str(user_id)]
        if not user_row.empty:
            return float(user_row['seconds'].values[0])
    except: pass
    return 0.0

# --- 3. 세션 초기화 (변수 생성 순서 고정) ---
if 'is_running' not in st.session_state:
    st.session_state.is_running = False
if 'total_seconds' not in st.session_state:
    st.session_state.total_seconds = get_db_seconds(st.session_state.user_id)

# --- 4. 타이머 계산 ---
display_secs = float(st.session_state.total_seconds)
if st.session_state.is_running:
    if 'start_stamp' not in st.session_state:
        st.session_state.start_stamp = time.time()
    display_secs += (time.time() - st.session_state.start_stamp)

# --- 5. 화면 표시 ---
st.title(f"🔥 {st.session_state.user_id}의 레이스")
st.header(f"⏱️ {format_time(display_secs)}")

# 버튼 제어
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
            
            # 구글 시트 저장 시도 (성공 여부 확인)
            with st.spinner('시트에 저장 중...'):
                try:
                    params = {"user_id": st.session_state.user_id, "seconds": final_secs}
                    response = requests.get(SAVE_URL, params=params, timeout=10, allow_redirects=True)
                    if response.status_code == 200:
                        st.session_state.total_seconds = final_secs
                        st.session_state.is_running = False
                        st.success("✅ 저장 성공!")
                        time.sleep(1)
                        st.rerun()
                except:
                    st.error("저장 중 통신 오류가 발생했습니다.")

with c2:
    if st.button("🔄 동기화", use_container_width=True):
        st.session_state.total_seconds = get_db_seconds(st.session_state.user_id)
        st.rerun()

# 실시간 업데이트
if st.session_state.is_running:
    time.sleep(1)
    st.rerun()
