
import streamlit as st
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage
from operator import itemgetter

# ==========================================
# 1. 페이지 설정
# ==========================================
st.set_page_config(
    page_title="AIVLE School 학습 도우미",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. CSS 디자인
# ==========================================
st.markdown("""
<style>

/* 전체 배경 */
.stApp {
    background-color: #edf6f7;
}

/* 기본 여백 */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1500px;
}

/* 상단 메뉴 숨기기 */
#MainMenu, footer, header {
    visibility: hidden;
}

/* 사이드바 */
section[data-testid="stSidebar"] {
    background-color: #78c5cd;
    min-width: 230px;
    max-width: 230px;
}

section[data-testid="stSidebar"] > div {
    padding: 25px 15px;
}

/* 사이드바 텍스트 */
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label {
    color: white;
}

/* 로고 */
.logo-area {
    background-color: rgba(255,255,255,0.95);
    border-radius: 18px;
    padding: 17px 10px;
    margin-bottom: 30px;
    text-align: center;
}

/* 사이드바 메뉴 */
.menu-item {
    color: white;
    padding: 13px 15px;
    margin: 8px 0;
    border-radius: 13px;
    font-size: 15px;
    font-weight: 600;
}

.menu-active {
    background-color: rgba(255,255,255,0.27);
}

/* 메인 인사말 */
.greeting {
    font-size: 29px;
    font-weight: 800;
    color: #19334d;
    margin-bottom: 5px;
}

.sub-greeting {
    color: #91a2ae;
    font-size: 13px;
    margin-bottom: 20px;
}

/* 상단 검색창 */
div[data-testid="stTextInput"] input {
    border: none;
    border-radius: 15px;
    background-color: white;
    min-height: 45px;
    box-shadow: 0 3px 15px rgba(30,60,80,0.07);
}

/* 카드 공통 */
.dashboard-card {
    border-radius: 23px;
    padding: 24px;
    min-height: 155px;
    box-shadow: 0 5px 20px rgba(50,80,100,0.07);
    margin-bottom: 18px;
}

.welcome-card {
    background: #43aebe;
    color: white;
}

.result-card {
    background: #83b3f5;
    color: white;
}

.dashboard-card h3 {
    font-size: 20px;
    margin: 0 0 12px 0;
}

.dashboard-card p {
    font-size: 13px;
    line-height: 1.7;
}

/* 기능 카드 */
.feature-card {
    background-color: white;
    border-radius: 20px;
    padding: 17px 12px;
    box-shadow: 0 5px 18px rgba(50,80,100,0.06);
    min-height: 105px;
    text-align: center;
    color: #263c54;
}

.feature-icon {
    font-size: 28px;
    margin-bottom: 8px;
}

.feature-title {
    font-size: 15px;
    font-weight: 800;
}

.feature-desc {
    font-size: 11px;
    color: #a0abb6;
    margin-top: 5px;
}

/* 섹션 제목 */
.section-title {
    font-size: 19px;
    font-weight: 800;
    color: #19334d;
    margin: 15px 0;
}

/* 채팅 영역 */
.st-key-chat_panel {
    background-color: white;
    border-radius: 25px;
    padding: 20px;
    box-shadow: 0 5px 20px rgba(50,80,100,0.06);
    min-height: 450px;
}

/* 채팅 메시지 */
div[data-testid="stChatMessage"] {
    border-radius: 15px;
    padding: 13px;
    margin-bottom: 12px;
}

div[data-testid="stChatMessage"]:has(
    div[data-testid="chatAvatarIcon-user"]
) {
    background-color: #e5f5f5;
}

div[data-testid="stChatMessage"]:has(
    div[data-testid="chatAvatarIcon-assistant"]
) {
    background-color: #f2f6fb;
}

/* 오른쪽 프로필 */
.profile-card {
    background-color: white;
    border-radius: 24px;
    padding: 25px 15px;
    text-align: center;
    box-shadow: 0 5px 20px rgba(50,80,100,0.06);
    margin-bottom: 20px;
}

.profile-icon {
    font-size: 48px;
    background-color: #e9f1fa;
    width: 80px;
    height: 80px;
    line-height: 80px;
    border-radius: 50%;
    margin: auto;
}

.profile-name {
    color: #19334d;
    font-size: 18px;
    font-weight: 800;
    margin-top: 12px;
}

.profile-desc {
    font-size: 12px;
    color: #a1adb8;
}

/* 오른쪽 정보 카드 */
.info-card {
    background-color: white;
    border-radius: 18px;
    padding: 18px;
    margin-bottom: 15px;
    box-shadow: 0 4px 15px rgba(50,80,100,0.05);
}

.info-title {
    color: #19334d;
    font-size: 15px;
    font-weight: 800;
    margin-bottom: 12px;
}

/* 버튼 */
.stButton > button {
    border-radius: 12px;
    border: 1px solid #e5edf1;
    background-color: white;
    color: #29445b;
    min-height: 42px;
    font-size: 13px;
    transition: 0.2s;
}

.stButton > button:hover {
    border-color: #55b9c1;
    color: #269eaa;
    background-color: #f0fbfb;
}

/* 채팅 입력창 */
div[data-testid="stForm"] {
    background-color: #f3f6fa;
    border-radius: 15px;
    padding: 10px;
    border: none;
}

/* 파일 업로드 */
div[data-testid="stFileUploader"] {
    background-color: white;
    border-radius: 13px;
    padding: 10px;
}

hr {
    border-color: #e9eff2;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# 3. RAG 설정
# ==========================================
CHROMA_DIR = "chroma_db"
COLLECTION = "aivle_docs"


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


@st.cache_resource
def get_retriever():

    embedding = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    vectorstore = Chroma(
        collection_name=COLLECTION,
        embedding_function=embedding,
        persist_directory=CHROMA_DIR
    )

    return vectorstore.as_retriever(
        search_kwargs={"k": 3}
    )


@st.cache_resource
def get_chain():

    retriever = get_retriever()

    s_msg = """
    당신은 주어진 문서를 기반으로 답변하는
    AIVLE School 학습 도우미입니다.

    반드시 제공된 문서를 기반으로 답변하세요.
    문서에 근거가 없는 내용은 추측하지 마세요.

    [문서]
    {context}
    """

    h_msg = "{input}"

    prompt = ChatPromptTemplate.from_messages([
        ("system", s_msg),
        ("human", h_msg)
    ])

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        streaming=True,
        temperature=0
    )

    rag_chain = (
        {
            "context": itemgetter("input") | retriever | format_docs,
            "input": itemgetter("input")
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain


# ==========================================
# 4. 세션 상태
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None


# ==========================================
# 5. 사이드바
# ==========================================
with st.sidebar:

    # 로고
    st.markdown("""
    <div class="logo-area">
        <img src="https://raw.githubusercontent.com/Jangrae/img/master/aivle.png"
        width="145">
        <p style="color:#9aa8b0; font-size:11px;">
        AIVLE SCHOOL
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 메뉴
    st.markdown("""
    <div class="menu-item menu-active">🏠　홈</div>
    <div class="menu-item">📚　학습 도우미</div>
    <div class="menu-item">📁　학습 자료</div>
    <div class="menu-item">💬　대화 기록</div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <p style="font-size:14px;font-weight:800;color:white;">
    ⚙️ 관리자
    </p>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "파일 업로드",
        type=["pdf", "txt", "docx"]
    )

    if uploaded_file:
        st.success(f"{uploaded_file.name} 선택됨")

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🗑️ 대화 삭제", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending_prompt = None
        st.rerun()

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown("""
    <p style="color:white;font-size:12px;">
    AIVLE School<br>
    Learning Assistant
    </p>
    """, unsafe_allow_html=True)


# ==========================================
# 6. 메인 화면 레이아웃
# ==========================================
left, right = st.columns([7, 3], gap="large")


# ==========================================
# 7. 중앙 메인 영역
# ==========================================
with left:

    # 인사말 및 검색창
    title_col, search_col = st.columns([5, 4])

    with title_col:
        st.markdown("""
        <div class="greeting">Hello, AIVLE! 👋</div>
        <div class="sub-greeting">
        오늘도 새로운 지식을 함께 배워봐요.
        </div>
        """, unsafe_allow_html=True)

    with search_col:
        search_value = st.text_input(
            "검색",
            placeholder="궁금한 내용을 검색해 보세요.",
            label_visibility="collapsed",
            key="search_input"
        )

    # 검색어를 입력하고 Enter를 누르면 질문으로 전달
    if search_value:
        st.session_state.pending_prompt = search_value
        st.session_state.search_input = ""
        st.rerun()

    # ======================================
    # 환영 카드 / 학습 안내 카드
    # ======================================
    card1, card2 = st.columns(2, gap="medium")

    with card1:
        st.markdown("""
        <div class="dashboard-card welcome-card">
            <h3>Welcome back! ✨</h3>
            <p>
            AIVLE School 학습 도우미입니다.<br>
            교육 과정, 강의 내용, 미니프로젝트 등<br>
            궁금한 내용을 자유롭게 질문해 보세요!
            </p>
            <div style="font-size:27px;text-align:right;">
            📘 🤖
            </div>
        </div>
        """, unsafe_allow_html=True)

    with card2:
        st.markdown("""
        <div class="dashboard-card result-card">
            <h3>Learning Guide 📊</h3>
            <p>
            여러분의 학습을 도와드릴게요.<br>
            문서 기반 RAG 시스템을 활용하여<br>
            필요한 정보를 빠르게 찾아보세요.
            </p>
            <div style="font-size:27px;text-align:right;">
            💡 📚
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ======================================
    # 주요 기능 카드
    # ======================================
    st.markdown(
        '<div class="section-title">Quick Menu</div>',
        unsafe_allow_html=True
    )

    f1, f2, f3 = st.columns(3, gap="medium")

    with f1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📚</div>
            <div class="feature-title">학습 자료</div>
            <div class="feature-desc">교육 문서 기반 질문</div>
        </div>
        """, unsafe_allow_html=True)

    with f2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🧠</div>
            <div class="feature-title">학습 Q&A</div>
            <div class="feature-desc">AI 문서 검색 및 답변</div>
        </div>
        """, unsafe_allow_html=True)

    with f3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🚀</div>
            <div class="feature-title">미니프로젝트</div>
            <div class="feature-desc">프로젝트 정보 확인</div>
        </div>
        """, unsafe_allow_html=True)

    # ======================================
    # 채팅 영역
    # ======================================
    st.markdown(
        '<div class="section-title">💬 AI Learning Assistant</div>',
        unsafe_allow_html=True
    )

    with st.container(key="chat_panel"):

        st.markdown("""
        <div style="font-size:17px;font-weight:800;color:#19334d;
        margin-bottom:12px;">
        🤖 AIVLE School 학습 도우미
        </div>
        <div style="font-size:12px;color:#9baab4;
        margin-bottom:15px;">
        궁금한 내용을 질문하면 관련 문서를 찾아 답변해 드립니다.
        </div>
        """, unsafe_allow_html=True)

        # 기존 대화 출력
        if not st.session_state.messages:

            st.info(
                "안녕하세요! 😊 무엇이 궁금하신가요? "
                "아래 입력창에 질문을 작성해 주세요."
            )

        for message in st.session_state.messages:

            role = (
                "user"
                if isinstance(message, HumanMessage)
                else "assistant"
            )

            with st.chat_message(role):
                st.markdown(message.content)

        # 질문 입력
        with st.form("chat_form", clear_on_submit=True):

            question = st.text_input(
                "질문 입력",
                placeholder="질문을 입력하세요.",
                label_visibility="collapsed"
            )

            submitted = st.form_submit_button(
                "질문 보내기 ➤",
                use_container_width=True
            )


# ==========================================
# 8. 오른쪽 프로필 및 추천 질문
# ==========================================
with right:

    # 프로필 카드
    st.markdown("""
    <div class="profile-card">
        <div class="profile-icon">👩🏻‍💻</div>
        <div class="profile-name">AIVLE Assistant</div>
        <div class="profile-desc">
        Your Learning Partner
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 학습 도우미 안내
    st.markdown("""
    <div class="info-card">
        <div class="info-title">📘 학습 도우미 안내</div>
        <p style="font-size:12px;color:#9aa8b3;line-height:1.8;">
        AIVLE School 교육 자료를 기반으로<br>
        질문에 대한 답변을 제공합니다.<br><br>
        <b style="color:#29445b;">RAG 기반 문서 검색</b><br>
        관련 문서를 검색하고 답변을 생성합니다.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 추천 질문
    st.markdown("""
    <div class="section-title">💡 추천 질문</div>
    """, unsafe_allow_html=True)

    questions = [
        "KT 에이블스쿨 지원 자격은?",
        "미니프로젝트는 어떻게 진행되나요?",
        "교육 과정은 어떻게 구성되나요?",
        "수료 기준은 무엇인가요?"
    ]

    for i, q in enumerate(questions):

        if st.button(
            q,
            key=f"recommend_{i}",
            use_container_width=True
        ):
            st.session_state.pending_prompt = q
            st.rerun()

    # 최근 대화
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="info-card">
        <div class="info-title">🕒 Recent Activity</div>
        <p style="font-size:12px;color:#8e9da8;">
        최근 대화 기록
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.messages:

        for msg in reversed(st.session_state.messages):

            if isinstance(msg, HumanMessage):
                st.caption("💬 " + msg.content[:30])
    else:
        st.caption("아직 대화 기록이 없습니다.")


# ==========================================
# 9. RAG 질문 처리
# ==========================================
prompt = None

if submitted and question.strip():
    prompt = question.strip()

elif st.session_state.pending_prompt:
    prompt = st.session_state.pending_prompt

if prompt:

    st.session_state.pending_prompt = None

    # 사용자 질문 저장
    st.session_state.messages.append(
        HumanMessage(content=prompt)
    )

    # RAG 답변 생성
    try:

        with st.spinner("관련 문서를 검색하고 있습니다..."):

            chain = get_chain()

            response_stream = chain.stream({
                "input": prompt
            })

            full_response = st.write_stream(
                response_stream
            )

        # AI 답변 저장
        st.session_state.messages.append(
            AIMessage(content=full_response)
        )

    except Exception as e:

        st.error(f"답변 생성 중 오류가 발생했습니다: {e}")

    st.rerun()
