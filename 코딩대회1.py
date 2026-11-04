import streamlit as st

st.set_page_config(
    page_title="옥련여고 스마트 캠퍼스 맵", page_icon="🏫", layout="wide"
)

# ---------------------------------------------------------
# 1. 전역 세션 상태 초기화 (학번, 이름, 포인트 기본값 설정)
# ---------------------------------------------------------
if "total_score" not in st.session_state:
    st.session_state.total_score = 0
if "location" not in st.session_state:
    st.session_state.location = "home"

# 🎒 사용자 학번 및 이름 관리 (기본값: 민서의 학번 10304)
if "user_grade_class_no" not in st.session_state:
    st.session_state.user_grade_class_no = "10304"
if "user_name" not in st.session_state:
    st.session_state.user_name = "김민서"

# 2026년 실제 학교 구조(위성 사진 및 배치도 기준 본관·별관 구조) 데이터
school_map = {
    "본관 (큰 건물)": {
        "1층": ["중앙 현관", "교장실", "행정실", "학생안전부 자치부", "보건실", "교과활동실1", "교과활동실2", "연정문화관·다목적실"],
        "2층": ["본교무실", "방송운영실", "소회의실2", "진로진학상담실", "2-1반", "2-2반", "2-3반"],
        "3층": ["2-4반", "2-5반", "2-6반", "2-7반", "2-8반", "2-9반", "2-10반"],
        "4층": ["1-5반", "1-6반", "1-7반", "1-8반", "1-9반", "1-10반", "1-11반"],
        "5층": ["3-5반", "3-6반", "3-7반", "3-8반", "3-9반", "3-10반", "3-11반"],
    },
    "별관 (작은 건물)": {
        "1층": ["정문", "문서고", "택배실", "숙직실", "시설물실", "소모품보관실", "변전실", "발간실", "소회의실1", "학생/교직원 식당", "휴게실"],
        "2층": ["2학년교무실", "여교직원휴게실", "연정회의실", "과학준비실", "실험실1", "과학교육부", "실험실2", "Wee클래스"],
        "3층": ["1학년교무실", "AI 융합실", "미래교육부", "열린배움터1", "1-1반", "1-2반", "1-3반", "1-4반", "학생회실", "연우관(강당)"],
        "4층": ["3학년교무실", "동아리실", "미술실", "미술준비실", "열린배움터2", "3-1반", "3-2반", "3-3반", "3-4반", "남교직원휴게실"],
        "5층": ["음악실", "홈베이스4", "연정누리(Study Cafe)", "연정서재(도서관)", "하늘정원", "열린갤러리"],
    },
}

# 모든 장소 게시판 데이터 초기화
if "board_data" not in st.session_state:
    st.session_state.board_data = {}
    for bldg, floors in school_map.items():
        for floor, rooms in floors.items():
            for room in rooms:
                st.session_state.board_data[f"{bldg} - {floor} - {room}"] = []

# 미니게임 상태 초기화
if "game_scene" not in st.session_state:
    st.session_state.game_scene = "select"  # 게임 선택 화면
if "game_earned_score" not in st.session_state:
    st.session_state.game_earned_score = 0

# ---------------------------------------------------------
# 2. 사이드바 - 학생증 (학번/이름 수정 가능 & 포인트 관리)
# ---------------------------------------------------------
st.sidebar.title("🎒 옥련여고 모바일 학생증")
st.sidebar.write("**소속:** 옥련여자고등학교")

with st.sidebar.expander("✏️ 내 학번·이름 수정하기", expanded=True):
    with st.form("student_info_form"):
        new_no = st.text_input("학번 (예: 10304)", value=st.session_state.user_grade_class_no, max_chars=5)
        new_name = st.text_input("이름 (예: 김민서)", value=st.session_state.user_name)
        update_btn = st.form_submit_button("학생증 정보 저장")
        if update_btn:
            if new_no and new_name:
                st.session_state.user_grade_class_no = new_no
                st.session_state.user_name = new_name
                st.sidebar.success("정보가 업데이트되었습니다!")
            else:
                st.sidebar.warning("학번과 이름을 모두 입력해주세요.")

st.sidebar.info(f"👤 **현재 사용자:** `{st.session_state.user_grade_class_no} {st.session_state.user_name}`님")
st.sidebar.metric(label="⭐ 나의 누적 활동 포인트", value=f"{st.session_state.total_score} P")
st.sidebar.divider()

if st.sidebar.button("🗺️ 메인 캠퍼스 맵으로 가기", use_container_width=True):
    st.session_state.location = "home"
    st.rerun()

