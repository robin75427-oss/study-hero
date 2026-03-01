import streamlit as st
import pandas as pd
from datetime import datetime
import time
import requests
from io import StringIO

# 1. 설정 (사용자 정보 및 구글 연동)
SHEET_ID = '1ixGEspMFYDK84_DDiPtbdPInKAOO6pImbuzm93xF_48'
SAVE_URL = 'https://script.google.com/macros/s/AKfycbw1BokrHiAQ2HFYXiSaGY48WSP4HXi1vIYh71zV9SM2j4U2Ttu8Bf0XA2SDZVYYz8Eohw/exec'
READ_URL = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv'

# 데이터 저장 함수 (리다이렉션 허용 추가)
def save_to_google(user_id, seconds):
    params = {
        "user_id": user_id,
        "seconds": seconds
    }
    try:
        # allow_redirects=True가 핵심입니다. 구글 서버의 이동 경로를 끝까지 쫓아갑니다.
        response = requests.get(SAVE_URL, params=params, allow_redirects=True, timeout=10)
        return response.text == "Success"
    except Exception as e:
        st.error(f"연결 실패: {e}")
        return False

# (중략: 로그인 및 시간 계산 로직은 동일)

# --- 저장 버튼 동작 부분 ---
if st.session_state.is_running:
    if st.button("⏸️ 일시 정지 및 저장", use_container_width=True):
        # 1. 최종 시간 계산
        final_secs = st.session_state.total_seconds + (time.time() - st.session_state.start_stamp)
        
        # 2. 구글 시트 전송 시도
        with st.spinner('구글 시트에 기록 중...'):
            success = save_to_google(st.session_state.user_id, final_secs)
            
        if success:
            st.session_state.total_seconds = final_secs
            st.session_state.is_running = False
            st.success("✅ 저장 성공!")
            time.sleep(1) # 메시지 볼 시간 확보
            st.rerun()
        else:
            # 저장 실패 시에도 세션엔 반영해서 앱 내에서는 유지되게 함
            st.session_state.total_seconds = final_secs
            st.session_state.is_running = False
            st.warning("⚠️ 시트 저장에 실패했지만 앱에는 기록되었습니다.")
            st.rerun()
