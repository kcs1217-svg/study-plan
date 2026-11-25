import streamlit as st
from datetime import date

# 화면 설정
st.set_page_config(
    page_title="나만의 공부 관리 앱",
    page_icon="📚",
    layout="centered"
)

st.title("📚 나만의 공부 관리 앱")
st.write("계획을 세우고 얼마나 성실하게 실천했는지 확인해 보세요!")

# 1. 리스트
subjects = ["국어", "영어", "수학", "과학", "사회", "역사", "정보"]
plans = ["시험 대비", "예습", "복습"]

# 날짜별 기록 관리
if "saved_date" not in st.session_state:
    st.session_state.saved_date = date.today()

if "records" not in st.session_state:
    st.session_state.records = []

if st.session_state.saved_date != date.today():
    st.session_state.records = []
    st.session_state.saved_date = date.today()

# 2. 함수
def check_risk(planned_time, actual_time):
    if planned_time == 0:
        return 0

    achievement = actual_time / planned_time * 100
    return min(achievement, 100)

def evaluate(achievement):
    if achievement >= 100:
        return "🏆 완벽하게 실천했어요!"
    elif achievement >= 80:
        return "👏 아주 성실하게 실천했어요!"
    elif achievement >= 50:
        return "👍 조금만 더 노력해 봐요!"
    else:
        return "💪 내일은 계획을 더 실천해 봐요!"

# 3. 공부 계획 입력
st.subheader("📝 오늘의 공부 계획")

selected_subjects = st.multiselect(
    "공부할 과목을 여러 개 선택하세요.",
    subjects,
    placeholder="과목을 선택하세요."
)

study_plan = st.selectbox("공부 목적", plans)

# 과목별 공부 시간 입력
planned_times = {}
actual_times = {}
completed_subjects = {}

if selected_subjects:
    st.write("### ⏰ 과목별 공부 시간")

    for subject in selected_subjects:
        st.markdown(f"**📖 {subject}**")

        col1, col2 = st.columns(2)

        with col1:
            planned_times[subject] = st.number_input(
                f"{subject} 계획 시간(분)",
                min_value=1,
                max_value=300,
                value=60,
                key=f"planned_{subject}"
            )

        with col2:
            actual_times[subject] = st.number_input(
                f"{subject} 실제 공부 시간(분)",
                min_value=0,
                max_value=300,
                value=0,
                key=f"actual_{subject}"
            )

        completed_subjects[subject] = st.checkbox(
            f"{subject} 공부 완료",
            key=f"completed_{subject}"
        )

# 공부 기록 저장
if st.button("공부 기록 저장하기"):
    if len(selected_subjects) == 0:
        st.warning("공부할 과목을 하나 이상 선택해 주세요.")

    else:
        for subject in selected_subjects:
            st.session_state.records.append({
                "subject": subject,
                "plan": study_plan,
                "planned": planned_times[subject],
                "actual": actual_times[subject],
                "completed": completed_subjects[subject]
            })

        st.success("공부 기록이 저장되었습니다!")

# 4. 공부 관리 결과
st.divider()
st.subheader("📊 오늘의 공부 관리 결과")

records = st.session_state.records

if records:

    total_planned = sum(r["planned"] for r in records)
    total_actual = sum(r["actual"] for r in records)
    completed_count = sum(r["completed"] for r in records)

    # 150분 초과 시 보상
    if total_actual > 150:
        st.balloons()
        st.success("🎉 축하합니다! 실제 공부 시간 150분 달성!")
        st.write("열심히 공부한 당신에게 맛있는 과자를 드립니다! 🍪")

        st.image(
            "https://commons.wikimedia.org/wiki/Special:FilePath/Cookies.jpg",
            caption="오늘의 공부 보상! 맛있는 쿠키 🍪",
            width=300
        )

    # 전체 공부 시간
    achievement = check_risk(total_planned, total_actual)

    col1, col2 = st.columns(2)

    col1.metric("계획 공부 시간", f"{total_planned}분")
    col2.metric("실제 공부 시간", f"{total_actual}분")

    st.write("### 공부 시간 달성률")
    st.progress(int(achievement))
    st.write(f"**{achievement:.1f}%**")

    st.write(evaluate(achievement))

    # 계획 완료율
    st.write(
        f"완료한 계획: {completed_count} / {len(records)}개"
    )

    completion_rate = completed_count / len(records) * 100

    st.write("### 계획 완료율")
    st.progress(int(completion_rate))
    st.write(f"**{completion_rate:.1f}%**")

    # 5. 과목별 공부 시간 분석
    st.divider()
    st.subheader("📈 과목별 공부 시간 분석")

    subject_stats = {}

    for subject in subjects:
        subject_records = [
            r for r in records if r["subject"] == subject
        ]

        if subject_records:
            planned = sum(r["planned"] for r in subject_records)
            actual = sum(r["actual"] for r in subject_records)

            rate = check_risk(planned, actual)

            subject_stats[subject] = {
                "planned": planned,
                "actual": actual,
                "rate": rate
            }

    # 과목별 그래프
    chart_data = {
        "계획 시간": {
            s: v["planned"] for s, v in subject_stats.items()
        },
        "실제 공부 시간": {
            s: v["actual"] for s, v in subject_stats.items()
        }
    }

    st.write("과목별 계획 시간과 실제 공부 시간 비교")
    st.bar_chart(chart_data)

    # 과목별 달성률
    st.write("### 과목별 달성률")

    for subject, data in subject_stats.items():
        st.write(f"**{subject}**")
        st.write(
            f"계획: {data['planned']}분 / "
            f"실제: {data['actual']}분"
        )
        st.progress(int(data["rate"]))
        st.write(f"달성률: {data['rate']:.1f}%")

    # 과목별 기록
    st.divider()
    st.subheader("📖 과목별 공부 기록")

    for i, record in enumerate(records, 1):
        st.write(
            f"{i}. {record['subject']} / {record['plan']}"
        )
        st.write(
            f"계획: {record['planned']}분 | "
            f"실제: {record['actual']}분"
        )
        st.write(
            "완료" if record["completed"] else "미완료"
        )

else:
    st.info("아직 저장된 공부 기록이 없습니다.")

# 6. 기록 초기화
st.divider()

if st.button("오늘의 기록 초기화"):
    st.session_state.records = []
    st.rerun()

