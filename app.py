import streamlit as st
import pandas as pd
from datetime import datetime
import time
import requests

# 1. 구글 시트 설정 (본인의 시트 ID를 입력하세요)
SHEET_ID = '1ixGEspMFYDK84_DDiPtbdPInKAOO6pImbuzm93xF_48'
# 데이터를 읽어오기 위한 URL
READ_URL = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv'
# 데이터를 저장하기 위한 앱스 스크립트 (나중에 연결 가능, 일단 읽기 위주)

st.set_page_config(page_title="절대 안지워지는 타이머")

def format_time(seconds):
    h, m, s = int(seconds // 3600), int((seconds % 3600) // 60), int(seconds % 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

# --- 로그인 세션 ---
if 'user_id' not in st.session_state:
    st.title("🔐 닉네임 접속")
    user = st.text_input("닉네임을 입력하세요 (예: 나, 룸메)")
    if st.button("내 기록 불러오기"):
        st.session_state.user_id = user
        st.rerun()
    st.stop()

# --- 데이터 로딩 (구글 시트 연동) ---
@st.cache_data(ttl=10) # 10초마다 시트 데이터 새로고침
def load_data():
    try:
        df = pd.read_csv(READ_URL)
        return df
    except:
        return pd.DataFrame(columns=['user_id', 'seconds'])

df = load_data()
user_row = df[df['user_id'] == st.session_state.user_id]
initial_seconds = float(user_row['seconds'].values[0]) if not user_row.empty else 0.0

# --- 타이머 상태 관리 ---
if 'total_seconds' not in st.session_state:
    st.session_state.total_seconds = initial_seconds
if 'is_running' not in st.session_state:
    st.session_state.is_running = False

st.title(f"🔥 {st.session_state.user_id}의 갓생 레이스")

# 현재 흐르는 시간 계산
display_secs = st.session_state.total_seconds
if st.session_state.is_running:
    if 'start_stamp' not in st.session_state: st.session_state.start_stamp = time.time()
    display_secs += (time.time() - st.session_state.start_stamp)

# 화면 표시
c1, c2 = st.columns(2)
c1.metric("🚀 과학고 페이스", "진행중..")
c2.metric("⏱️ 내 공부량", format_time(display_secs))

# 제어 버튼
if not st.session_state.is_running:
    if st.button("▶️ 공부 시작", use_container_width=True):
        st.session_state.start_stamp = time.time()
        st.session_state.is_running = True
        st.rerun()
else:
    if st.button("⏸️ 일시 정지 및 저장", use_container_width=True):
        st.session_state.total_seconds += (time.time() - st.session_state.start_stamp)
        st.session_state.is_running = False
        # [중요] 여기에 나중에 저장 API를 넣으면 완벽합니다.
        st.success(f"현재 기록: {format_time(st.session_state.total_seconds)}")
        st.rerun()

if st.session_state.is_running:
    time.sleep(1)
    st.rerun()