# ---------------------------------------------------------
# [화면 1] 홈 화면 : 본관·별관 구조 맞춤형 층별 맵 시스템
# ---------------------------------------------------------
if st.session_state.location == "home":
    st.title("🏫 옥련여고 스마트 캠퍼스 맵")
    st.markdown(
        "> 본관(큰 건물)과 별관(작은 건물)의 실제 구조를 바탕으로 한 층별 안내 시스템입니다. 건물을 선택하고 층수 버튼을 눌러 각 구역의 건의함과 분실물함을 이용해보세요!"
    )
    st.divider()

    bldg_tabs = st.tabs(["🏛️ 본관 (큰 건물 구조)", "🏢 별관 (작은 건물 구조)", "🎮 캠퍼스 미니게임 쉼터"])
    bldg_keys = list(school_map.keys())

    # 1. 본관 탭
    with bldg_tabs[0]:
        st.subheader("🏛️ 본관 층별 구역 안내")
        st.caption("본관의 1층부터 5층까지의 교실 및 시설 배치를 확인하세요.")

        for floor, rooms in school_map[bldg_keys[0]].items():
            with st.expander(f"📌 [본관] {floor} 구역 보기", expanded=(floor == "1층")):
                cols = st.columns(4)
                for idx, room in enumerate(rooms):
                    with cols[idx % 4]:
                        if st.button(room, key=f"btn_본관_{floor}_{room}", use_container_width=True):
                            st.session_state.location = f"{bldg_keys[0]} - {floor} - {room}"
                            st.rerun()

    # 2. 별관 탭
    with bldg_tabs[1]:
        st.subheader("🏢 별관 층별 구역 안내")
        st.caption("별관의 1층부터 5층까지의 특별실 및 교무실 배치를 확인하세요.")

        for floor, rooms in school_map[bldg_keys[1]].items():
            with st.expander(f"📌 [별관] {floor} 구역 보기", expanded=(floor == "1층")):
                cols = st.columns(4)
                for idx, room in enumerate(rooms):
                    with cols[idx % 4]:
                        if st.button(room, key=f"btn_별관_{floor}_{room}", use_container_width=True):
                            st.session_state.location = f"{bldg_keys[1]} - {floor} - {room}"
                            st.rerun()

    # 3. 미니게임 탭
    with bldg_tabs[2]:
        st.subheader("🎮 옥련여고 미니게임 쉼터")
        st.write("쉬는 시간에 즐기는 캠퍼스 미니게임 모음! 포인트를 모아보세요.")
        if st.button("🚀 미니게임 룸 입장하기", use_container_width=True):
            st.session_state.location = "미니게임"
            st.session_state.game_scene = "select"
            st.rerun()


# ---------------------------------------------------------
# [화면 2] 개별 장소 상세 페이지 (분실물 & 건의함 + 학번/이름 자동 연동)
# ---------------------------------------------------------
elif st.session_state.location != "미니게임":
    loc_key = st.session_state.location
    st.title(f"📍 옥련여고 [{loc_key}]")
    st.write("선택하신 위치의 공간입니다. 분실물 접수나 시설 개선 건의사항을 남겨보세요.")
    st.markdown("---")

    # 새 글 작성 폼 (사이드바에 입력한 학번/이름이 자동으로 반영됨)
    with st.expander("✍️ 이 위치에 새로운 소식(분실물/건의) 등록하기"):
        with st.form(f"form_{loc_key}"):
            post_type = st.selectbox(
                "글 종류 선택", ["🔍 분실물", "💡 건의사항", "💬 기타 소통"]
            )
            title = st.text_input("제목 (예: 사물함 앞에서 책을 주웠어요)")
            content = st.text_area("상세 내용 (예: 행정실에 맡겨두었습니다)")

            st.write(f"📝 **작성자 정보 (자동 적용):** `{st.session_state.user_grade_class_no} {st.session_state.user_name}`")
            submitted = st.form_submit_button("등록하고 +10 포인트 받기")

            if submitted:
                if title:
                    full_author = f"{st.session_state.user_grade_class_no} {st.session_state.user_name}"
                    st.session_state.board_data[loc_key].append(
                        {
                            "type": post_type,
                            "title": title,
                            "content": content,
                            "author": full_author,
                        }
                    )
                    st.session_state.total_score += 10
                    st.success("등록 완료! 포인트가 적립되었습니다.")
                    st.rerun()
                else:
                    st.warning("제목을 입력해주세요!")

    st.markdown("### 📋 이 위치에 등록된 소식들")
    posts = st.session_state.board_data.get(loc_key, [])
    if posts:
        for p in reversed(posts):
            with st.container(border=True):
                st.markdown(f"**[{p['type']}] {p['title']}**")
                st.write(p["content"])
                st.caption(f"작성자: `{p['author']}`")
    else:
        st.info("아직 등록된 소식이 없습니다. 첫 번째 소식을 남겨보세요! (+10P)")

    st.markdown("---")
    if st.button("🗺️ 메인 캠퍼스 맵으로 돌아가기", use_container_width=True):
        st.session_state.location = "home"
        st.rerun()


