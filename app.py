import time

# 1. 공부할 과목 리스트
today_subject = ["국어", "영어", "수학", "과학", "사회", "역사", "정보"]

# 공부 계획 리스트
study_plans = ["시험 대비", "예습", "복습"]

# 2. 공부 계획 확인 함수
def check_risk(study_time, study_plan):
    print("\n오늘의 공부 계획:", study_plan)
    print("총 공부 시간:", study_time, "분")

    # 3. 조건문
    if study_time >= 150:
        print("축하합니다! 오늘의 공부 목표를 달성했어요!")
        print("보상: 맛있는 간식 받기!")
    elif study_time >= 0:
        print("조금만 더 힘내세요!")
    else:
        print("올바른 공부 시간을 입력하세요.")

# 4. 프로그램 반복
while True:
    print("\n===== 나만의 공부 계획 앱 =====")

    # 과목 선택
    print("공부할 수 있는 과목:", today_subject)
    subject = input("오늘 공부할 과목을 입력하세요: ")

    # 공부 시간 입력
    study_time = int(input("공부할 시간(분)을 입력하세요: "))

    # 공부 계획 선택
    print("공부 계획:", study_plans)
    study_plan = input("공부 계획을 입력하세요: ")

    # 함수 실행
    check_risk(study_time, study_plan)

    print("\n오늘의 공부 기록이 저장되었습니다.")

    # 자정 확인
    if time.strftime("%H:%M") == "00:00":
        print("새로운 하루가 시작되었습니다! 공부 기록을 초기화합니다.")
        continue
