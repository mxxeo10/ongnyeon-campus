import streamlit as st

st.set_page_config(
    page_title="옥련여고 스마트 캠퍼스 맵", page_icon="🏫", layout="wide"
)

# ---------------------------------------------------------
# 1. 전역 세션 상태 초기화 (학번, 이름, 포인트)
# ---------------------------------------------------------
if "total_score" not in st.session_state:
    st.session_state.total_score = 0
if "location" not in st.session_state:
    st.session_state.location = "home"

# 사용자 학번 및 이름 기본값 설정
if "user_grade_class_no" not in st.session_state:
    st.session_state.user_grade_class_no = "10304"
if "user_name" not in st.session_state:
    st.session_state.user_name = "김민서"

# 학교 구조 데이터 (본관 / 별관)
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
    st.session_state.game_scene = "select"
if "game_earned_score" not in st.session_state:
    st.session_state.game_earned_score = 0

# ---------------------------------------------------------
# 2. 사이드바 - 학생증 (이름/학번 수정 입력창 상시 노출)
# ---------------------------------------------------------
st.sidebar.title("🎒 옥련여고 학생증")
st.sidebar.caption("소속: 옥련여자고등학교")
st.sidebar.markdown("---")

st.sidebar.subheader("✏️ 내 학생 정보 입력")
# 상시 노출되는 학번/이름 입력 폼
with st.sidebar.form("student_info_form_direct"):
    input_no = st.text_input("학번 입력", value=st.session_state.user_grade_class_no, placeholder="예: 10304")
    input_name = st.text_input("이름 입력", value=st.session_state.user_name, placeholder="예: 김민서")
    save_btn = st.form_submit_button("💾 내 정보 저장하기", use_container_width=True)

    if save_btn:
        if input_no and input_name:
            st.session_state.user_grade_class_no = input_no
            st.session_state.user_name = input_name
            st.sidebar.success("저장되었습니다!")
        else:
            st.sidebar.error("학번과 이름을 입력해주세요.")

st.sidebar.markdown("---")
st.sidebar.success(f"👤 **현재 사용자:**\n`{st.session_state.user_grade_class_no}` **{st.session_state.user_name}** 님")
st.sidebar.metric(label="⭐ 나의 포인트", value=f"{st.session_state.total_score} P")
st.sidebar.markdown("---")

if st.sidebar.button("🗺️ 메인 캠퍼스 맵", use_container_width=True):
    st.session_state.location = "home"
    st.rerun()

# ---------------------------------------------------------
# [화면 1] 홈 화면 : 본관·별관 구조 층별 맵
# ---------------------------------------------------------
if st.session_state.location == "home":
    st.title("🏫 옥련여고 스마트 캠퍼스 맵")
    st.markdown("> 오른쪽 화면과 왼쪽 메뉴를 통해 본관과 별관을 둘러보세요.")
    st.divider()

    bldg_tabs = st.tabs(["🏛️ 본관 (큰 건물)", "🏢 별관 (작은 건물)", "🎮 캠퍼스 미니게임"])
    bldg_keys = list(school_map.keys())

    # 1. 본관
    with bldg_tabs[0]:
        st.subheader("🏛️ 본관 층별 구역")
        for floor, rooms in school_map[bldg_keys[0]].items():
            with st.expander(f"📌 [본관] {floor} 시설 보기", expanded=(floor == "1층")):
                cols = st.columns(4)
                for idx, room in enumerate(rooms):
                    with cols[idx % 4]:
                        if st.button(room, key=f"btn_본관_{floor}_{room}", use_container_width=True):
                            st.session_state.location = f"{bldg_keys[0]} - {floor} - {room}"
                            st.rerun()

    # 2. 별관
    with bldg_tabs[1]:
        st.subheader("🏢 별관 층별 구역")
        for floor, rooms in school_map[bldg_keys[1]].items():
            with st.expander(f"📌 [별관] {floor} 시설 보기", expanded=(floor == "1층")):
                cols = st.columns(4)
                for idx, room in enumerate(rooms):
                    with cols[idx % 4]:
                        if st.button(room, key=f"btn_별관_{floor}_{room}", use_container_width=True):
                            st.session_state.location = f"{bldg_keys[1]} - {floor} - {room}"
                            st.rerun()

    # 3. 미니게임
    with bldg_tabs[2]:
        st.subheader("🎮 옥련여고 미니게임 쉼터")
        if st.button("🚀 미니게임 입장하기", use_container_width=True):
            st.session_state.location = "미니게임"
            st.session_state.game_scene = "select"
            st.rerun()


