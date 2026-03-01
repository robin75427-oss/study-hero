import streamlit as st
from datetime import datetime

# 1. 설정 (가장 위에 필수)
st.set_page_config(page_title="과학고 추격기")

# 2. 제목
st.title("🔥 과학고 벤치마킹 시스템")
st.write("아이폰 홈 화면에 추가해서 실시간으로 확인하세요.")

# 3. 고스트(과학고) 시간 계산
now = datetime.now()
# 오늘 오전 8시 설정
start_time = now.replace(hour=8, minute=0, second=0, microsecond=0)
passed_seconds = (now - start_time).total_seconds()
passed_seconds = max(0, passed_seconds)

# 과학고는 오전 8시부터 밤 12시까지 일정하게 공부한다고 가정 (목표 10시간)
ghost_hours = min((passed_seconds / (16 * 3600)) * 10, 10.0)

# 4. 내 공부 데이터 (임시 저장)
if 'my_hours' not in st.session_state:
    st.session_state.my_hours = 0.0

# 5. 시각적 비교 (Progress Bar)
st.subheader(f"🚀 과학고 고스트: {ghost_hours:.1f}시간")
st.progress(ghost_hours / 10.0)

st.subheader(f"👤 나의 공부량: {st.session_state.my_hours:.1f}시간")
st.progress(min(st.session_state.my_hours / 10.0, 1.0))

# 6. 제어 버튼
st.divider()
if st.button("➕ 공부 시간 30분 추가 (테스트용)"):
    st.session_state.my_hours += 0.5
    st.rerun()

# 7. 격차 잔소리 (시각적)
gap = ghost_hours - st.session_state.my_hours
if gap > 0:
    st.error(f"⚠️ 과학고 학생보다 {gap:.1f}시간 뒤처져 있습니다!")
else:
    st.success(f"✅ 과학고 학생보다 {abs(gap):.1f}시간 앞서고 있습니다!")
