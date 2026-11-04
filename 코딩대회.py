import streamlit as st

st.set_page_config(
    page_title="옥련여고 스마트 캠퍼스 맵", page_icon="🏫", layout="wide"
)

# ---------------------------------------------------------
# 1. 전역 세션 상태 초기화
# ---------------------------------------------------------
if "total_score" not in st.session_state:
    st.session_state.total_score = 0
if "location" not in st.session_state:
    st.session_state.location = "home"

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

# 미니게임 상태
if "game_scene" not in st.session_state:
    st.session_state.game_scene = "start"
if "game_earned_score" not in st.session_state:
    st.session_state.game_earned_score = 0

# ---------------------------------------------------------
# 2. 사이드바 - 학생증 및 포인트
# ---------------------------------------------------------
st.sidebar.title("🎒 옥련여고 학생증")
st.sidebar.write("**소속:** 옥련여자고등학교")
st.sidebar.metric(
    label="⭐ 나의 누적 활동 포인트", value=f"{st.session_state.total_score} P"
)
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
        "> 위성 사진으로 확인한 **본관(큰 건물)**과 **별관(작은 건물)**의 실제 구조를 바탕으로 재구성한 층별 안내 시스템입니다. 건물을 선택하고 층수 버튼을 누르면 각 구역의 건의함으로 연결됩니다!"
    )
    st.divider()

    # 건물 선택 (탭 방식)
    bldg_tabs = st.tabs(["🏛️ 본관 (큰 건물 구조)", "🏢 별관 (작은 건물 구조)", "🎮 캠퍼스 이동 미니게임"])

    # 건물별 탭 내용 구성
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
        st.subheader("🎮 옥련여고 캠퍼스 미니게임")
        st.write("쉬는 시간에 본관에서 별관 5층 음악실까지 이동하는 타이쿤 게임!")
        if st.button("🚀 미니게임 시작하기", use_container_width=True):
            st.session_state.location = "미니게임"
            st.rerun()


# ---------------------------------------------------------
# [화면 2] 개별 장소 상세 페이지 (분실물 & 건의함 + 학번/이름)
# ---------------------------------------------------------
elif st.session_state.location != "미니게임":
    loc_key = st.session_state.location
    st.title(f"📍 옥련여고 [{loc_key}]")
    st.write("선택하신 위치의 공간입니다. 분실물 접수나 시설 개선 건의사항을 남겨보세요.")
    st.markdown("---")

    # 새 글 작성 폼
    with st.expander("✍️ 이 위치에 새로운 소식(분실물/건의) 등록하기"):
        with st.form(f"form_{loc_key}"):
            post_type = st.selectbox(
                "글 종류 선택", ["🔍 분실물", "💡 건의사항", "💬 기타 소통"]
            )
            title = st.text_input("제목 (예: 사물함 앞에서 책을 주웠어요)")
            content = st.text_area("상세 내용 (예: 행정실에 맡겨두었습니다)")

            col_a, col_b = st.columns(2)
            with col_a:
                grade_class_no = st.text_input("학번 입력 (예: 10304)", max_chars=5)
            with col_b:
                name = st.text_input("이름 입력 (예: 김민서)")

            submitted = st.form_submit_button("등록하고 +10 포인트 받기")

            if submitted:
                if title and grade_class_no and name:
                    full_author = f"{grade_class_no} {name}"
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
                    st.warning("학번, 이름, 제목을 모두 정확히 입력해주세요!")

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
# [화면 3] 미니게임 쉼터
# ---------------------------------------------------------
elif st.session_state.location == "미니게임":
    st.title("🎮 옥련여고 미니게임 쉼터")
    st.write("본관에서 별관 5층 음악실까지 지각하지 않고 이동하기 타이쿤!")
    st.divider()

    if st.session_state.game_scene == "start":
        st.subheader("⏰ 쉬는 시간 종료 직전! 본관에서 별관 5층 음악실로 이동해야 한다!")
        st.write("어떤 경로로 이동하시겠습니까?")

        if st.button("🏃‍♀️ 중앙 통로를 가로질러 별관 계단 전력 질주! (+20 P)"):
            st.session_state.game_earned_score = 20
            st.session_state.game_scene = "ending"
            st.rerun()

        if st.button("🚶‍♀️ 하늘정원을 구경하며 느긋하게 이동 (+10 P)"):
            st.session_state.game_earned_score = 10
            st.session_state.game_scene = "ending"
            st.rerun()

    elif st.session_state.game_scene == "ending":
        st.balloons()
        st.success("🎉 무사히 음악실 도착 완료!")
        st.write(f"이번 게임 보상 포인트: **+{st.session_state.game_earned_score} P**")

        if st.button("🗺️ 포인트 적립하고 메인 캠퍼스 맵으로 돌아가기", use_container_width=True):
            st.session_state.total_score += st.session_state.game_earned_score
            st.session_state.game_earned_score = 0
            st.session_state.game_scene = "start"
            st.session_state.location = "home"
            st.rerun()