# ---------------------------------------------------------
# [화면 2] 개별 장소 게시판 (분실물 / 건의함)
# ---------------------------------------------------------
elif st.session_state.location != "미니게임":
    loc_key = st.session_state.location
    st.title(f"📍 [{loc_key}]")
    st.write("이 장소에 분실물 접수나 건의사항을 등록해 보세요.")
    st.markdown("---")

    with st.form(f"form_{loc_key}"):
        st.subheader("✍️ 글 남기기")
        post_type = st.selectbox("종류", ["🔍 분실물", "💡 건의사항", "💬 기타 소통"])
        title = st.text_input("제목")
        content = st.text_area("내용")

        st.info(f"작성자: **{st.session_state.user_grade_class_no} {st.session_state.user_name}**")
        submitted = st.form_submit_button("등록 (+10P)")

        if submitted:
            if title:
                full_author = f"{st.session_state.user_grade_class_no} {st.session_state.user_name}"
                st.session_state.board_data[loc_key].append(
                    {"type": post_type, "title": title, "content": content, "author": full_author}
                )
                st.session_state.total_score += 10
                st.success("글이 등록되었습니다!")
                st.rerun()
            else:
                st.warning("제목을 입력해주세요.")

    st.markdown("### 📋 등록된 게시글")
    posts = st.session_state.board_data.get(loc_key, [])
    if posts:
        for p in reversed(posts):
            with st.container(border=True):
                st.markdown(f"**[{p['type']}] {p['title']}**")
                st.write(p["content"])
                st.caption(f"작성자: `{p['author']}`")
    else:
        st.info("아직 등록된 글이 없습니다.")

    st.markdown("---")
    if st.button("🗺️ 메인으로 돌아가기", use_container_width=True):
        st.session_state.location = "home"
        st.rerun()


# ---------------------------------------------------------
# [화면 3] 미니게임 쉼터
# ---------------------------------------------------------
elif st.session_state.location == "미니게임":
    st.title("🎮 미니게임 쉼터")
    st.write(f"플레이어: **{st.session_state.user_grade_class_no} {st.session_state.user_name}** 님")
    st.divider()

    if st.session_state.game_scene == "select":
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("#### 🏃‍♀️ 지각 탈출")
            if st.button("시작하기", key="g1"):
                st.session_state.game_scene = "game1_play"
                st.rerun()
        with col2:
            st.markdown("#### 🥪 매점 쟁탈전")
            if st.button("시작하기", key="g2"):
                st.session_state.game_scene = "game2_play"
                st.rerun()
        with col3:
            st.markdown("#### 🎯 학교 골든벨")
            if st.button("시작하기", key="g3"):
                st.session_state.game_scene = "game3_play"
                st.rerun()

        st.markdown("---")
        if st.button("🗺️ 메인으로 돌아가기"):
            st.session_state.location = "home"
            st.rerun()

    elif st.session_state.game_scene == "game1_play":
        st.subheader("🏃‍♀️ 지각 탈출 대작전")
        if st.button("전력 질주하기 (+20P)"):
            st.session_state.game_earned_score = 20
            st.session_state.game_scene = "ending"
            st.rerun()

    elif st.session_state.game_scene == "game2_play":
        st.subheader("🥪 매점 쟁탈전")
        if st.button("줄 바로 서기 (+25P)"):
            st.session_state.game_earned_score = 25
            st.session_state.game_scene = "ending"
            st.rerun()

    elif st.session_state.game_scene == "game3_play":
        st.subheader("🎯 옥련여고 골든벨")
        st.write("별관 5층에 없는 시설은?")
        if st.button("교장실 (정답)"):
            st.session_state.game_earned_score = 30
            st.session_state.game_scene = "ending"
            st.rerun()

    elif st.session_state.game_scene == "ending":
        st.balloons()
        st.success(f"🎉 성공! +{st.session_state.game_earned_score}P 획득")
        if st.button("포인트 적립하고 게임 메뉴로"):
            st.session_state.total_score += st.session_state.game_earned_score
            st.session_state.game_earned_score = 0
            st.session_state.game_scene = "select"
            st.rerun()