# ---------------------------------------------------------
# [화면 3] 풍성해진 미니게임 쉼터 (3가지 게임)
# ---------------------------------------------------------
elif st.session_state.location == "미니게임":
    st.title("🎮 옥련여고 미니게임 쉼터")
    st.write(f"현재 플레이어: **{st.session_state.user_grade_class_no} {st.session_state.user_name}**님")
    st.divider()

    # 1. 게임 종류 선택 화면
    if st.session_state.game_scene == "select":
        st.subheader("🕹️ 플레이할 미니게임을 선택하세요!")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("#### 🏃‍♀️ 지각 탈출 대작전")
            st.write("본관에서 별관 5층 음악실까지 쉬는 시간 내에 뛰어가는 타이쿤!")
            if st.button("게임 1 시작", use_container_width=True):
                st.session_state.game_scene = "game1_play"
                st.rerun()

        with col2:
            st.markdown("#### 🥪 매점 쟁탈전")
            st.write("쉬는 시간 종 치자마자 매점 단백질바를 사수하기 위한 심리전!")
            if st.button("게임 2 시작", use_container_width=True):
                st.session_state.game_scene = "game2_play"
                st.rerun()

        with col3:
            st.markdown("#### 🎯 옥련여고 골든벨")
            st.write("학교에 대해 얼마나 알고 있는지 맞추는 퀴즈 서바이벌!")
            if st.button("게임 3 시작", use_container_width=True):
                st.session_state.game_scene = "game3_play"
                st.rerun()

        st.markdown("---")
        if st.button("🗺️ 메인 캠퍼스 맵으로 돌아가기", use_container_width=True):
            st.session_state.location = "home"
            st.rerun()

    # --- [미니게임 1] 지각 탈출 대작전 ---
    elif st.session_state.game_scene == "game1_play":
        st.subheader("🏃‍♀️ [미니게임 1] 지각 탈출 대작전")
        st.write("쉬는 시간 종료 2분 전! 별관 5층 음악실 수업에 늦기 직전이다. 어떤 이동 경로를 선택하시겠습니까?")

        if st.button("1. 중앙 통로로 전력 질주 후 별관 계단 오르기 (+20 P)"):
            st.session_state.game_earned_score = 20
            st.session_state.game_scene = "ending"
            st.rerun()
        if st.button("2. 하늘정원 경치를 감상하며 우아하게 걷기 (+10 P)"):
            st.session_state.game_earned_score = 10
            st.session_state.game_scene = "ending"
            st.rerun()

        st.markdown("---")
        if st.button("게임 선택 화면으로 돌아가기"):
            st.session_state.game_scene = "select"
            st.rerun()

    # --- [미니게임 2] 매점 쟁탈전 ---
    elif st.session_state.game_scene == "game2_play":
        st.subheader("🥪 [미니게임 2] 매점 쟁탈전")
        st.write("체육 시간이 끝나고 목이 마르다. 매점에 갔더니 줄이 엄청 길다! 어떻게 할까?")

        if st.button("1. 새치기하는 친구를 용감하게 저지하고 정정당당하게 줄 서기 (+25 P)"):
            st.session_state.game_earned_score = 25
            st.session_state.game_scene = "ending"
            st.rerun()
        if st.button("2. 자판기 뒷사람에게 부탁해서 음료수 뽑기 (+15 P)"):
            st.session_state.game_earned_score = 15
            st.session_state.game_scene = "ending"
            st.rerun()

        st.markdown("---")
        if st.button("게임 선택 화면으로 돌아가기"):
            st.session_state.game_scene = "select"
            st.rerun()

    # --- [미니게임 3] 옥련여고 골든벨 ---
    elif st.session_state.game_scene == "game3_play":
        st.subheader("🎯 [미니게임 3] 옥련여고 골든벨 퀴즈")
        st.write("**문제:** 옥련여고 별관 5층에 위치하지 않는 시설은?")

        if st.button("1. 음악실"):
            st.session_state.game_earned_score = 5  # 오답 보상 적음
            st.session_state.game_scene = "quiz_wrong"
            st.rerun()
        if st.button("2. 연정서재(도서관)"):
            st.session_state.game_earned_score = 5
            st.session_state.game_scene = "quiz_wrong"
            st.rerun()
        if st.button("3. 교장실"):  # 정답 (본관 1층)
            st.session_state.game_earned_score = 30
            st.session_state.game_scene = "ending"
            st.rerun()

        st.markdown("---")
        if st.button("게임 선택 화면으로 돌아가기"):
            st.session_state.game_scene = "select"
            st.rerun()

    elif st.session_state.game_scene == "quiz_wrong":
        st.warning("아쉽습니다! 교장실은 본관 1층에 있어요!")
        if st.button("보상 +5 P 받고 결과로 넘어가기"):
            st.session_state.game_scene = "ending"
            st.rerun()

    # --- 공통 엔딩 화면 ---
    elif st.session_state.game_scene == "ending":
        st.balloons()
        st.success("🎉 미니게임 클리어 완료!")
        st.write(f"이번 게임 획득 포인트: **+{st.session_state.game_earned_score} P**")

        if st.button("🗺️ 포인트 적립하고 미니게임 메인으로 가기", use_container_width=True):
            st.session_state.total_score += st.session_state.game_earned_score
            st.session_state.game_earned_score = 0
            st.session_state.game_scene = "select"
            st.rerun()