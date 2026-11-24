import streamlit as st
from datetime import date

# 앱 제목
st.title("📚 나만의 공부 계획 앱")
st.write("오늘의 공부 계획을 세우고 목표를 달성해 보세요!")

# 1. 리스트: 공부할 과목과 계획
today_subject = ["국어", "영어", "수학", "과학", "사회", "역사", "정보"]
study_plans = ["시험 대비", "예습", "복습"]

# 날짜 확인 및 공부 기록 초기화
if "study_date" not in st.session_state:
    st.session_state.study_date = date.today()
    st.session_state.records = []

if st.session_state.study_date != date.today():
    st.session_state.study_date = date.today()
    st.session_state.records = []

# 2. 함수: 공부 시간에 따른 보상 확인
def check_risk(study_time, study_plan):
    if study_time >= 150:
        return "🎉 축하합니다! 공부 목표 달성! 맛있는 간식을 보상으로 받으세요!"
    elif study_time >= 0:
        return "💪 조금만 더 힘내세요! 목표까지 도전해 봐요!"
    else:
        return "공부 시간을 다시 확인해 주세요."

# 과목 선택
st.subheader("1. 오늘 공부할 과목")
selected_subjects = st.multiselect(
    "공부할 과목을 선택하세요.",
    today_subject
)

# 공부 시간 선택
st.subheader("2. 공부 가능한 시간")
study_time = st.slider(
    "공부할 시간을 선택하세요. (분)",
    min_value=0,
    max_value=300,
    value=60,
    step=10
)

# 공부 계획 선택
st.subheader("3. 오늘의 공부 계획")
study_plan = st.selectbox(
    "공부 목적을 선택하세요.",
    study_plans
)

# 공부 계획 저장 버튼
if st.button("오늘의 공부 계획 저장하기"):
    if len(selected_subjects) == 0:
        st.warning("공부할 과목을 하나 이상 선택해 주세요.")
    else:
        st.session_state.records.append({
            "subjects": selected_subjects,
            "time": study_time,
            "plan": study_plan
        })
        st.success("공부 계획이 저장되었습니다!")

# 오늘의 공부 기록
st.divider()
st.subheader("📖 오늘의 공부 기록")

total_study_time = 0

for record in st.session_state.records:
    st.write("과목:", ", ".join(record["subjects"]))
    st.write("공부 계획:", record["plan"])
    st.write("공부 시간:", record["time"], "분")
    total_study_time += record["time"]

# 누적 공부 시간
st.metric("오늘의 총 공부 시간", f"{total_study_time}분")

# 3. 조건문: 목표 달성 여부 확인
if len(st.session_state.records) > 0:
    result = check_risk(total_study_time, study_plan)
    st.info(result)

# 공부 기록 초기화 버튼
if st.button("공부 기록 초기화"):
    st.session_state.records = []
    st.rerun()

# 4. 반복문: 선택한 과목 확인
st.divider()
st.subheader("✅ 선택한 과목 확인")

for subject in today_subject:
    if subject in selected_subjects:
        st.write("✔️", subject)
