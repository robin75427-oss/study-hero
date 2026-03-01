import streamlit as st
import pandas as pd
import time
import requests
from io import StringIO

# 1. 설정 (본인의 ID와 URL이 맞는지 눈으로 한 번 더 확인!)
SHEET_ID = '1ixGEspMFYDK84_DDiPtbdPInKAOO6pImbuzm93xF_48'
SAVE_URL = 'https://script.google.com/macros/s/AKfycbw1BokrHiAQ2HFYXiSaGY48WSP4HXi1vIYh71zV9SM2j4U2Ttu8Bf0XA2SDZVYYz8Eohw/exec'

st.title("🔍 시스템 오류 진단 모드")

# --- 진단용 저장 함수 ---
def debug_save(user_id, seconds):
    st.info(f"데이터 전송 시도: ID={user_id}, 시간={seconds}")
    params = {"user_id": user_id, "seconds": seconds}
    
    try:
        # 10초 동안 응답 기다림, 리다이렉션 허용
        response = requests.get(SAVE_URL, params=params, timeout=10, allow_redirects=True)
        
        # 진단 결과 출력
        st.write(f"📡 응답 코드: {response.status_code}") # 200이면 정상
        st.write(f"📝 서버 응답 내용: {response.text}")
        
        if "Success" in response.text or response.status_code == 200:
            return True
        else:
            st.error("서버에는 도달했으나 'Success' 메시지를 받지 못했습니다.")
            return False
            
    except Exception as e:
        st.error(f"❌ 네트워크 오류 발생: {str(e)}")
        return False

# --- 최소한의 실행 구조 ---
if 'user_id' not in st.session_state:
    user = st.text_input("진단용 닉네임 입력 (시트 A2에 있는 이름)")
    if st.button("입장"):
        st.session_state.user_id = user
        st.rerun()
    st.stop()

st.subheader(f"접속자: {st.session_state.user_id}")

# 테스트용 저장 버튼
test_seconds = time.time() % 1000 # 랜덤한 숫자 생성
if st.button("🚀 지금 즉시 시트로 전송 테스트"):
    with st.spinner('통신 중...'):
        result = debug_save(st.session_state.user_id, test_seconds)
    
    if result:
        st.success("✅ 시트에 데이터가 찍혔을 것입니다! 확인해보세요.")
    else:
        st.error("❌ 저장 실패. 위 진단 내용을 확인하세요.")

st.divider()
st.write("💡 **확인 방법:** 위 버튼을 눌렀을 때 '응답 코드: 200'이 뜨는지, 아니면 에러 메시지가 뜨는지 확인해서 알려주세요.")
