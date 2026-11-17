import streamlit as st
import calendar as pycalendar
import uuid
from datetime import date, datetime
from zoneinfo import ZoneInfo
import html
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

/* 전체 여백 */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1500px;
}

/* 기본 메뉴 및 푸터 숨기기 */
#MainMenu, footer {
    visibility: hidden;
}

/* 상단 헤더 유지 - 사이드바 버튼 보호 */
.stAppHeader {
    background-color: transparent;
}

/* 사이드바 */
section[data-testid="stSidebar"] {
    background-color: #78c5cd;
    min-width: 230px;
}

/* 사이드바 내부 여백 */
section[data-testid="stSidebar"] > div {
    padding: 25px 15px;
}

/* 사이드바 글자 */
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

.logo-area p {
    color: #9aa8b0 !important;
    font-size: 11px;
    margin-bottom: 0;
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

/* 검색창 */
div[data-testid="stTextInput"] input {
    border: none;
    border-radius: 15px;
    background-color: white;
    min-height: 45px;
    box-shadow: 0 3px 15px rgba(30,60,80,0.07);
}

/* 대시보드 카드 */
.dashboard-card {
    border-radius: 23px;
    padding: 24px;
    min-height: 155px;
    box-shadow: 0 5px 20px rgba(50,80,100,0.07);
    margin-bottom: 18px;
    box-sizing: border-box;
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
    color: white;
}

.dashboard-card p {
    font-size: 13px;
    line-height: 1.7;
    color: white;
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
    box-sizing: border-box;
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

/* 출결 및 일정 달력 */
.st-key-calendar_panel {
    background: #ffffff;
    border-radius: 24px;
    padding: 22px;
    margin: 18px 0 24px 0;
    box-shadow: 0 5px 20px rgba(50,80,100,0.06);
}
.calendar-panel {
    background: #ffffff;
    border-radius: 24px;
    padding: 22px;
    margin: 18px 0 24px 0;
    box-shadow: 0 5px 20px rgba(50,80,100,0.06);
}
.calendar-caption {
    color: #91a2ae;
    font-size: 12px;
    margin-top: -6px;
    margin-bottom: 12px;
}
.calendar-weekday {
    text-align: center;
    color: #7f929f;
    font-size: 12px;
    font-weight: 700;
    padding: 7px 0;
}
.calendar-legend {
    color: #8496a3;
    font-size: 11px;
    margin-top: 10px;
}
.calendar-subcard {
    background: #f7fafc;
    border: 1px solid #edf2f5;
    border-radius: 16px;
    padding: 15px;
    min-height: 150px;
}
.calendar-subtitle {
    color: #19334d;
    font-weight: 800;
    font-size: 14px;
    margin-bottom: 10px;
}

section[data-testid="stSidebar"] button p {color:inherit !important;}
button[kind="primary"] {background:#43aebe !important;color:white !important;border-color:#43aebe !important;}
.st-key-calendar_panel .stButton > button {min-height:58px;}
/* 달력 날짜 버튼 */
.st-key-calendar_day button {
    min-height: 58px;
}

/* 채팅 영역 */
.st-key-chat_panel {
    background-color: white;
    border-radius: 25px;
    padding: 20px;
    box-shadow: 0 5px 20px rgba(50,80,100,0.06);
    min-height: 450px;
}

/* 채팅 제목 */
.chat-heading {
    font-size: 17px;
    font-weight: 800;
    color: #19334d;
    margin-bottom: 12px;
}

.chat-description {
    font-size: 12px;
    color: #9baab4;
    margin-bottom: 15px;
}

/* 채팅 말풍선 */
div[data-testid="stChatMessage"] {
    border-radius: 15px;
    padding: 13px;
    margin-bottom: 12px;
}

/* 사용자 메시지 */
div[data-testid="stChatMessage"]:has(
    div[data-testid="chatAvatarIcon-user"]
) {
    background-color: #e5f5f5;
}

/* AI 메시지 */
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
    font-size: 42px;
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
    margin-top: 5px;
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

.info-card p {
    font-size: 12px;
    color: #9aa8b3;
    line-height: 1.8;
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

/* 파일 업로드 */
div[data-testid="stFileUploader"] {
    background-color: white;
    border-radius: 13px;
    padding: 10px;
}

/* 채팅 입력 폼 */
div[data-testid="stForm"] {
    background-color: #f3f6fa;
    border-radius: 15px;
    padding: 10px;
    border: none;
}

/* 구분선 */
hr {
    border-color: #e9eff2;
}


/* 캘린더 오른쪽 패널: 본문과 함께 흘러가지 않고 화면 상단에 유지 */
@media (min-width: 769px) {
    [data-testid="stColumn"]:has(.st-key-upcoming_panel) {
        position: sticky;
        top: 4.5rem;
        align-self: flex-start;
        height: fit-content;
        max-height: calc(100dvh - 5.5rem);
        overflow-y: auto;
        overscroll-behavior-y: contain;
        scrollbar-width: thin;
    }
}
/* 좁은 화면에서 세로로 쌓이는 패널은 본문을 가리지 않도록 일반 배치 */
@media (max-width: 768px) {
    [data-testid="stColumn"]:has(.st-key-upcoming_panel) {
        position: static;
        max-height: none;
        overflow: visible;
    }
}


.today-card { background: linear-gradient(115deg, #ffffff 0%, #def4ee 100%); border: 1px solid #c8e6df; border-radius: 24px; padding: 28px 32px; margin: 8px 0 12px; box-shadow: 0 8px 28px rgba(37,95,87,.05); display: flex; align-items: center; gap: 28px; }
.today-stamp { min-width: 94px; padding: 12px; border-radius: 18px; background: #fff; text-align: center; box-shadow: 0 4px 14px rgba(37,95,87,.06); }
.today-month { color: #41877b; font-size: 13px; font-weight: 700; letter-spacing: 1px; }
.today-number { color: #116e61; font-size: 46px; font-weight: 800; line-height: 1.2; }
.today-weekday { color: #55746d; font-size: 13px; }
.today-eyebrow { color: #537a72; font-size: 13px; letter-spacing: .7px; margin-bottom: 8px; }
.today-heading { color: #23483f; font-size: clamp(21px, 2.1vw, 30px); font-weight: 750; line-height: 1.4; margin: 0 0 9px; }
.today-heading strong { color: #008675; }
.today-cheer { color: #48675f; font-size: 15px; margin: 0 0 12px; line-height: 1.6; }
.today-basis { color: #718c85; font-size: 11px; }
@media(max-width: 600px) { .today-card { padding: 20px 16px; gap: 15px; } .today-stamp { min-width: 72px; } .today-number { font-size: 36px; } }


.cert-exam-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px; margin: 10px 0 18px; }
.cert-exam-card { background: #fff; border: 1px solid #d4e6e2; border-radius: 20px; padding: 24px; display: flex; flex-direction: column; box-shadow: 0 5px 18px rgba(32,86,76,.04); min-width: 0; }
.cert-card-badge { color: #137f6e; background: #edf8f4; border-radius: 8px; padding: 5px 10px; font-size: 12px; font-weight: 650; align-self: flex-start; }
.cert-exam-card h3 { color: #29473e; font-size: 19px; line-height: 1.5; margin: 14px 0 16px; overflow-wrap: anywhere; }
.cert-exam-card dl { margin: 0 0 22px; }
.cert-exam-card dt { color: #738a83; font-size: 12px; margin-bottom: 4px; }
.cert-exam-card dd { color: #3e534d; font-size: 14px; line-height: 1.7; margin: 0 0 12px; overflow-wrap: anywhere; }
a.cert-apply-link { display: block; text-align: center; background: #eef8f4; color: #117963 !important; border: 1px solid #cce9df; border-radius: 11px; padding: 11px 12px; margin-top: auto; text-decoration: none !important; font-size: 14px; font-weight: 650; }
a.cert-apply-link:hover { background: #dcf1e8; border-color: #80baa7; }
a.cert-apply-link:focus-visible { outline: 3px solid #168a72; outline-offset: 3px; }
@media(max-width: 640px) { .cert-exam-grid { grid-template-columns: 1fr; } }

</style>
""", unsafe_allow_html=True)


# ==========================================
# 3. RAG 설정
# ==========================================

import os, re, json, math, tempfile, hashlib
from pathlib import Path
from collections import Counter
import pandas as pd
CHROMA_DIR = "chroma_db"
COLLECTION = "aivle_docs"
ONTOLOGY_FILE = "aivle_ontology.json"
BOT_IMG = "assets/bot.png"

def ensure_rag_imports():
    global OpenAIEmbeddings, ChatOpenAI, Chroma, Document
    global ChatPromptTemplate, MessagesPlaceholder, StrOutputParser
    global PyMuPDF4LLMLoader, RecursiveCharacterTextSplitter
    from langchain_openai import OpenAIEmbeddings, ChatOpenAI
    from langchain_chroma import Chroma
    from langchain_core.documents import Document
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
    from langchain_core.output_parsers import StrOutputParser
    from langchain_pymupdf4llm import PyMuPDF4LLMLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    try:
        key = st.secrets.get("OPENAI_API_KEY")
        if key: os.environ["OPENAI_API_KEY"] = key
    except Exception:
        pass

def format_docs(docs):
    return "\n\n".join(d.page_content for d in docs)

@st.cache_resource(show_spinner="백서 검색을 준비하고 있습니다. 최초 질문 시 시간이 걸릴 수 있습니다.")
def get_vectorstore():
    ensure_rag_imports()
    embedding = OpenAIEmbeddings(model="text-embedding-3-small")
    # Existing deployed DB is reused; opening UI pages never indexes the PDF.
    vs = Chroma(collection_name=COLLECTION, embedding_function=embedding,
                persist_directory=CHROMA_DIR)
    if vs._collection.count():
        return vs
    pdf = Path("AIVLE School 백서.pdf")
    if not pdf.exists():
        raise ValueError("백서 PDF 또는 기존 chroma_db를 배포 저장소에 넣어 주세요.")
    digest = hashlib.sha256(pdf.read_bytes()).hexdigest()[:20]
    vs = Chroma(collection_name="whitepaper_"+digest, embedding_function=embedding,
                persist_directory=CHROMA_DIR)
    if not vs._collection.count():
        docs = PyMuPDF4LLMLoader(str(pdf)).load()
        chunks = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100,
                    separators=["\n\n", "\n", ".", " ", ""]).split_documents(docs)
        chunks = [d for d in chunks if d.page_content.strip()]
        if not chunks: raise ValueError("백서에서 텍스트를 추출하지 못했습니다.")
        vs.add_documents(chunks)
    return vs

# Uploads use an in-memory retriever isolated from other users and the whitepaper.
def rag_pipeline(filepath, collection_name=None):
    ensure_rag_imports()
    docs = PyMuPDF4LLMLoader(filepath).load()
    chunks = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100,
                separators=["\n\n", "\n", ".", " ", ""]).split_documents(docs)
    chunks = [d for d in chunks if d.page_content.strip()]
    if not chunks: raise ValueError("문서에서 텍스트를 추출하지 못했습니다.")
    from langchain_core.vectorstores import InMemoryVectorStore
    vs = InMemoryVectorStore.from_documents(chunks, OpenAIEmbeddings(model="text-embedding-3-small"))
    prompt = ChatPromptTemplate.from_messages([
        ("system", "문서 내용만 근거로 답하세요. 근거가 없으면 확인되지 않는다고 말하세요.\n{context}"),
        ("human", "{input}")])
    return ({"context": itemgetter("input") | vs.as_retriever(search_kwargs={"k":4}) | format_docs,
             "input": itemgetter("input")} | prompt | get_llm() | StrOutputParser())

# 4.2 백서 검색기: 벡터 + BM25(한글 2-gram) Hybrid, RRF로 합침
def kor_tokenize(text):
    tokens = re.findall(r"[A-Za-z0-9]+|[가-힣]+", text.lower())
    result = []
    for w in tokens:
        result.append(w)
        if re.match(r"[가-힣]", w) and len(w) >= 2:
            result += [w[i:i+2] for i in range(len(w) - 1)]
    return result


class SimpleBM25:
    """rank_bm25와 같은 BM25Okapi 계산 (추가 패키지 없이 구현)"""
    def __init__(self, docs, k1=1.5, b=0.75):
        self.docs = docs
        self.toks = [kor_tokenize(d.page_content) for d in docs]
        self.avgdl = sum(len(t) for t in self.toks) / max(len(self.toks), 1)
        self.tf = [Counter(t) for t in self.toks]
        df = Counter()
        for t in self.toks:
            df.update(set(t))
        n = len(self.toks)
        self.idf = {w: math.log((n - c + 0.5) / (c + 0.5) + 1) for w, c in df.items()}
        self.k1, self.b = k1, b

    def search(self, query, k=8):
        q = kor_tokenize(query)
        scores = []
        for i, tf in enumerate(self.tf):
            dl = len(self.toks[i])
            s = 0.0
            for w in q:
                if w in tf:
                    f = tf[w]
                    s += self.idf[w] * f * (self.k1 + 1) / (f + self.k1 * (1 - self.b + self.b * dl / self.avgdl))
            scores.append(s)
        order = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
        return [self.docs[i] for i in order[:k] if scores[i] > 0]


def rrf_merge(result_lists, weights, c=60, top_n=4):
    score, keep = {}, {}
    for docs, w in zip(result_lists, weights):
        for rank, d in enumerate(docs):
            key = d.page_content
            score[key] = score.get(key, 0) + w / (c + rank + 1)
            keep[key] = d
    best = sorted(score, key=score.get, reverse=True)[:top_n]
    return [keep[k] for k in best]


@st.cache_resource
def get_bm25():
    data = get_vectorstore()._collection.get(include=["documents", "metadatas"])
    docs = [Document(page_content=t, metadata=m or {}) for t, m in zip(data["documents"], data["metadatas"])]
    return SimpleBM25(docs) if docs else None


def hybrid_retrieve(query, k=4):
    vec = get_vectorstore().similarity_search(query, k=8)
    bm25 = get_bm25()
    kw = bm25.search(query, k=8) if bm25 else []
    return rrf_merge([kw, vec], [0.5, 0.5], top_n=k)


@st.cache_resource
def get_llm(streaming=True):
    ensure_rag_imports()
    return ChatOpenAI(model="gpt-4o-mini", streaming=streaming, temperature=0)

# 4.3 쿼리 리라이팅 (혜린님 규칙)
REWRITE_SYS = """당신은 KT AIVLE School 문서 검색을 위한 질의 재작성 도우미입니다.
대화 이력과 현재 질문을 참고하여, 이전 대화 없이도 의미를 이해할 수 있는 독립적인 검색 질문 한 개를 작성하세요.
규칙:
1. "그럼", "그 회사", "그 조건"처럼 생략된 대상을 대화에서 명확히 확인할 수 있을 때만 구체적으로 바꾸세요.
2. 현재 질문의 의미와 조건을 유지하세요.
3. 기수, 트랙, 기업명, 인물명, 숫자를 임의로 바꾸거나 추가하지 마세요.
4. 새로운 주제의 질문이면 이전 주제와 억지로 연결하지 마세요.
5. 이미 독립적으로 이해할 수 있는 질문이면 그대로 반환하세요.
6. 대화에 나온 이전 답변을 검증된 사실로 취급하지 마세요.
7. 답을 작성하지 말고 검색 질문만 한 줄로 출력하세요."""


def rewrite_question(question, history):
    ensure_rag_imports()
    if not history:
        return question
    prompt = ChatPromptTemplate.from_messages([
        ("system", REWRITE_SYS), MessagesPlaceholder("history"), ("human", "{input}")])
    chain = prompt | get_llm(False) | StrOutputParser()
    out = chain.invoke({"input": question, "history": history}).strip()
    return out or question

# 4.4 답변 프롬프트: rag_pipeline 규칙 + 프로필 + 현재 화면
ANSWER_SYS = """
당신은 KT AIVLE School 교육생과 예비 지원자를 돕는 'AIVLE School 학습 도우미'입니다.
1. 반드시 제공된 문서 내용(context)에 근거하여 답변하세요.
2. 문서에 없는 내용은 추측하지 말고 "업로드된 문서에서 확인되지 않습니다."라고 답한 뒤, 확인할 수 있는 곳(공식 홈페이지, AIVLE-EDU 공지, 담당 매니저 등)을 안내하세요.
3. 문서에 [추정], [후기], [언론] 표기가 있는 내용은 그 표기를 함께 알려 근거 수준을 밝히세요.
4. 일정, 자격, 지원금처럼 바뀔 수 있는 정보는 운영 공지 확인을 함께 안내하세요.
5. 답변은 간결하고 명확하게 목록 형태로 정리하고, 마지막에 바로 실천할 수 있는 한 줄 응원이나 도전 제안을 덧붙이세요.

[사용자 프로필]
{profile}

[사용자가 보고 있는 화면]
{screen}

[문서]
{context}"""


def answer_stream(question, history, profile_text, screen_text):
    """백서 기준 답변: 리라이팅 → Hybrid 검색 → 프로필·화면 반영 답변 (스트리밍)"""
    search_q = rewrite_question(question, history)
    docs = hybrid_retrieve(search_q, k=4)
    prompt = ChatPromptTemplate.from_messages([
        ("system", ANSWER_SYS), MessagesPlaceholder("history"), ("human", "{input}")])
    chain = prompt | get_llm(True) | StrOutputParser()
    stream = chain.stream({"input": question, "history": history, "profile": profile_text,
                           "screen": screen_text or "없음", "context": format_docs(docs)})
    return stream, docs, search_q

# ==========================================
# 6. 온톨로지 불러오기
# ==========================================
@st.cache_data
def load_ontology_text(raw):
    data = json.loads(raw)
    nodes = {n["id"]: n.get("type", "기타") for n in data.get("nodes", [])}
    links = data.get("links") or data.get("edges") or []
    edges = []
    for l in links:
        edges.append({"subject": l["source"], "relation": l.get("relation", "관련됨"),
                      "object": l["target"], "evidence": l.get("evidence", ""),
                      "page": l.get("page", ""),
                      "s_type": nodes.get(l["source"], "기타"), "o_type": nodes.get(l["target"], "기타")})
    return edges


TAB_RULES = {
    "교육": ({"과목", "미니프로젝트", "트랙", "규정"}, ["교육", "과목", "미니프로젝트", "출결", "수료", "장려금", "파이썬", "머신러닝", "딥러닝"]),
    "취업": ({"취업프로그램", "플랫폼", "자격"}, ["취업", "컨설팅", "면접", "잡페어", "인적성", "자기소개서", "플랫폼", "AICE"]),
    "포폴": (set(), ["포트폴리오", "프로젝트", "깃허브", "GitHub", "노션", "발표"]),
}


def edge_in_tab(e, tab):
    types, kws = TAB_RULES[tab]
    if e["s_type"] in types or e["o_type"] in types:
        return True
    text = f'{e["subject"]} {e["object"]} {e["evidence"]}'
    return any(k in text for k in kws)

def ask(question):
    st.session_state.pending_prompt = question

def save_archive():
    # Per-browser session only: never share chat history through a server JSON file.
    pass

# 3.2 프로필 단계별 설정 (예비 에이블러 / 에이블러 / 수료자)
STAGES = {
    "예비": {
        "label": "예비 에이블러", "emoji": "🌱",
        "desc": "지원·합격 발표·입교 준비 단계<br>지원 자격, 트랙 선택, 입교 전 준비",
        "focus": ["지원", "자격", "트랙", "역량", "입교", "파이썬"],
        "rule": "사용자는 아직 입교 전인 예비 지원자임. 일정은 정확한 날짜 대신 '교육 n주차' 또는 '○월 초·중·말 예정'처럼 대략적으로 안내함. 지원을 망설이지 않도록 도전을 응원하는 말로 마무리함.",
        "questions": ["비전공자도 따라갈 수 있나요?", "AI 개발자 트랙과 DX 트랙은 어떻게 달라요?",
                      "지원 자격과 선발 절차를 알려주세요.", "입교 전에 무엇을 준비하면 좋을까요?"],
    },
    "재학": {
        "label": "에이블러", "emoji": "🚀",
        "desc": "교육 과정 진행 중<br>출결·장려금, 미니프로젝트, 취업 일정",
        "focus": ["미니프로젝트", "출결", "장려금", "컨설팅", "포트폴리오", "AICE"],
        "rule": "사용자는 현재 교육 중인 에이블러임. 일정은 월/일 날짜로 정확히 안내하고, 신청 마감이 가까운 순서로 정리함.",
        "questions": ["훈련장려금은 얼마이고 어떤 조건에서 받나요?", "지각, 조퇴 기준과 수료 기준을 알려주세요.",
                      "포트폴리오·자소서·면접 컨설팅은 언제 신청하나요?", "DX 트랙 포트폴리오에는 어떤 프로젝트를 넣나요?"],
    },
    "수료": {
        "label": "수료자", "emoji": "🎓",
        "desc": "수료 후 1년간 맞춤 정보 제공<br>취업 준비, 잡페어, 면접, 선배 사례",
        "focus": ["취업", "잡페어", "면접", "자기소개서", "포트폴리오", "사례"],
        "rule": "사용자는 과정을 마친 수료생임. 일정은 월/일 날짜로 안내하고, 취업 준비와 선배 사례 중심으로 답함.",
        "questions": ["잡페어와 모의면접은 언제인가요?", "면접은 어떻게 준비하면 좋을까요?",
                      "선배들은 어떤 직무로 취업했나요?", "포트폴리오를 어떤 순서로 정리하면 좋을까요?"],
    },
}

# 3.4 날짜 표시
def fmt_event_date(start, end, stage):
    """재학·수료는 월/일 날짜, 예비는 n주차·○월 초/중/말 예정으로 표시"""
    if stage == "예비":
        week = (start - EDU_START).days // 7 + 1
        part = "초" if start.day <= 10 else ("중" if start.day <= 20 else "말")
        w = f"교육 {week}주차 · " if week >= 1 else ""
        return f"{w}{start.month}월 {part} 예정"
    s = f"{start.month}/{start.day:02d}({WEEKDAY[start.weekday()]})"
    if end != start:
        s += f" ~ {end.month}/{end.day:02d}({WEEKDAY[end.weekday()]})"
    return s


def dday_text(start, end, today):
    if start <= today <= end:
        return "진행 중"
    d = (start - today).days
    return f"D-{d}" if d > 0 else "종료"

EDU_START = date(2026,9,29)
EDU_END = date(2027,3,5)
WEEKDAY = ["월","화","수","목","금","토","일"]
def render_event_list(evs):
    lines = []
    for s, e, title, cat in evs:
        when = fmt_event_date(s, e, stage)
        st.markdown(f"""
        <div class="event-row">
            <span class="dday">{dday_text(s, e, today)}</span>
            <span class="tag tag-{cat}">{cat}</span><span class="event-title">{title}</span>
            <div class="event-date">{when}</div>
        </div>""", unsafe_allow_html=True)
        lines.append(f"{title}({when}, {dday_text(s, e, today)})")
    if not evs:
        st.caption("남은 일정이 없습니다.")
    return lines

# 10.4 취업과정 (체크리스트 공통 사용)
CHECKLISTS = {
    "취업": {
        "예비": ["지원 자격(연령·학력·미취업) 확인", "국민내일배움카드 발급 가능 여부 확인", "트랙 선택 이유 정리"],
        "재학": ["취업지원 플랫폼 회원가입", "포트폴리오 컨설팅 신청", "자기소개서 컨설팅 신청", "면접 컨설팅 신청", "잡페어 참여 기업 확인"],
        "수료": ["지원 직무 JD 3줄 분석", "포트폴리오 최신화", "면접 답변 경험 8문항 정리", "잡페어 후속 지원"],
    },
    "포폴": {
        "예비": ["지금까지의 프로젝트·경험 목록 만들기", "GitHub 계정 만들기"],
        "재학": ["프로젝트 1: 문제 정의부터 제안까지 간 대표 프로젝트", "프로젝트 2: 데이터로 근거를 만든 프로젝트",
                 "프로젝트 3: 문서화·제안·고객 소통이 보이는 프로젝트", "각 프로젝트에 개요·판단 과정·결과 그림 넣기"],
        "수료": ["지원 직무에 맞춰 프로젝트 순서 바꾸기", "빅프로젝트를 대표 프로젝트로 정리", "결과를 숫자로 표현"],
    },
}


def render_checklist(kind):
    items = CHECKLISTS[kind][stage]
    done = 0
    for i, item in enumerate(items):
        key = f"{kind}_{stage}_{i}"
        v = st.checkbox(item, value=st.session_state.checks.get(key, False), key=f"chk_{key}")
        st.session_state.checks[key] = v
        done += v
    st.progress(done / len(items), text=f"{done}/{len(items)} 완료")
    return f"체크리스트 {done}/{len(items)} 완료. 남은 항목: " + ", ".join(
        it for i, it in enumerate(items) if not st.session_state.checks.get(f"{kind}_{stage}_{i}"))


st.markdown('<style>\n.edu-hero {\n    background: linear-gradient(110deg, #dff5f6 0%, #eaf7fb 55%, #d9eff5 100%);\n    border-radius: 22px; padding: 25px 28px; margin: 8px 0 20px 0;\n    min-height: 145px; display: flex; align-items: center; justify-content: space-between;\n    box-shadow: 0 5px 18px rgba(50,80,100,0.05);\n}\n.edu-hero-title { color:#19334d; font-size:25px; font-weight:900; line-height:1.4; }\n.edu-hero-desc { color:#657d8e; font-size:14px; line-height:1.7; margin-top:8px; }\n.edu-hero-art { font-size:66px; white-space:nowrap; padding:0 15px; }\n.edu-section-head { display:flex; align-items:center; gap:10px; margin:17px 0 10px 0; color:#19334d; font-size:18px; font-weight:900; }\n.edu-section-no { background:#35b9c0; color:white; border-radius:9px; padding:4px 10px; font-size:13px; }\n.edu-track { border-radius:18px; padding:17px; min-height:112px; color:white; box-shadow:0 5px 15px rgba(50,80,100,.08); }\n.edu-track.ai { background:linear-gradient(110deg,#32b9c1,#39aebd); }\n.edu-track.dx { background:linear-gradient(110deg,#83b4f5,#659bea); }\n.edu-track h3 { color:white; font-size:19px; margin:0 0 6px 0; }\n.edu-track p { color:white; font-size:12px; margin:0; line-height:1.6; }\n.edu-track .track-icon { font-size:31px; float:left; margin-right:14px; }\n.edu-step { background:#f8fcfd; border:1px solid #e2f0f3; border-radius:17px; padding:13px 8px; text-align:center; min-height:128px; box-shadow:0 4px 12px rgba(50,80,100,.04); }\n.edu-step-icon { font-size:31px; }\n.edu-step-label { display:inline-block; background:#28aeb7; color:white; border-radius:12px; padding:3px 10px; font-size:10px; font-weight:800; margin:5px 0; }\n.edu-step-title { color:#19334d; font-size:14px; font-weight:900; }\n.edu-step-desc { color:#718697; font-size:11px; line-height:1.5; margin-top:5px; }\n.edu-topic { background:white; border:1px solid #eaf0f3; border-radius:16px; padding:13px 8px; min-height:105px; text-align:center; box-shadow:0 4px 12px rgba(50,80,100,.05); }\n.edu-topic-icon { font-size:27px; }\n.edu-topic-title { color:#19334d; font-weight:900; font-size:14px; margin-top:3px; }\n.edu-topic-desc { color:#8193a0; font-size:11px; margin-top:4px; line-height:1.4; }\n.edu-project { background:white; border:1px solid #e8eff3; border-radius:16px; padding:14px; margin-bottom:10px; box-shadow:0 4px 12px rgba(50,80,100,.05); }\n.edu-project h4 { color:#19334d; font-size:15px; margin:0 0 7px 0; }\n.edu-project p { color:#718697; font-size:11px; line-height:1.7; margin:0; }\n.edu-banner { background:linear-gradient(100deg,#087b88,#0b6575); color:white; border-radius:17px; padding:16px 22px; margin-top:16px; text-align:center; }\n.edu-banner strong { font-size:20px; }\n.edu-banner span { font-size:12px; opacity:.9; }\n.job-hero-title { color:#19334d; font-size:24px; font-weight:900; line-height:1.4; }\n.job-hero-desc { color:#20a6b6; font-size:14px; font-weight:700; line-height:1.7; margin-top:8px; }\n.job-hero-art { font-size:58px; white-space:nowrap; padding:0 12px; }\n.job-section-head { display:flex; align-items:center; gap:10px; margin:15px 0 9px; color:#19334d; font-size:17px; font-weight:900; }\n.job-section-no { background:#27b5bd; color:white; border-radius:9px; padding:4px 10px; font-size:12px; }\n.job-roadmap-card { border-radius:16px; padding:14px 8px; min-height:124px; text-align:center;\n    background:linear-gradient(145deg,#e4f8f7,#e8f3ff); border:1px solid #e2eff4; }\n.job-roadmap-icon { font-size:29px; }\n.job-roadmap-title { color:#19334d; font-weight:900; font-size:13px; margin-top:5px; }\n.job-roadmap-desc { color:#6e8292; font-size:10px; line-height:1.5; margin-top:5px; }\n.job-mini-card { background:white; border:1px solid #eaf0f3; border-radius:16px; padding:13px;\n    min-height:100px; box-shadow:0 4px 12px rgba(50,80,100,.05); margin-bottom:8px; }\n.job-mini-title { color:#19334d; font-size:13px; font-weight:900; margin-bottom:5px; }\n.job-mini-desc { color:#718697; font-size:11px; line-height:1.55; }\n.job-role-panel { background:#f7fbfd; border:1px solid #e7f0f4; border-radius:17px; padding:15px; min-height:210px; }\n.job-role-title { color:#19334d; font-size:15px; font-weight:900; margin-bottom:7px; }\n.job-role-desc { color:#718697; font-size:11px; line-height:1.65; }\n.job-role-row { color:#405a6e; font-size:11px; line-height:1.8; margin-top:7px; }\n.job-resource { background:white; border:1px solid #eaf0f3; border-radius:15px; padding:13px 6px;\n    min-height:92px; text-align:center; box-shadow:0 4px 12px rgba(50,80,100,.05); }\n.job-resource-icon { font-size:27px; }\n.job-resource-title { color:#19334d; font-size:12px; font-weight:900; margin-top:5px; }\n.job-content-panel { background:linear-gradient(110deg,#f5fbfc,#eef9fa); border-radius:17px; padding:15px 17px; min-height:150px; }\n.job-content-line { color:#405a6e; font-size:12px; line-height:1.9; }\n.job-bottom-banner { background:linear-gradient(100deg,#087b88,#0b6575); color:white; border-radius:17px;\n    padding:15px 20px; margin-top:15px; text-align:center; }\n.job-bottom-banner strong { font-size:19px; }\n.job-bottom-banner span { font-size:12px; opacity:.92; }.page-title{font-size:28px;font-weight:800;color:#19334d}.page-sub{color:#8294a4;margin-bottom:20px}.white-card{background:white;padding:24px;border-radius:18px;margin-bottom:18px}</style>', unsafe_allow_html=True)


# ==========================================
# 4. 세션 상태 초기화
# ==========================================
KST = ZoneInfo('Asia/Seoul')


def korea_today(now=None):
    """서버의 시간대와 무관하게 한국 날짜를 사용합니다."""
    return (now or datetime.now(KST)).astimezone(KST).date()


def event(eid, title, start, end=None, category='취업지원', mode='once',
          period='시간 미정', description='', source='백서 7.2.1 · 본문 51쪽'):
    return dict(id=eid, title=title, start=start, end=end or start,
                category=category, mode=mode, period=period,
                description=description, source=source)


# 종료일은 포함입니다. 연도 생략 일정은 10기 과정의 연속성을 따라 2026→2027로 정리했습니다.
# mode: once=기간 중 한 번 완료, daily=날짜별 완료, info=안내(체크 없음).
EVENTS = [
    event('day1-am', '코딩테스트 1차', '2026-11-13', category='교육', period='오전'),
    event('day1-pm', '취업지원 안내·포트폴리오 강의·네트워킹', '2026-11-13', period='오후'),
    event('mini4', '미니프로젝트 4차', '2026-11-16', '2026-11-17', '프로젝트', 'daily',
          description='백서·RAG 학습 도우미 구축. 각 날짜의 진행 완료를 체크합니다.', source='백서 3.2 · 본문 29쪽'),
    event('signup', '취업지원 플랫폼 회원가입', '2026-11-16', '2026-11-18',
          description='회원가입 후 구직희망 정보, 입사지원서, 포트폴리오를 등록합니다. 마감 시각은 백서에 명시되어 있지 않습니다.'),
    event('platform', '취업지원 플랫폼 이용 가능', '2026-11-16', '2027-09-05', mode='info'),
    event('ai-interview', 'AI 면접·AI 역량평가 연습', '2026-11-17', '2027-09-05', mode='info',
          description='해당 기간 최대 15회 연습 가능. 매일 의무적으로 해야 하는 할 일은 아닙니다.'),
    event('portfolio', '포트폴리오 컨설팅 신청', '2026-11-30', '2026-12-02',
          description='신청 기간입니다. 실제 컨설팅은 빅프로젝트 이전 진행하며 개인별 시간은 별도 안내됩니다.'),
    event('day2-am', '코딩테스트 2차', '2026-12-24', category='교육', period='오전'),
    event('day2-pm', 'AI 상상광고 챌린지·면접 전략 특강', '2026-12-24', period='오후',
          description='AIVLE Day 2. 클래스 네트워킹 포함.'),
    event('resume-consult', '자기소개서 컨설팅 신청', '2026-12-28', '2027-01-03',
          description='신청 기간입니다. 실제 컨설팅은 빅프로젝트 기간 중 진행됩니다.'),
    event('interview-consult', '면접 컨설팅 신청', '2027-01-20', '2027-01-22',
          description='신청 기간입니다. 실제 컨설팅은 빅프로젝트 기간 중 진행됩니다.'),
    event('refresh-project', '빅프로젝트 재정비', '2027-02-22', category='프로젝트', period='오전'),
    event('refresh-portfolio', '포트폴리오 재정비·실전 피칭 강의', '2027-02-22', period='오후'),
    event('presession', '발표회 프리세션', '2027-02-23', category='프로젝트', period='오전'),
    event('aptitude', '기업 인적성검사 대비·발표회 준비', '2027-02-23', period='오후'),
    event('presentation', '빅프로젝트 발표회', '2027-02-24', category='프로젝트', period='종일',
          description='백서에는 같은 날 클래스 네트워킹도 안내되어 있습니다.'),
    event('resume-class', '이력서·자기소개서 강의', '2027-02-25', period='오전'),
    event('resume-practice', '이력서·자기소개서 실습·잡서칭', '2027-02-25', period='오후'),
    event('jobfair', 'AIVLE 잡페어', '2027-02-26', period='종일', description='장소와 참여 기업은 추후 안내.'),
    event('mock-interview', '조별 모의면접·면접 스터디', '2027-03-02', '2027-03-03', mode='daily', period='오전'),
    event('jobsearch', '잡서칭 세션', '2027-03-02', '2027-03-03', mode='daily', period='오후'),
    event('platform-class', '취업 플랫폼 강의', '2027-03-04', period='오전'),
    event('platform-practice', '취업 플랫폼 실습', '2027-03-04', period='오후'),
    event('graduation', '에이블스쿨 수료', '2027-03-05', category='교육', source='백서 3.2 · 본문 30쪽'),
]


# 자격증 일정: 2026년 및 공식 발표가 확인된 2027년 1~3월.
# 종료일 포함. window는 개인 시험일이 아닌 시행기간이며 할 일 체크에서 제외합니다.
CERT_CHECKED = '2026-11-17'
CERT_EVENTS = []


def add_cert(cert, attempt, stage, start, end=None, *, url, window=False,
             note='', evidence='공식', period='시각은 시행기관 공지 확인', completion_id=None):
    eid = f'cert:{cert}:{attempt}:{stage}:{start}'
    CERT_EVENTS.append(dict(
        id=eid, title=f'{cert} · {attempt} · {stage}', start=start, end=end or start,
        category='자격증', type='자격증', attempt=attempt, stage=stage, mode='window' if window else 'once',
        period=period, description=note, memo=note, official=True, cert=cert,
        source=evidence + ' 일정 · 확인 ' + CERT_CHECKED, source_url=url,
        evidence=evidence, completion_id=completion_id or eid,
    ))


COS_ROWS = [
('71','2025-11-17','2026-01-15','2026-01-17'),
('72','2025-12-22','2026-02-19','2026-02-21'),
('73','2026-01-19','2026-03-19','2026-03-21'),
('74','2026-02-16','2026-04-16','2026-04-18'),
('75','2026-03-16','2026-05-14','2026-05-16'),
('76','2026-04-20','2026-06-18','2026-06-20'),
('77','2026-05-18','2026-07-16','2026-07-18'),
('78','2026-06-15','2026-08-13','2026-08-15'),
('79','2026-07-20','2026-09-17','2026-09-19'),
('80','2026-08-17','2026-10-15','2026-10-17'),
('81','2026-09-21','2026-11-19','2026-11-21'),
('82','2026-10-19','2026-12-17','2026-12-19'),
('83','2026-11-23','2027-01-21','2027-01-23'),
('84','2026-12-28','2027-02-25','2027-02-27'),
('85','2027-01-18','2027-03-18','2027-03-20'),
]
for attempt, start, end, exam in COS_ROWS:
    url = 'https://www.ybmit.com/cos_pro/cos_pro_info.jsp'
    add_cert('COS Pro 1급', attempt+'회', '접수', start, end, url=url)
    add_cert('COS Pro 1급', attempt+'회', '시험', exam, url=url, period='14:00')


def add_round(cert, attempt, row, url, written_window=True, note=''):
    # 필기 접수 시작/끝, 필기 시작/끝, 실기 접수 시작/끝, 실기 시작/끝
    a,b,c,d,e,f,g,h = ['2026-'+v for v in row.split()]
    add_cert(cert, attempt, '필기 접수', a, b, url=url, note=note)
    add_cert(cert, attempt, '필기 시험', c, d, url=url, window=written_window, note=note)
    if e == '2026-09-21':
        # 공휴일을 접수기간으로 잘못 포함하지 않도록 두 구간으로 표시합니다.
        key = cert+attempt+'실기접수'
        add_cert(cert, attempt, '실기 접수 1차 구간', e, '2026-09-23', url=url, completion_id=key)
        add_cert(cert, attempt, '실기 접수 2차 구간', '2026-09-28', url=url, completion_id=key)
    else:
        add_cert(cert, attempt, '실기 접수', e, f, url=url, note=note)
    add_cert(cert, attempt, '실기 시험', g, h, url=url, window=(g != h), note=note)


for attempt, row in [
('12회','03-03 03-09 04-04 04-04 05-18 05-22 06-20 06-20'),
('13회','08-03 08-07 09-05 09-05 10-26 10-30 11-28 11-28')]:
    add_round('빅데이터분석기사', attempt, row,
              'https://mods.go.kr/menu.es?mid=a10411020100', written_window=False)

ARTICLE_ROWS = {
'1회':'01-12 01-15 01-30 03-03 03-23 03-26 04-18 05-06',
'2회':'04-20 04-23 05-09 05-29 06-22 06-25 07-18 08-05',
'3회':'07-20 07-23 08-07 09-01 09-21 09-28 10-24 11-15',
}
for cert, code, rounds in [
('정보처리기사','1320',['1회','2회','3회']),
('정보처리산업기사','2290',['1회','2회','3회']),
('컴퓨터시스템기사','1998',['1회','3회'])]:
    for attempt in rounds:
        row = ARTICLE_ROWS[attempt]
        if cert == '정보처리산업기사' and attempt == '3회':
            row = row.replace('11-15','11-13')
        note = ('구 전자계산기기사·전자계산기조직응용기사 통합 종목. 변경된 명칭의 AX 인정 여부는 교육 운영진 확인.'
                if cert == '컴퓨터시스템기사' else '')
        add_round(cert, attempt, row,
                  f'https://www.q-net.or.kr/crf005.do?id=crf00503s02&jmCd={code}&jmInfoDivCcd=B0', note=note)

for attempt, row in [
('1회','01-06 01-09 01-20 01-24 02-02 02-05 03-14 04-05'),
('2회','03-16 03-20 04-04 04-09 04-27 04-30 05-30 06-14'),
('3회','06-08 06-11 06-27 07-02 07-27 07-30 08-29 09-16'),
('4회','08-24 08-27 09-16 09-21 10-12 10-15 11-14 12-02')]:
    add_round('프로그래밍기능사', attempt, row,
              'https://www.q-net.or.kr/crf005.do?id=crf00503s02&jmCd=6921&jmInfoDivCcd=A0',
              note='구 정보처리기능사. 변경된 명칭의 AX 인정 여부는 교육 운영진 확인.')

TECH_ROWS = {
'138회':'01-06 01-09 02-07 03-03 03-06 03-30 04-02 05-02 05-16',
'139회':'04-13 04-16 05-16 06-08 06-11 06-29 07-02 08-01 08-15',
'140회':'07-13 07-16 08-22 08-31 09-03 10-12 10-15 11-14 11-28',
}
for cert, code, rounds in [('정보관리기술사','0601',list(TECH_ROWS)),
                            ('컴퓨터시스템응용기술사','0622',['138회','140회'])]:
    url = f'https://www.q-net.or.kr/crf005.do?id=crf00503s02&jmCd={code}'
    for attempt in rounds:
        a,b,c,d,e,f,g,h,i = ['2026-'+v for v in TECH_ROWS[attempt].split()]
        add_cert(cert,attempt,'필기 접수',a,b,url=url)
        add_cert(cert,attempt,'필기 시험',c,url=url)
        for label, start, end in [('1차',d,e),('2차',f,g)]:
            add_cert(cert,attempt,'면접 접수 '+label,start,end,url=url,
                     note='필기 면제·합격 등 응시자 구분에 따라 적용되는 접수기간이 다릅니다.',
                     completion_id=cert+attempt+'면접접수')
        add_cert(cert,attempt,'면접 시험',h,i,url=url,window=True)

for cert in ['정보보안기사','정보보안산업기사']:
    for attempt, row in [
    ('1회','01-26 01-29 02-09 03-06 03-16 03-19 04-11 04-26'),
    ('2회','05-11 05-14 05-22 06-15 06-22 06-25 07-25 08-09'),
    ('4회','08-31 09-03 09-14 10-08 10-19 10-22 11-14 11-29')]:
        add_round(cert,attempt,row,'https://www.cq.or.kr/qh_quagm03_001.do',
                  note='연간 시행계획의 기간입니다. 종목별 실제 응시일은 회차별 공고·수험표로 확인하세요.')

for attempt, exam in [('1차','2026-08-08'),('2차','2026-10-31')]:
    add_cert('소프트웨어 보안약점 진단원',attempt,'시험',exam,
             url='https://www.kisa.or.kr/401/form?postSeq=3681',
             note='기본교육 이수 등 응시요건 확인 필요. 접수기간은 확인되지 않아 미등록.')

for attempt, deadline, exam, url in [
('63회','2026-05-15','2026-05-30','https://www.ipmc.kr/board/read.jsp?code=notice&id=1941706&ln=board&page=13'),
('64회','2026-11-06','2026-11-21','https://www.ipmc.kr/board/read.jsp?code=notice&id=1966256')]:
    for stage, day in [('접수 마감',deadline),('필기 시험',exam)]:
        add_cert('IT-PMP',attempt,stage,day,url=url,evidence='교육기관 게재 공고',
                 note='시행기관 원문 미대조. 접수 시작일 미확인. 기본 표시에서 제외.')
    if attempt == '63회':
        add_cert('IT-PMP',attempt,'면접 시험','2026-06-20',url=url,evidence='교육기관 게재 공고')

# 공식 문서 대조: 사용자 확인(2026-11-17). 원문 파일 자체는 앱에 포함하지 않습니다.
for attempt, row in [
    ('36회', '01-05 01-09 02-07 02-07 03-30 04-03 05-02 05-02'),
    ('37회', '07-06 07-10 08-08 08-08 09-14 09-18 10-17 10-17'),
]:
    add_round('데이터분석전문가(ADP)', attempt, row,
              'https://www.dataq.or.kr/', written_window=False)
for attempt, start, end, exam in [
    ('65회', '2026-02-09', '2026-02-13', '2026-03-21'),
    ('66회', '2026-08-14', '2026-08-21', '2026-09-19'),
]:
    add_cert('데이터아키텍처전문가(DAP)', attempt, '접수', start, end,
             url='https://www.dataq.or.kr/')
    add_cert('데이터아키텍처전문가(DAP)', attempt, '시험', exam,
             url='https://www.dataq.or.kr/')
for item in CERT_EVENTS:
    if item['cert'] in ('데이터분석전문가(ADP)', '데이터아키텍처전문가(DAP)'):
        item['source'] = 'DataQ 공식 문서 · 사용자 대조 확인 2026-11-17'
        item['evidence'] = '공식 문서 · 사용자 확인'

# 접수 목적지와 일정 근거 URL은 별개로 관리합니다.
def registration_destination(cert):
    if cert == 'COS Pro 1급':
        return ('https://www.ybmit.com/test_rec/gen_rec.jsp', '시험 접수하기',
                'COS Pro 선택 후 로그인하여 접수하세요.')
    if cert in ('빅데이터분석기사', '데이터분석전문가(ADP)', '데이터아키텍처전문가(DAP)'):
        return ('https://www.dataq.or.kr/', 'DataQ 접수 사이트로 이동',
                '로그인 → 원서접수에서 종목을 선택하세요.')
    if cert in ('정보보안기사', '정보보안산업기사'):
        return ('https://www.cq.or.kr/main.do', 'KCA 접수 사이트로 이동',
                '국가자격 원서접수 → 로그인 후 종목을 선택하세요.')
    if cert == '소프트웨어 보안약점 진단원':
        return ('https://swsca.kr/', '진단원 시험 신청 창구로 이동',
                'SW개발보안 교육 전용창구에서 이수시험을 신청하세요.')
    if cert == 'IT-PMP':
        return ('http://www.pmo.or.kr/', 'IT-PMP 접수 사이트로 이동',
                '원서접수 메뉴를 이용하세요. 접속이 안 되면 공고의 이메일 접수 방법을 확인하세요.')
    return ('https://www.q-net.or.kr/rcv202.do?gId=&gSite=Q&id=rcv20210',
            'Q-Net 원서접수 신청', '로그인 후 종목과 회차를 선택하세요.')


CERT_NAMES = sorted({e['cert'] for e in CERT_EVENTS})
DEFAULT_CERTS = [name for name in CERT_NAMES if name != 'IT-PMP']


def remember_cert_filter():
    st.session_state.cert_preferences = list(st.session_state.cert_filter)


def visible_events():
    chosen = st.session_state.get('cert_preferences', DEFAULT_CERTS)
    return [e for e in st.session_state.calendar_events
            if not e.get('cert') or e['cert'] in chosen]


def nearest_cert_exams(day):
    """선택일 이후(진행 중 포함) 자격증별 가장 가까운 시험 한 개."""
    visible = [e for e in visible_events() if e.get('cert')]
    nearest = []
    for cert in st.session_state.get('cert_preferences', DEFAULT_CERTS):
        exams = [e for e in visible if e['cert'] == cert
                 and '접수' not in e['stage'] and date.fromisoformat(e['end']) >= day]
        if not exams:
            continue
        exam = min(exams, key=lambda e: (max(e['start'], day.isoformat()), e['end'], e['id']))
        phase = exam['stage'].replace(' 시험', '')
        registrations = [e for e in visible
                         if e['cert'] == cert and e['attempt'] == exam['attempt']
                         and '접수' in e['stage']
                         and (phase == '시험' or e['stage'].startswith(phase))]
        nearest.append((exam, sorted(registrations, key=lambda e: e['start'])))
    return sorted(nearest, key=lambda pair: (max(pair[0]['start'], day.isoformat()), pair[0]['cert']))


def task_key(item, day):
    return item.get('completion_id', item['id']) + (':' + day.isoformat() if item.get('mode') == 'daily' else '')


def update_done(task_id, widget_key):
    st.session_state.calendar_done[task_id] = st.session_state[widget_key]


def navigate(page):
    st.session_state.active_page = page


st.session_state.setdefault('active_page', 'home')
st.session_state.setdefault('calendar_done', {})

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None

# 달력/출결/일정 데이터
if "calendar_month" not in st.session_state:
    st.session_state.calendar_month = korea_today().replace(day=1)

if "selected_calendar_date" not in st.session_state:
    st.session_state.selected_calendar_date = korea_today()

if "calendar_events" not in st.session_state:
    st.session_state.calendar_events = [
        {**e, 'type': e['category'], 'memo': e['description'], 'official': True}
        for e in EVENTS
    ]

# 공식 시험 데이터만 갱신하며 개인 일정과 완료 기록은 유지합니다.
st.session_state.calendar_events = [
    e for e in st.session_state.calendar_events if not e.get('cert')
] + CERT_EVENTS
st.session_state.setdefault('cert_preferences', DEFAULT_CERTS.copy())

if "attendance_records" not in st.session_state:
    st.session_state.attendance_records = {}


def events_on(day):
    """해당 날짜에 진행 중인 일정 목록을 반환합니다."""
    result = []
    for event in visible_events():
        start = date.fromisoformat(event["start"])
        end = date.fromisoformat(event["end"])
        if start <= day <= end:
            result.append(event)
    return result


# 검색창 콜백
def submit_search():

    value = st.session_state.get(
        "search_input", ""
    ).strip()

    if value:
        st.session_state.pending_prompt = value


# ==========================================
# 5. 사이드바
# ==========================================
def page_intro():
    st.markdown('<div class="page-title">🙋 에이블스쿨 소개</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="page-sub">{S["label"]}에게 맞춘 소개 · 자세한 내용은 오른쪽 챗봇에 물어보세요</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="white-card">
    <b>KT 에이블스쿨(AIVLE School)</b>은 고용노동부 'KDT 첨단산업·디지털 선도기업 아카데미' 사업으로 운영되는
    청년 대상 AI·클라우드 실무 인재 양성 과정임. 10기는 2026.9.29 ~ 2027.3.5, 총 106일 840시간임.
    </div>""", unsafe_allow_html=True)
    t1, t2 = st.columns(2, gap="medium")
    with t1:
        st.markdown("""<div class="white-card"><b>🤖 AI 개발자 트랙</b><br><br>
        AI와 Cloud로 서비스를 구현하는 개발자<br>코드를 짜서 무언가를 만드는 데서 보람을 느끼는 사람</div>""",
                    unsafe_allow_html=True)
    with t2:
        st.markdown("""<div class="white-card"><b>📊 DX 컨설턴트 트랙</b><br><br>
        AI와 Cloud로 기업의 디지털 전환을 주도하는 촉진자<br>문제를 정의하고 근거를 들어 설득하는 데 강점이 있는 사람</div>""",
                    unsafe_allow_html=True)
    return "에이블스쿨 소개 화면(운영 기관, 10기 기간, AI 개발자 트랙과 DX 컨설턴트 트랙 비교)"
def page_edu():
    """참고 이미지의 AIVLE School 교육과정 대시보드 화면."""
    st.html("""
    <div class="page-title">📚 교육과정</div>
    <div class="page-sub">AIVLE School Curriculum</div>
    <div class="edu-hero">
      <div>
        <div class="edu-hero-title">배움에서 실무까지, 성장의 여정 🚀</div>
        <div class="edu-hero-desc">체계적인 교육과 프로젝트를 통해<br>AI·DX 실무 역량을 키워보세요.</div>
      </div>
      <div class="edu-hero-art">📊 🤖 💻</div>
    </div>
    <div class="edu-section-head"><span class="edu-section-no">01.</span> 교육 트랙 선택</div>
    """)

    track1, track2 = st.columns(2, gap="small")
    with track1:
        st.html("""<div class="edu-track ai"><div class="track-icon">💻</div><h3>AI 개발자 트랙</h3><p>AI 모델 개발 및 서비스 구현 중심 교육<br><b>AI Developer</b></p></div>""")
    with track2:
        st.html("""<div class="edu-track dx"><div class="track-icon">📊</div><h3>DX 컨설턴트 트랙</h3><p>데이터 분석과 AI를 활용한 비즈니스 문제 해결<br><b>DX Consultant</b></p></div>""")

    st.html('<div class="edu-section-head"><span class="edu-section-no">02.</span> 교육 진행 로드맵</div>')
    steps = [
        ("💻", "STEP 01", "기초 역량 학습", "Python, SQL,<br>데이터 분석 등"),
        ("⚙️", "STEP 02", "AI·DX 심화 학습", "머신러닝, 딥러닝,<br>생성형 AI, 클라우드"),
        ("👥", "STEP 03", "미니 프로젝트", "학습한 기술을 활용한<br>실습 및 팀 프로젝트"),
        ("🚀", "STEP 04", "빅 프로젝트", "실제 비즈니스 문제 해결 및<br>서비스 구현")
    ]
    step_cols = st.columns(4, gap="small")
    for col, (icon, label, title, desc) in zip(step_cols, steps):
        with col:
            st.html(f'<div class="edu-step"><div class="edu-step-icon">{icon}</div><div class="edu-step-label">{label}</div><div class="edu-step-title">{title}</div><div class="edu-step-desc">{desc}</div></div>')

    st.html('<div class="edu-section-head"><span class="edu-section-no">03.</span> 주요 학습 분야</div>')
    topics = [
        ("🐍", "Python", "프로그래밍 기초 및<br>데이터 처리"),
        ("📊", "데이터 분석", "데이터 전처리·분석·시각화"),
        ("🛢️", "SQL", "데이터베이스·데이터 조회"),
        ("🤖", "머신러닝", "AI 모델 학습과 평가"),
        ("🧠", "딥러닝", "신경망 기반 모델 학습"),
        ("✨", "생성형 AI", "LLM, 프롬프트 엔지니어링,<br>RAG 활용")
    ]
    topic_rows = [topics[:3], topics[3:]]
    for row in topic_rows:
        cols = st.columns(3, gap="small")
        for col, (icon, title, desc) in zip(cols, row):
            with col:
                st.html(f'<div class="edu-topic"><div class="edu-topic-icon">{icon}</div><div class="edu-topic-title">{title}</div><div class="edu-topic-desc">{desc}</div></div>')

    st.html('<div class="edu-section-head"><span class="edu-section-no">04.</span> 프로젝트 학습</div>')
    project_col1, project_col2 = st.columns(2, gap="small")
    with project_col1:
        st.html("""<div class="edu-project"><h4>📋 미니 프로젝트</h4><p>✔ 학습 내용을 실제로 적용<br>✔ 개인 및 팀 기반 프로젝트 수행<br>✔ 결과 발표 및 피드백</p></div>""")
    with project_col2:
        st.html("""<div class="edu-project"><h4>🚀 빅 프로젝트</h4><p>✔ 실제 비즈니스 문제 발굴<br>✔ AI 기반 서비스 기획 및 구현<br>✔ 최종 결과물 발표 및 성과 공유</p></div>""")

    st.html("""<div class="edu-banner"><strong>△　Your Future Starts Here!</strong><br><span>AIVLE School과 함께 실무형 인재로 성장해 보세요.</span></div>""")
def page_job():
    """참고 이미지 기반 취업 준비 대시보드."""
    st.html("""
    <div class="page-title">💼 취업과정</div>
    <div class="page-sub">Career &amp; Job Preparation</div>
    <div class="job-hero">
      <div>
        <div class="job-hero-title">AIVLE School 취업 준비 가이드</div>
        <div class="job-hero-desc">학습부터 포트폴리오, 면접까지<br>실무형 취업 역량을 완성해 보세요!</div>
      </div>
      <div class="job-hero-art">📋 👩🏻‍💻 📊</div>
    </div>
    <div class="job-section-head"><span class="job-section-no">01.</span> 취업 준비 로드맵</div>
    """)

    roadmap = [
        ("🎯", "직무 탐색", "관심 직무 이해 및<br>요구 역량 파악"),
        ("📚", "역량 강화", "교육 과정 기반<br>핵심 역량 확보"),
        ("💻", "포트폴리오", "프로젝트 정리 및<br>성과 도출"),
        ("📄", "서류 준비", "이력서·자기소개서<br>작성"),
        ("👥", "면접 대비", "기술·인성 면접 및<br>실전 연습"),
    ]
    roadmap_cols = st.columns(5, gap="small")
    for col, (icon, title, desc) in zip(roadmap_cols, roadmap):
        with col:
            st.html(f"""
            <div class="job-roadmap-card">
              <div class="job-roadmap-icon">{icon}</div>
              <div class="job-roadmap-title">{title}</div>
              <div class="job-roadmap-desc">{desc}</div>
            </div>
            """)

    st.html('<div class="job-section-head"><span class="job-section-no">02.</span> 주요 취업 지원 프로그램</div>')
    left_programs, right_role = st.columns([1.05, 1.2], gap="small")

    with left_programs:
        programs = [
            ("🎓", "취업 특강", "현직자 직무 특강 및<br>채용 트렌드 안내"),
            ("📄", "자소서 클리닉", "자기소개서 작성법과<br>1:1 피드백"),
            ("👥", "모의 면접", "실전형 면접 연습 및<br>개별 피드백"),
            ("🏢", "채용 연계", "협력사 및 채용 정보<br>탐색과 지원"),
        ]
        for row in (programs[:2], programs[2:]):
            cols = st.columns(2, gap="small")
            for col, (icon, title, desc) in zip(cols, row):
                with col:
                    st.html(f"""
                    <div class="job-mini-card">
                      <div class="job-mini-title">{icon}　{title}</div>
                      <div class="job-mini-desc">{desc}</div>
                    </div>
                    """)

    with right_role:
        st.html('<div class="job-section-head" style="margin-top:0;"><span class="job-section-no">03.</span> 직무별 정보</div>')
        role = st.radio(
            "직무 선택",
            ["DX 컨설턴트", "AI 개발자"],
            horizontal=True,
            label_visibility="collapsed",
            key="job_role_choice"
        )
        if role == "DX 컨설턴트":
            role_title = "DX 컨설턴트 (DX Consultant)"
            role_desc = "데이터와 AI를 활용해 기업의 비즈니스 문제를 분석하고, 디지털 전환을 기획·제안하는 직무입니다."
            duties = [
                ("주요 업무", "데이터 분석, DX 과제 기획, 솔루션 제안"),
                ("요구 역량", "데이터 분석력, 비즈니스 이해, 커뮤니케이션"),
                ("연관 직무", "데이터 분석가, IT기획, PM, BI 개발자 등"),
            ]
            role_icon = "📊"
        else:
            role_title = "AI 개발자 (AI Developer)"
            role_desc = "AI·머신러닝 기술을 활용해 모델과 서비스를 개발하고 실제 업무에 적용하는 직무입니다."
            duties = [
                ("주요 업무", "데이터 전처리, 모델 개발·평가, AI 서비스 구현"),
                ("요구 역량", "Python, 머신러닝·딥러닝, 알고리즘"),
                ("연관 직무", "AI 엔지니어, ML 엔지니어, 백엔드 개발자 등"),
            ]
            role_icon = "💻"

        st.html(f"""
        <div class="job-role-panel">
          <div class="job-role-title">{role_icon}　{role_title}</div>
          <div class="job-role-desc">{role_desc}</div>
          <div class="job-role-row">""" + "".join(
              f"<b>✓　{label}</b>　{desc}<br>" for label, desc in duties
          ) + """</div>
        </div>
        """)

    resources_col, contents_col = st.columns([1.2, 1], gap="small")
    with resources_col:
        st.html('<div class="job-section-head"><span class="job-section-no">04.</span> 취업 준비 자료실</div>')
        resources = [
            ("📄", "이력서 템플릿"),
            ("🖊️", "자기소개서 가이드"),
            ("💬", "면접 질문 모음"),
            ("📁", "포트폴리오 예시"),
        ]
        resource_cols = st.columns(4, gap="small")
        for col, (icon, title) in zip(resource_cols, resources):
            with col:
                st.html(f"""
                <div class="job-resource">
                  <div class="job-resource-icon">{icon}</div>
                  <div class="job-resource-title">{title}</div>
                </div>
                """)

    with contents_col:
        st.html('<div class="job-section-head"><span class="job-section-no">05.</span> 추천 학습 콘텐츠</div>')
        st.html("""
        <div class="job-content-panel">
          <div class="job-content-line">
            <b style="color:#20ad91;">✓</b>　프로젝트 경험 정리 및 성과 수치화 방법<br>
            <b style="color:#20ad91;">✓</b>　데이터·AI 직무 면접 대비 예상 질문<br>
            <b style="color:#20ad91;">✓</b>　포트폴리오 구성 및 발표 팁<br>
            <b style="color:#20ad91;">✓</b>　기업별 채용 공고 및 자격 요건 정리
          </div>
        </div>
        """)

    st.html("""
    <div class="job-bottom-banner">
      <strong>△　Next Career with AIVLE School!</strong><br>
      <span>AIVLE School과 함께, 실무 역량을 취업으로 연결하세요.</span>
    </div>
    """)

    # 개인별 취업 준비 체크리스트
    with st.expander("✅ 나의 취업 준비 체크리스트", expanded=False):
        phase = st.selectbox(
            "현재 준비 단계",
            ["예비", "재학", "수료"],
            index=1,
            key="job_check_phase"
        )
        checklist = {
            "예비": [
                "지원 자격(연령·학력·미취업) 확인",
                "관심 직무 2개 이상 탐색",
                "지금까지의 프로젝트·경험 목록 만들기"
            ],
            "재학": [
                "지원 직무와 요구 역량 정리",
                "포트폴리오 대표 프로젝트 선정",
                "자기소개서 초안 작성",
                "모의 면접 또는 취업 특강 참여",
                "채용 공고 및 잡페어 참여 기업 확인"
            ],
            "수료": [
                "지원 직무 JD 분석",
                "포트폴리오 최신화",
                "면접 답변 경험 8문항 정리",
                "관심 기업 지원 및 후속 일정 관리"
            ]
        }
        done = 0
        items = checklist[phase]
        for idx, item in enumerate(items):
            check_id = f"job_check_{phase}_{idx}"
            checked = st.checkbox(item, key=check_id,
                value=st.session_state.checks.get(check_id, False))
            st.session_state.checks[check_id] = checked
            done += int(checked)
        st.progress(done / len(items), text=f"{done}/{len(items)}개 완료")
def page_portfolio():

    st.markdown("""
    <style>
    .portfolio-banner {
        background: linear-gradient(110deg, #dff7f8, #e7f4ff);
        border-radius: 20px;
        padding: 27px;
        margin: 15px 0 20px 0;
        color: #19334d;
    }
    .portfolio-banner h2 {
        font-size: 25px;
        font-weight: 800;
        margin-bottom: 10px;
    }
    .portfolio-banner p {
        font-size: 15px;
        line-height: 1.8;
        color: #526d83;
    }
    .portfolio-card {
        background: white;
        border-radius: 17px;
        padding: 20px 10px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(50,80,100,0.06);
        min-height: 115px;
    }
    .portfolio-card h3 {
        color: #19334d;
        font-size: 17px;
        margin: 8px 0;
    }
    .portfolio-card p {
        color: #8294a4;
        font-size: 12px;
    }
    .portfolio-section {
        font-size: 19px;
        font-weight: 800;
        color: #19334d;
        margin: 18px 0 12px 0;
    }
    .portfolio-info {
        background: #e4f8f7;
        padding: 15px;
        border-radius: 14px;
        color: #19334d;
        line-height: 1.9;
        margin-top: 10px;
    }
    .senior-card {
        background: white;
        border: 1px solid #e6edf3;
        border-radius: 14px;
        padding: 14px;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

    # 상단 제목
    st.markdown(
        '<div class="page-title">📁 포트폴리오</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="page-sub">Portfolio | 나만의 프로젝트 경험을 가치 있는 포트폴리오로!</div>',
        unsafe_allow_html=True
    )

    # 상단 배너
    st.markdown("""
    <div class="portfolio-banner">
        <h2>프로젝트 경험을 가치 있는 포트폴리오로! ✨</h2>
        <p>
        작성부터 AI 피드백, 선배 사례까지<br>
        AIVLE School이 포트폴리오 완성을 도와드립니다.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 퀵 메뉴
    st.markdown('<div class="portfolio-section">⭐ Portfolio Menu</div>',
                unsafe_allow_html=True)

    q1, q2, q3, q4 = st.columns(4)

    with q1:
        st.markdown("""
        <div class="portfolio-card">
            <div style="font-size:32px;">✏️</div>
            <h3>포트폴리오 작성</h3>
            <p>템플릿으로 쉽게 작성</p>
        </div>
        """, unsafe_allow_html=True)

    with q2:
        st.markdown("""
        <div class="portfolio-card">
            <div style="font-size:32px;">✨</div>
            <h3>AI 피드백 받기</h3>
            <p>완성도 분석 및 개선 제안</p>
        </div>
        """, unsafe_allow_html=True)

    with q3:
        st.markdown("""
        <div class="portfolio-card">
            <div style="font-size:32px;">📂</div>
            <h3>선배 포트폴리오</h3>
            <p>우수 사례 확인 및 참고</p>
        </div>
        """, unsafe_allow_html=True)

    with q4:
        st.markdown("""
        <div class="portfolio-card">
            <div style="font-size:32px;">📖</div>
            <h3>작성 가이드</h3>
            <p>구성·작성법·예시 제공</p>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    # ==========================================
    # 01. 포트폴리오 작성
    # ==========================================
    left, right = st.columns([1, 1], gap="medium")

    with left:
        st.markdown('<div class="portfolio-section">01. 📝 포트폴리오 작성하기</div>',
                    unsafe_allow_html=True)

        write_tab, saved_tab = st.tabs(["✏️ 새로 작성하기", "📁 내 포트폴리오"])

        with write_tab:

            template = st.radio(
                "작성 템플릿 선택",
                [
                    "프로젝트 중심 템플릿",
                    "취업용 종합 템플릿",
                    "데이터·AI 특화 템플릿"
                ],
                horizontal=False,
                key="portfolio_template"
            )

            with st.form("portfolio_write_form"):

                st.markdown("#### 기본 정보")

                project_name = st.text_input(
                    "프로젝트명",
                    placeholder="예: 고객 VOC 분석 기반 AI 서비스"
                )

                target_job = st.selectbox(
                    "지원 희망 직무",
                    ["DX 컨설턴트", "AI 개발자", "데이터 분석가",
                     "BI 개발자", "IT 기획/PM", "기타"]
                )

                period = st.text_input(
                    "프로젝트 기간",
                    placeholder="예: 2026.10 ~ 2026.11"
                )

                st.markdown("#### 프로젝트 상세 내용")

                problem = st.text_area(
                    "1. 프로젝트 배경 및 문제 정의",
                    placeholder="어떤 문제를 해결하기 위해 프로젝트를 시작했나요?",
                    height=90
                )

                goal = st.text_area(
                    "2. 프로젝트 목표",
                    placeholder="프로젝트를 통해 달성하고자 한 목표를 작성하세요.",
                    height=80
                )

                role = st.text_area(
                    "3. 본인의 역할",
                    placeholder="담당한 업무와 기여 내용을 작성하세요.",
                    height=80
                )

                technology = st.text_input(
                    "4. 활용 기술",
                    placeholder="예: Python, SQL, Pandas, LangChain, RAG"
                )

                result = st.text_area(
                    "5. 프로젝트 성과 및 결과",
                    placeholder="정량적·정성적 성과를 작성하세요.",
                    height=90
                )

                learned = st.text_area(
                    "6. 배운 점 및 개선 사항",
                    placeholder="프로젝트를 통해 배운 점과 향후 개선 방향",
                    height=80
                )

                submitted = st.form_submit_button(
                    "✏️ 포트폴리오 저장하기",
                    use_container_width=True
                )

                if submitted:

                    if not project_name.strip():
                        st.warning("프로젝트명을 입력해 주세요.")

                    else:
                        portfolio = {
                            "프로젝트명": project_name,
                            "지원 직무": target_job,
                            "기간": period,
                            "템플릿": template,
                            "문제 정의": problem,
                            "프로젝트 목표": goal,
                            "담당 역할": role,
                            "활용 기술": technology,
                            "성과": result,
                            "배운 점": learned
                        }

                        if "my_portfolios" not in st.session_state:
                            st.session_state.my_portfolios = []

                        st.session_state.my_portfolios.append(portfolio)

                        st.success("포트폴리오가 저장되었습니다!")

        with saved_tab:

            st.markdown("#### 📁 내가 작성한 포트폴리오")

            saved = st.session_state.get("my_portfolios", [])

            if saved:

                for i, p in enumerate(saved):

                    with st.expander(f"📄 {p['프로젝트명']}"):

                        for key, value in p.items():
                            if value:
                                st.markdown(f"**{key}**")
                                st.write(value)

                        if st.button(
                            "🗑️ 삭제",
                            key=f"delete_portfolio_{i}"
                        ):
                            st.session_state.my_portfolios.pop(i)
                            st.rerun()

            else:
                st.info("아직 작성한 포트폴리오가 없습니다.")

    # ==========================================
    # 02. AI 피드백
    # ==========================================
    with right:

        st.markdown('<div class="portfolio-section">02. 🤖 AI 포트폴리오 피드백</div>',
                    unsafe_allow_html=True)

        st.markdown("""
        <div class="portfolio-info">
        <b>📤 포트폴리오 파일을 업로드하세요.</b><br>
        PDF, PPTX, DOCX 파일을 지원합니다.<br>
        AI가 포트폴리오의 완성도를 분석할 수 있도록 준비합니다.
        </div>
        """, unsafe_allow_html=True)

        feedback_file = st.file_uploader(
            "포트폴리오 파일 선택",
            type=["pdf", "pptx", "docx"],
            key="portfolio_feedback_file"
        )

        if feedback_file:

            st.success(f"파일 업로드 완료: {feedback_file.name}")

            st.markdown("#### ✨ AI 피드백 분석 기준")

            st.markdown("""
            <div class="portfolio-info">
            ✅ 프로젝트 설명의 구체성과 논리 흐름 분석<br>
            ✅ 성과(정량·정성) 표현의 적절성 평가<br>
            ✅ 지원 직무 관점의 강점과 보완점 제안<br>
            ✅ 구성, 가독성, 디자인 개선 가이드 제공
            </div>
            """, unsafe_allow_html=True)

            st.info("현재 파일 업로드 기능이 연결되었습니다. 실제 AI 분석은 기존 RAG/LLM 체인과 연결해야 합니다.")

        else:
            st.info("포트폴리오 파일을 업로드하면 피드백 분석을 준비할 수 있습니다.")

    st.write("")

    # ==========================================
    # 03. 선배 포트폴리오
    # ==========================================
    st.markdown('<div class="portfolio-section">03. 👥 포트폴리오 구성 예시</div>',
                unsafe_allow_html=True)

    filter1, filter2 = st.columns([2, 1])

    with filter1:
        job_filter = st.selectbox(
            "직무별 포트폴리오",
            ["전체", "DX 컨설턴트", "AI 개발자"],
            key="senior_job_filter"
        )

    with filter2:
        project_filter = st.selectbox(
            "프로젝트 유형",
            ["전체", "데이터 분석", "AI·ML", "서비스 개발"],
            key="senior_project_filter"
        )

    seniors = [
        {
            "직무": "DX 컨설턴트",
            "유형": "데이터 분석",
            "제목": "VOC 분석 기반 AI 고객상담 지원 서비스",
            "기술": "Python · RAG · 데이터분석"
        },
        {
            "직무": "AI 개발자",
            "유형": "AI·ML",
            "제목": "이미지 분류 기반 품질 검사 시스템",
            "기술": "딥러닝 · 모델링 · Flask"
        },
        {
            "직무": "DX 컨설턴트",
            "유형": "데이터 분석",
            "제목": "공공데이터 분석을 통한 지역 서비스 개선",
            "기술": "Python · 시각화 · 정책제안"
        },
        {
            "직무": "AI 개발자",
            "유형": "서비스 개발",
            "제목": "LLM 기반 문서 질의응답 시스템",
            "기술": "LLM · RAG · LangChain"
        }
    ]

    filtered = [
        s for s in seniors
        if (job_filter == "전체" or s["직무"] == job_filter)
        and (project_filter == "전체" or s["유형"] == project_filter)
    ]

    senior_cols = st.columns(4)

    for i, senior in enumerate(filtered):

        with senior_cols[i % 4]:

            st.markdown(f"""
            <div class="senior-card">
                <div style="font-size:30px;">📁</div>
                <small>{senior['직무']}</small>
                <h4 style="color:#19334d;">{senior['제목']}</h4>
                <p style="font-size:12px;color:#8294a4;">
                    {senior['기술']}
                </p>
            </div>
            """, unsafe_allow_html=True)

            with st.expander("상세 보기"):
                st.write("직무:", senior["직무"])
                st.write("프로젝트 유형:", senior["유형"])
                st.write("활용 기술:", senior["기술"])
                st.info("구성 설명을 위한 예시입니다. 실제 수료생의 사례가 아닙니다.")

    if not filtered:
        st.info("조건에 맞는 포트폴리오가 없습니다.")

    # ==========================================
    # 04. 포트폴리오 작성 가이드
    # ==========================================
    st.markdown('<div class="portfolio-section">04. 📚 포트폴리오 작성 가이드</div>',
                unsafe_allow_html=True)

    guide_items = {
        "📋 좋은 포트폴리오의 구성 요소": """
        1. 프로젝트 개요 및 배경
        2. 문제 정의 및 해결 목표
        3. 담당 역할 및 기여도
        4. 활용 기술 및 분석 방법
        5. 프로젝트 결과 및 성과
        6. 배운 점 및 향후 개선 방향
        """,

        "💻 프로젝트 작성 예시": """
        프로젝트명: 고객 VOC 분석 기반 AI 상담 지원 서비스

        문제 정의: 반복적인 고객 문의로 인한 상담 업무 부담

        해결 방법: VOC 데이터 분석 및 RAG 기반 질의응답 시스템 구축

        활용 기술: Python, Pandas, LangChain, Chroma

        성과: 상담 업무 효율화 가능성 및 정보 검색 편의성 제시
        """,

        "📊 성과 지표 표현 방법": """
        정량적 성과:
        - 데이터 처리 시간 감소율
        - 모델 정확도 및 F1-score
        - 사용자 만족도
        - 업무 처리 시간 개선

        정성적 성과:
        - 문제 해결 과정
        - 협업 및 의사소통 경험
        - 업무 프로세스 개선
        """,

        "💡 자주 묻는 질문 (FAQ)": """
        Q. 프로젝트 경험이 적어도 작성할 수 있나요?
        A. 미니프로젝트, 개인 프로젝트, 학습 경험도 작성할 수 있습니다.

        Q. 팀 프로젝트에서 어떤 내용을 강조해야 하나요?
        A. 팀 전체 성과뿐 아니라 본인의 역할과 기여도를 구체적으로 작성하세요.

        Q. 성과를 수치로 표현하기 어려우면 어떻게 하나요?
        A. 문제 해결 과정, 개선 사항, 결과물 등 정성적 성과를 제시하세요.
        """
    }

    for title, content in guide_items.items():
        with st.expander(title):
            st.markdown(content)

    # 기존 일정 및 체크리스트 유지
    st.markdown('<div class="portfolio-section">📅 포트폴리오 일정 및 점검</div>',
                unsafe_allow_html=True)

    lines = render_event_list(
        [e for e in TEAM_EVENTS if e[3] == "포폴"]
    )

    chk = render_checklist("포폴")

    return (
        "포트폴리오 화면. "
        "포트폴리오 작성, AI 피드백 업로드, "
        "선배 포트폴리오 및 작성 가이드를 제공합니다. "
        + "일정: " + "; ".join(lines)
        + ". " + chk
    )
def page_upload():

    import os
    import tempfile
    import uuid
    from datetime import datetime

    # --------------------------------------
    # 세션 상태 초기화
    # --------------------------------------
    if "uploaded_documents" not in st.session_state:
        st.session_state.uploaded_documents = []

    if "upload_activity" not in st.session_state:
        st.session_state.upload_activity = []

    if "upload_name" not in st.session_state:
        st.session_state.upload_name = None

    if "upload_chain" not in st.session_state:
        st.session_state.upload_chain = None

    # --------------------------------------
    # 디자인 CSS
    # --------------------------------------
    st.markdown("""
    <style>

    .upload-banner {
        background: linear-gradient(110deg, #e0f7f8, #e5f3ff);
        border-radius: 20px;
        padding: 25px;
        margin: 15px 0 18px 0;
        min-height: 135px;
    }

    .upload-banner h2 {
        color: #19334d;
        font-size: 25px;
        font-weight: 800;
        margin-bottom: 12px;
    }

    .upload-banner p {
        color: #526d83;
        font-size: 15px;
        line-height: 1.8;
    }

    .upload-feature {
        background: white;
        border-radius: 16px;
        padding: 16px 8px;
        text-align: center;
        min-height: 95px;
        box-shadow: 0 4px 14px rgba(50,80,100,0.07);
        border: 1px solid #e9f0f5;
    }

    .upload-feature .emoji {
        font-size: 27px;
    }

    .upload-feature h4 {
        font-size: 15px;
        color: #19334d;
        margin: 5px 0;
    }

    .upload-feature p {
        font-size: 11px;
        color: #8294a4;
        margin: 0;
    }

    .upload-section-title {
        font-size: 20px;
        font-weight: 800;
        color: #19334d;
        margin: 20px 0 12px 0;
    }

    .upload-box {
        background: #ffffff;
        border: 1px dashed #9bbbd2;
        border-radius: 17px;
        padding: 20px;
        text-align: center;
        color: #19334d;
    }

    .upload-setting {
        background: white;
        border-radius: 17px;
        padding: 18px;
        box-shadow: 0 4px 15px rgba(50,80,100,0.06);
    }

    .upload-info {
        background: #e5f8f7;
        border-radius: 13px;
        padding: 14px;
        color: #19334d;
        font-size: 13px;
        line-height: 1.8;
    }

    .document-status {
        background: #e5f8ed;
        color: #149b64;
        padding: 5px 10px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 700;
    }

    </style>
    """, unsafe_allow_html=True)

    # ======================================
    # 페이지 제목
    # ======================================
    st.markdown(
        '<div class="page-title">📁 파일 불러오기</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-sub">Document Upload | 나만의 학습 자료를 등록하고 RAG로 질문하세요.</div>',
        unsafe_allow_html=True
    )

    # ======================================
    # 상단 배너
    # ======================================
    st.markdown("""
    <div class="upload-banner">
        <h2>학습 자료를 업로드하고, AI와 대화해 보세요! ✨</h2>
        <p>
        AIVLE School 백서, 교안, 프로젝트 자료 등<br>
        나만의 문서를 등록하여 RAG 기반으로 질문하고 답변을 받을 수 있습니다.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ======================================
    # 주요 기능 안내
    # ======================================
    f1, f2, f3, f4 = st.columns(4)

    features = [
        ("📤", "문서 업로드", "PDF 문서 등록"),
        ("📚", "자동 처리", "문서 분할 및 임베딩"),
        ("💬", "AI 기반 질의응답", "업로드 문서 기반 답변"),
        ("📑", "지식 관리", "등록 문서 확인 및 삭제")
    ]

    for col, feature in zip([f1, f2, f3, f4], features):
        with col:
            st.markdown(f"""
            <div class="upload-feature">
                <div class="emoji">{feature[0]}</div>
                <h4>{feature[1]}</h4>
                <p>{feature[2]}</p>
            </div>
            """, unsafe_allow_html=True)

    # ======================================
    # 01. 문서 업로드
    # ======================================
    st.markdown(
        '<div class="upload-section-title">01. 📤 문서 업로드</div>',
        unsafe_allow_html=True
    )

    left, right = st.columns([1.2, 0.9], gap="medium")

    with left:

        st.markdown("""
        <div class="upload-box">
            <div style="font-size:48px;">☁️</div>
            <h4>학습 자료를 업로드하세요.</h4>
            <p>파일을 선택하여 업로드할 수 있습니다.</p>
        </div>
        """, unsafe_allow_html=True)

        uploaded_file = st.file_uploader(
            "파일 선택",
            type=["pdf"],
            key="document_uploader",
            help="현재 RAG 자동 처리 기능은 PDF를 지원합니다."
        )

        st.caption("지원 형식: PDF | 파일당 최대 200MB")

        if uploaded_file:

            file_size = uploaded_file.size

            st.success(f"📄 {uploaded_file.name}")

            st.caption(
                f"파일 크기: {file_size / (1024 * 1024):.2f} MB"
            )

            if file_size > 200 * 1024 * 1024:
                st.error("파일 크기는 200MB를 초과할 수 없습니다.")

    # ======================================
    # 02. 업로드 설정
    # ======================================
    with right:

        st.markdown(
            '<div class="upload-section-title">02. ⚙️ 업로드 설정</div>',
            unsafe_allow_html=True
        )

        category = st.selectbox(
            "📂 문서 카테고리",
            [
                "교육 자료",
                "프로젝트 자료",
                "취업 자료",
                "포트폴리오",
                "기타"
            ],
            key="document_category"
        )

        description = st.text_area(
            "📝 문서 설명 (선택)",
            placeholder="문서 내용을 간단히 입력하세요.\n예: DX 교안, 미니프로젝트 자료 등",
            height=105,
            key="document_description"
        )

        st.markdown("""
        <div class="upload-info">
        <b>📌 문서 처리 과정</b><br>
        ① PDF 문서 읽기<br>
        ② 텍스트 분할 (Chunking)<br>
        ③ 임베딩 생성<br>
        ④ Chroma 벡터 저장소 등록<br>
        ⑤ RAG 질의응답 준비
        </div>
        """, unsafe_allow_html=True)

        st.write("")

        process_button = st.button(
            "📤 업로드 및 처리",
            use_container_width=True,
            type="primary",
            disabled=uploaded_file is None
        )

        # 문서 처리
        if process_button and uploaded_file:

            if uploaded_file.size > 200 * 1024 * 1024:
                st.error("200MB 이하의 파일만 업로드할 수 있습니다.")

            elif any(
                d["name"] == uploaded_file.name
                for d in st.session_state.uploaded_documents
            ):
                st.warning("이미 등록된 문서입니다.")

            else:

                tmp = os.path.join(
                    tempfile.gettempdir(),
                    f"upload_{uuid.uuid4().hex}.pdf"
                )

                try:

                    with st.spinner(
                        "문서를 읽고 벡터 저장소를 만드는 중입니다..."
                    ):

                        with open(tmp, "wb") as f:
                            f.write(uploaded_file.getbuffer())

                        # 기존 RAG 파이프라인 사용
                        chain = rag_pipeline(
                            tmp,
                            collection_name="user_docs"
                        )

                        st.session_state.upload_chain = chain
                        st.session_state.upload_name = uploaded_file.name
                        st.session_state.answer_source = "업로드 문서"

                        now = datetime.now().strftime(
                            "%Y.%m.%d %H:%M"
                        )

                        document = {
                            "name": uploaded_file.name,
                            "category": category,
                            "description": description,
                            "size": uploaded_file.size,
                            "date": now,
                            "status": "완료",
                            "content": uploaded_file.getvalue(),
                            "chain": chain
                        }

                        st.session_state.uploaded_documents.append(
                            document
                        )

                        st.session_state.upload_activity.insert(
                            0,
                            {
                                "name": uploaded_file.name,
                                "date": now
                            }
                        )

                    st.success(
                        f"{uploaded_file.name} 등록 및 RAG 처리가 완료되었습니다!"
                    )

                except Exception as e:
                    st.error(f"문서 처리 중 오류가 발생했습니다: {e}")

                finally:
                    if os.path.exists(tmp):
                        os.remove(tmp)

    # ======================================
    # 03. 등록된 문서 관리
    # ======================================
    st.markdown(
        '<div class="upload-section-title">03. 📚 등록된 문서 관리</div>',
        unsafe_allow_html=True
    )

    documents = st.session_state.uploaded_documents

    # 검색 및 필터
    search_col, filter_col, count_col = st.columns([2, 1.3, 0.7])

    with search_col:
        search_text = st.text_input(
            "🔍 문서명 검색",
            placeholder="문서명을 검색하세요.",
            key="document_search"
        )

    with filter_col:
        selected_category = st.selectbox(
            "카테고리",
            ["전체", "교육 자료", "프로젝트 자료",
             "취업 자료", "포트폴리오", "기타"],
            key="document_filter"
        )

    with count_col:
        st.markdown("**등록 문서**")
        st.markdown(
            f"### {len(documents)}개"
        )

    # 필터 적용
    filtered_documents = [
        d for d in documents
        if search_text.lower() in d["name"].lower()
        and (
            selected_category == "전체"
            or d["category"] == selected_category
        )
    ]

    # 문서 목록
    if filtered_documents:

        header = st.columns([0.4, 2.4, 1.2, 1.2, 0.8, 1.1, 1.4])

        headers = [
            "선택",
            "파일명",
            "카테고리",
            "업로드일",
            "크기",
            "상태",
            "작업"
        ]

        for col, title in zip(header, headers):
            col.markdown(f"**{title}**")

        st.divider()

        for idx, doc in enumerate(filtered_documents):

            cols = st.columns([0.4, 2.4, 1.2, 1.2, 0.8, 1.1, 1.4])

            with cols[0]:
                selected = st.checkbox(
                    "선택",
                    key=f"doc_select_{doc['name']}",
                    label_visibility="collapsed"
                )

            with cols[1]:
                st.markdown(f"📄 **{doc['name']}**")

            with cols[2]:
                st.caption(doc["category"])

            with cols[3]:
                st.caption(doc["date"])

            with cols[4]:
                st.caption(
                    f"{doc['size'] / (1024 * 1024):.1f} MB"
                )

            with cols[5]:
                st.markdown(
                    '<span class="document-status">● 완료</span>',
                    unsafe_allow_html=True
                )

            with cols[6]:

                view_col, delete_col = st.columns(2)

                with view_col:
                    if st.button(
                        "👁️",
                        key=f"view_doc_{idx}",
                        help="문서 정보 확인"
                    ):
                        st.session_state["view_document"] = doc["name"]

                with delete_col:
                    if st.button(
                        "🗑️",
                        key=f"delete_doc_{idx}",
                        help="문서 삭제"
                    ):
                        st.session_state.uploaded_documents = [
                            d for d in st.session_state.uploaded_documents
                            if d["name"] != doc["name"]
                        ]

                        if st.session_state.upload_name == doc["name"]:
                            st.session_state.upload_name = None
                            st.session_state.upload_chain = None
                            st.session_state.answer_source = "AIVLE School 백서"

                        st.success("문서가 삭제되었습니다.")
                        st.rerun()

            # 문서 정보 확인
            if st.session_state.get("view_document") == doc["name"]:

                with st.expander(
                    f"📄 {doc['name']} 문서 정보",
                    expanded=True
                ):

                    st.write("카테고리:", doc["category"])
                    st.write("설명:", doc["description"] or "설명 없음")
                    st.write("업로드일:", doc["date"])

                    st.download_button(
                        "📥 원본 문서 다운로드",
                        data=doc["content"],
                        file_name=doc["name"],
                        mime="application/pdf",
                        key=f"download_{idx}"
                    )

                    if st.button(
                        "닫기",
                        key=f"close_view_{idx}"
                    ):
                        st.session_state.view_document = None
                        st.rerun()

            st.divider()

        # 선택 문서 일괄 삭제
        if st.button("🗑️ 선택한 문서 삭제", use_container_width=True):

            selected_names = [
                d["name"] for d in filtered_documents
                if st.session_state.get(
                    f"doc_select_{d['name']}", False
                )
            ]

            if selected_names:

                st.session_state.uploaded_documents = [
                    d for d in st.session_state.uploaded_documents
                    if d["name"] not in selected_names
                ]

                if st.session_state.upload_name in selected_names:
                    st.session_state.upload_name = None
                    st.session_state.upload_chain = None
                    st.session_state.answer_source = "AIVLE School 백서"

                st.success(
                    f"{len(selected_names)}개 문서를 삭제했습니다."
                )

                st.rerun()

            else:
                st.warning("삭제할 문서를 선택해 주세요.")

    else:

        st.info(
            "등록된 문서가 없습니다. PDF 파일을 업로드해 주세요."
            if not documents
            else "검색 조건에 맞는 문서가 없습니다."
        )

    # ======================================
    # 최근 업로드 활동
    # ======================================
    st.markdown(
        '<div class="upload-section-title">🕒 최근 업로드 활동</div>',
        unsafe_allow_html=True
    )

    activities = st.session_state.upload_activity

    if activities:

        for activity in activities[:5]:

            st.markdown(
                f"""
                <div style="
                    background:white;
                    padding:13px;
                    border-radius:13px;
                    margin-bottom:8px;
                    box-shadow:0 3px 12px rgba(50,80,100,0.04);
                ">
                    <b>🟢 {activity['name']}</b><br>
                    <span style="color:#8a9aa6;font-size:12px;">
                        {activity['date']} 업로드 완료
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )

    else:
        st.caption("아직 업로드 활동이 없습니다.")

    # ======================================
    # 현재 RAG 연결 상태
    # ======================================
    st.markdown(
        '<div class="upload-section-title">🤖 현재 RAG 연결 상태</div>',
        unsafe_allow_html=True
    )

    if st.session_state.upload_chain:

        st.success(
            f"현재 활성 문서: {st.session_state.upload_name}"
        )

        st.caption(
            "업로드한 문서를 기준으로 AI Learning Assistant에서 질문할 수 있습니다."
        )

    else:

        st.info(
            "현재 업로드 문서가 활성화되어 있지 않습니다. "
            "문서를 업로드하고 처리해 주세요."
        )

    # 기존 챗봇과 연결하기 위한 반환값
    return (
        "파일 불러오기 화면. "
        f"등록된 문서 수: {len(documents)}개. "
        f"현재 업로드 문서: {st.session_state.upload_name or '없음'}"
    )
def page_ontology():

    # --------------------------------------
    # 1. 상단 제목
    # --------------------------------------
    st.markdown("""
    <div style="display:flex; justify-content:space-between;
                align-items:center; margin-bottom:5px;">
        <div>
            <div style="font-size:29px; font-weight:850; color:#19334d;">
                🌸 온톨로지
            </div>
            <div style="font-size:14px; color:#8295a5;">
                Ontology & Knowledge Graph
            </div>
        </div>
        <div style="background:#16aaa9; color:white; padding:9px 18px;
                    border-radius:25px; font-size:12px; font-weight:800;">
            KNOWLEDGE GRAPH
        </div>
    </div>
    """, unsafe_allow_html=True)


    # --------------------------------------
    # 2. 소개 배너
    # --------------------------------------
    st.markdown("""
    <div style="
        background:linear-gradient(110deg,#dff7f8,#e9f5ff);
        border-radius:20px;
        padding:22px 25px;
        margin:15px 0;
        min-height:110px;
    ">
        <div style="font-size:25px; font-weight:850; color:#19334d;">
            AIVLE School 지식 구조를 한눈에!
        </div>
        <div style="font-size:15px; color:#536c83; line-height:1.8;
                    margin-top:8px;">
            교육과정, 직무, 프로젝트 등 주요 개념의 관계를<br>
            온톨로지(지식 그래프)로 시각화하고 탐색할 수 있습니다.
        </div>
    </div>
    """, unsafe_allow_html=True)


    # --------------------------------------
    # 3. 온톨로지 데이터 불러오기
    # --------------------------------------
    raw = st.session_state.get("ontology_raw")

    if os.path.exists(ONTOLOGY_FILE):
        with open(ONTOLOGY_FILE, "r", encoding="utf-8") as f:
            raw = f.read()

    else:
        uploaded_json = st.file_uploader(
            "온톨로지 JSON 파일 업로드",
            type=["json"],
            key="ontology_json_upload"
        )

        if uploaded_json:
            raw = uploaded_json.getvalue().decode("utf-8")
            st.session_state.ontology_raw = raw

    if not raw:
        st.info(
            "온톨로지 파일이 없습니다. "
            "01번 노트북에서 생성한 aivle_ontology.json을 업로드해주세요."
        )
        return "온톨로지 화면. 데이터 파일 없음"


    # 기존 데이터 처리 함수 활용
    try:
        edges = load_ontology_text(raw)
    except (ValueError, KeyError, TypeError) as exc:
        st.error(f"온톨로지 파일 형식을 확인해 주세요: {exc}")
        return "온톨로지 파일 형식 오류"
    if not edges:
        st.info("표시할 관계가 없습니다.")
        return "온톨로지 관계 없음"

    entities = sorted(
        {e["subject"] for e in edges}
        | {e["object"] for e in edges}
    )

    relations = sorted({
        e["relation"] for e in edges
    })


    # --------------------------------------
    # 4. 상단 메뉴
    # --------------------------------------
    menu = st.radio(
        "온톨로지 메뉴",
        [
            "📊 지식 그래프",
            "📁 클래스(개념)",
            "🔗 속성(Property)",
            "📄 관계 미리보기",
            "⚙️ 관리"
        ],
        horizontal=True,
        label_visibility="collapsed",
        key="ontology_menu"
    )

    st.markdown("---")


    # ======================================
    # 메뉴 1. 지식 그래프
    # ======================================
    if menu == "📊 지식 그래프":

        st.markdown("### 01. 지식 그래프 시각화")

        col_graph, col_info = st.columns([2.5, 1])

        with col_graph:

            # 관심 개체 선택
            st.multiselect(
                "📌 관심 개체 고정",
                entities,
                key="pinned"
            )

            # 교육 / 취업 / 포트폴리오 구분
            tabs = st.tabs([
                "📚 교육",
                "💼 취업",
                "📁 포폴"
            ])

            shown_lines = []

            for tab, name in zip(
                tabs,
                ["교육", "취업", "포폴"]
            ):

                with tab:

                    tab_edges = [
                        e for e in edges
                        if edge_in_tab(e, name)
                    ]

                    focus = S["focus"]

                    def score(e):
                        text = (
                            f'{e["subject"]} {e["object"]}'
                        )

                        pin = (
                            2 if (
                                e["subject"] in st.session_state.pinned
                                or e["object"] in st.session_state.pinned
                            ) else 0
                        )

                        return pin + sum(
                            k in text for k in focus
                        )

                    tab_edges.sort(
                        key=score,
                        reverse=True
                    )

                    # 검색
                    keyword = st.text_input(
                        "관계 검색",
                        placeholder="예: Python, 미니프로젝트",
                        key=f"ontology_search_{name}"
                    )

                    if keyword:
                        tab_edges = [
                            e for e in tab_edges
                            if keyword.lower() in (
                                f'{e["subject"]} '
                                f'{e["object"]} '
                                f'{e["relation"]} '
                                f'{e["evidence"]}'
                            ).lower()
                        ]

                    st.caption(
                        f"총 관계 수: {len(tab_edges)}개"
                    )

                    top = tab_edges[:20]

                    if top:

                        # Graphviz 그래프 생성
                        def safe_text(value):
                            return (
                                str(value)
                                .replace("\\", "/")
                                .replace('"', "'")
                                .replace("\n", " ")[:40]
                            )

                        dot = [
                            "digraph G {",
                            "rankdir=LR;",
                            'bgcolor="transparent";',
                            'node [shape=box, style="rounded,filled", '
                            'fillcolor="#e5f5f5", color="#43aebe", '
                            'fontname="sans-serif", fontsize=11];',
                            'edge [color="#83b3f5", '
                            'fontname="sans-serif", fontsize=9];'
                        ]

                        for e in top:

                            subject = safe_text(e["subject"])
                            obj = safe_text(e["object"])
                            relation = safe_text(e["relation"])

                            dot.append(
                                f'"{subject}" -> "{obj}" '
                                f'[label="{relation}"];'
                            )

                        dot.append("}")

                        st.graphviz_chart(
                            "\n".join(dot),
                            use_container_width=True
                        )

                        # 관계 데이터
                        df = pd.DataFrame(top)[
                            [
                                "subject",
                                "relation",
                                "object",
                                "evidence",
                                "page"
                            ]
                        ]

                        df.columns = [
                            "개체",
                            "관계",
                            "대상",
                            "근거 원문",
                            "쪽"
                        ]

                        st.dataframe(
                            df,
                            use_container_width=True,
                            hide_index=True
                        )

                        # 챗봇 질문 연결
                        pick = st.selectbox(
                            "관계 선택",
                            range(len(top)),
                            key=f"ontology_pick_{name}",
                            format_func=lambda i:
                                f'{top[i]["subject"]} → '
                                f'{top[i]["relation"]} → '
                                f'{top[i]["object"]}'
                        )

                        if st.button(
                            "💬 챗봇에게 자세히 질문하기",
                            key=f"ontology_ask_{name}",
                            use_container_width=True
                        ):

                            selected = top[pick]

                            question = (
                                f'"{selected["subject"]}"의 '
                                f'"{selected["relation"]}" 관계와 '
                                f'"{selected["object"]}"에 대해 '
                                f'자세히 설명해주세요.'
                            )

                            ask(question)

                        shown_lines += [
                            f'[{name}] {e["subject"]} '
                            f'-{e["relation"]}-> {e["object"]}'
                            for e in top[:8]
                        ]

                    else:
                        st.info("해당 조건에 맞는 관계가 없습니다.")


        # ----------------------------------
        # 온톨로지 정보
        # ----------------------------------
        with col_info:

            st.markdown("### 02. 온톨로지 정보")

            info_tab = st.tabs([
                f"클래스 ({len(entities)})",
                f"속성 ({len(relations)})"
            ])

            with info_tab[0]:

                for entity in entities:

                    with st.expander(f"🔷 {entity}"):

                        related = [
                            e for e in edges
                            if (
                                e["subject"] == entity
                                or e["object"] == entity
                            )
                        ]

                        st.caption(
                            f"연결된 관계: {len(related)}개"
                        )

                        for e in related[:10]:

                            st.write(
                                f'{e["subject"]} '
                                f'→ {e["relation"]} '
                                f'→ {e["object"]}'
                            )

            with info_tab[1]:

                for relation in relations:

                    with st.expander(f"🔗 {relation}"):

                        related = [
                            e for e in edges
                            if e["relation"] == relation
                        ]

                        st.caption(
                            f"사용 횟수: {len(related)}개"
                        )

                        for e in related[:10]:

                            st.write(
                                f'{e["subject"]} → {e["object"]}'
                            )


    # ======================================
    # 메뉴 2. 클래스(개념)
    # ======================================
    elif menu == "📁 클래스(개념)":

        st.markdown("### 📁 클래스 및 개념 탐색")

        st.caption(
            "AIVLE School을 구성하는 주요 개념을 탐색합니다."
        )

        selected = st.selectbox(
            "클래스 선택",
            entities,
            key="ontology_class_select"
        )

        related = [
            e for e in edges
            if (
                e["subject"] == selected
                or e["object"] == selected
            )
        ]

        st.markdown(
            f"#### 🔷 {selected}"
        )

        st.metric(
            "연결된 관계 수",
            len(related)
        )

        if related:

            df = pd.DataFrame(related)[
                ["subject", "relation", "object", "evidence"]
            ]

            df.columns = [
                "개체",
                "관계",
                "대상",
                "근거"
            ]

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )


    # ======================================
    # 메뉴 3. 속성(Property)
    # ======================================
    elif menu == "🔗 속성(Property)":

        st.markdown("### 🔗 관계 및 속성 탐색")

        st.caption(
            "개체 사이에 어떤 관계가 형성되어 있는지 확인합니다."
        )

        selected_relation = st.selectbox(
            "관계 선택",
            relations,
            key="ontology_relation_select"
        )

        related = [
            e for e in edges
            if e["relation"] == selected_relation
        ]

        st.metric(
            "해당 관계 수",
            len(related)
        )

        if related:

            df = pd.DataFrame(related)[
                ["subject", "relation", "object", "evidence", "page"]
            ]

            df.columns = [
                "시작 개체",
                "관계",
                "연결 개체",
                "근거 원문",
                "페이지"
            ]

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )


    # ======================================
    # 메뉴 4. SPARQL 질의
    # ======================================
    elif menu == "📄 관계 미리보기":

        st.markdown("### 03. 관계 데이터 미리보기")

        st.caption(
            "온톨로지 관계를 질의하고 관련 데이터를 확인합니다."
        )

        st.caption("현재 버전은 SPARQL 실행기가 아닌 관계 데이터 미리보기입니다.")
        if st.button(
            "▶ 관계 20개 보기",
            use_container_width=True,
            key="ontology_sparql_run"
        ):

            # 현재 구현은 관계 데이터 기반 미리보기 검색
            st.session_state.ontology_query_result = edges[:20]
            st.session_state.ontology_query_executed = True

        if st.session_state.get(
            "ontology_query_executed",
            False
        ):

            result = st.session_state.get(
                "ontology_query_result",
                []
            )

            st.markdown(
                f"#### 결과 ({len(result)}개)"
            )

            if result:

                result_df = pd.DataFrame(result)[
                    ["subject", "relation", "object"]
                ]

                result_df.columns = [
                    "subject",
                    "relation",
                    "object"
                ]

                st.dataframe(
                    result_df,
                    use_container_width=True,
                    hide_index=True
                )


    # ======================================
    # 메뉴 5. 관리
    # ======================================
    elif menu == "⚙️ 관리":

        st.markdown("### ⚙️ 온톨로지 관리")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "전체 개체",
                len(entities)
            )

        with col2:
            st.metric(
                "전체 관계",
                len(edges)
            )

        with col3:
            st.metric(
                "관계 유형",
                len(relations)
            )

        st.markdown("#### 📌 관심 개체 관리")

        st.multiselect(
            "항상 표시할 개체",
            entities,
            key="pinned"
        )

        st.button("🗑 관심 개체 초기화", on_click=lambda: st.session_state.update(pinned=[]))


    # ======================================
    # 하단 예시 질문
    # ======================================
    if menu == "📊 지식 그래프":

        st.markdown("---")

        st.markdown("### 04. 예시 질의")

        col1, col2 = st.columns(2)

        questions = [
            "DX 컨설턴트에게 필요한 핵심 역량은?",
            "미니프로젝트 주제와 사용 기술은?",
            "교육과정 간의 관계를 알려줘.",
            "특정 프로젝트에 사용된 기술은?",
            "포트폴리오와 연관된 개념은?"
        ]

        for i, question in enumerate(questions):

            target_col = col1 if i % 2 == 0 else col2

            with target_col:

                if st.button(
                    f"🔍 {question}",
                    key=f"ontology_example_{i}",
                    use_container_width=True
                ):

                    ask(question)


    return (
        "온톨로지 화면. "
        f"전체 개체 {len(entities)}개, "
        f"전체 관계 {len(edges)}개. "
        + "; ".join(shown_lines)
        if menu == "📊 지식 그래프"
        else (
            "온톨로지 화면. "
            f"전체 개체 {len(entities)}개, "
            f"전체 관계 {len(edges)}개."
        )
    )
def page_archive():
    st.markdown('<div class="page-title">💬 대화 기록</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">지난 질문과 답변을 날짜별로 다시 볼 수 있어요</div>', unsafe_allow_html=True)
    arc = st.session_state.archive
    if not arc:
        st.info("아직 저장된 대화가 없습니다.")
        return "대화 기록 화면(기록 없음)"
    dates = sorted({a["date"] for a in arc}, reverse=True)
    d = st.selectbox("날짜 선택", dates)
    kw = st.text_input("기록 검색", placeholder="질문이나 답변에 들어간 단어")
    rows = [a for a in arc if a["date"] == d and (not kw or kw in a["question"] or kw in a["answer"])]
    for a in reversed(rows):
        with st.expander(f'🕒 {a["time"]} · {a["question"][:40]}'):
            st.caption(f'{a["stage"]} · {a["page"]} · 기준: {a.get("source", "")}')
            st.markdown(f'**Q.** {a["question"]}')
            st.markdown(a["answer"])
            st.button("🔁 다시 질문하기", key=f're_{a["id"]}', on_click=ask, args=(a["question"],))
    c1, c2 = st.columns(2)
    with c1:
        csv = pd.DataFrame(arc).to_csv(index=False).encode("utf-8-sig")
        st.download_button("⬇️ 전체 기록 CSV 다운로드", csv, "aivle_chat_log.csv", "text/csv", use_container_width=True)
    with c2:
        if st.button("🗑️ 이 날짜 기록 삭제", use_container_width=True):
            st.session_state.archive = [a for a in arc if a["date"] != d]
            save_archive()
            st.rerun()
    return f"대화 기록 화면. {d} 기록 {len(rows)}건"


# Shared page state. The user's calendar keys are retained unchanged.
for key, value in {"profile":{"stage":"재학","name":"에이블러","track":"DX 컨설턴트"},
    "checks":{}, "pinned":[], "archive":[], "upload_chain":None, "upload_name":None,
    "answer_source":"AIVLE School 백서", "send_screen":False, "last_sources":[]}.items():
    st.session_state.setdefault(key,value)
profile = st.session_state.profile
stage = profile["stage"]
S = STAGES[stage]
today = korea_today()
profile_text = f"이름: {profile['name']}, 단계: {S['label']}, 트랙: {profile['track']}, 오늘: {today}. {S['rule']}"
# Calendar's original events remain the authoritative source of dates.
TEAM_EVENTS = [(date.fromisoformat(e['start']),date.fromisoformat(e['end']),e['title'],
    '포폴' if '포트폴리오' in e['title'] else ('교육' if e['category']=='교육' else '취업'))
    for e in EVENTS if not e.get('cert') and e.get('mode')!='daily']
with st.sidebar:

    # AIVLE 로고
    st.html("""
    <div class="logo-area">
        <img
            src="https://raw.githubusercontent.com/Jangrae/img/master/aivle.png"
            width="145">
        <p>AIVLE SCHOOL</p>
    </div>
    """)

    # 실제 페이지 이동 버튼: 홈과 캘린더만 연결했습니다.
    st.button('🏠 홈', key='nav_home', on_click=navigate, args=('home',),
              type='primary' if st.session_state.active_page == 'home' else 'secondary',
              use_container_width=True)
    st.button('🗓️ 캘린더 · 할 일', key='nav_calendar', on_click=navigate, args=('calendar',),
              type='primary' if st.session_state.active_page == 'calendar' else 'secondary',
              use_container_width=True)
    # 예은님 기능을 기존 사이드바 순서로 연결합니다.
    for label, page in [
        ("👋 소개", "intro"), ("📚 교육과정", "edu"), ("💼 취업과정", "job"),
        ("🗂️ 포트폴리오", "portfolio"), ("📂 파일 불러오기", "upload"),
        ("🧩 온톨로지", "ontology"), ("💬 대화 기록", "archive")]:
        st.button(label, key=f"nav_{page}", on_click=navigate, args=(page,),
                  type="primary" if st.session_state.active_page==page else "secondary",
                  use_container_width=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # 관리자
    st.html("""
    <p style="font-size:14px;font-weight:800;color:white;">
        ⚙️ 관리자
    </p>
    """)

    st.button("📤 문서 관리 열기", key="admin_documents", on_click=navigate,
              args=("upload",), use_container_width=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # 대화 삭제
    if st.button(
        "🗑️ 대화 삭제",
        use_container_width=True
    ):

        st.session_state.messages = []
        st.session_state.pending_prompt = None
        st.rerun()

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.html("""
    <p style="color:white;font-size:12px;">
        AIVLE School<br>
        Learning Assistant
    </p>
    """)


# ==========================================
# 6. 전체 화면 레이아웃
# ==========================================
left, right = st.columns(
    [7, 3],
    gap="large"
)


# ==========================================
# 7. 중앙 대시보드
# ==========================================
submitted = False
question = ""
PAGE_FUNCS = {"intro":page_intro,"edu":page_edu,"job":page_job,"portfolio":page_portfolio,
              "upload":page_upload,"ontology":page_ontology,"archive":page_archive}
screen_text = "홈 화면"
with left:
    if st.session_state.active_page in PAGE_FUNCS:
        screen_text = PAGE_FUNCS[st.session_state.active_page]() or st.session_state.active_page
    elif st.session_state.active_page == 'calendar':
        # ======================================
        # 출결 및 일정 관리 달력
        # ======================================
        st.html("""
        <div class="section-title">📅 출결 & 일정 관리</div>
        <div class="calendar-caption">
            백서 일정과 오늘의 할 일을 확인하세요. 출결 기록은 개인 메모이며 공식 출결과 연동되지 않습니다.
        </div>
        """)

        # 백서 1.5.2: 10기 개강 2026-09-29. 출석일수가 아닌 달력 경과일입니다.
        today = korea_today()
        course_start = date(2026, 9, 29)
        course_end = date(2027, 3, 5)
        elapsed_day = (today - course_start).days + 1
        if today < course_start:
            hero_heading = f'교육 시작까지 <strong>{(course_start - today).days}일</strong> 남았어요.'
        elif today > course_end:
            hero_heading = '교육을 마친 여러분의 <strong>다음 도전</strong>을 응원해요.'
        else:
            hero_heading = f'오늘은 교육 <strong>{elapsed_day}일차</strong>입니다.'
        cheers = [
            '오늘 배운 것 하나, 내 것으로 만들어봐요.',
            '막혔던 문제도 한 단계씩 풀어가면 돼요.',
            '작은 실습 하나가 다음 프로젝트의 밑바탕이 됩니다.',
            '오늘의 목표 하나부터 차근차근 시작해봐요.',
            '어제보다 하나 더 이해하는 하루를 만들어봐요.',
            '잠깐 쉬어가도 좋아요. 다시 시작할 힘을 채워봐요.',
            '함께 묻고, 함께 풀면서 한 걸음 더 나아가요.',
        ]
        weekday = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일'][today.weekday()]
        st.html(f"""
        <section class="today-card" aria-label="오늘의 학습 응원">
          <div class="today-stamp">
            <div class="today-month">{today.year} · {today.month:02d}</div>
            <div class="today-number">{today.day:02d}</div>
            <div class="today-weekday">{weekday}</div>
          </div>
          <div>
            <div class="today-eyebrow">AIVLE SCHOOL · 오늘의 한 걸음</div>
            <h2 class="today-heading">{hero_heading}</h2>
            <p class="today-cheer">{cheers[today.toordinal() % len(cheers)]}</p>
            <div class="today-basis">한국시간 기준 · 2026.09.29 개강 · 일차는 주말·공휴일을 포함한 경과일</div>
          </div>
        </section>
        """)
        with st.container(key="calendar_panel"):
            # 월 이동 및 월 표시
            month_prev, month_title, month_next = st.columns([1, 5, 1])

            with month_prev:
                if st.button("‹", key="calendar_prev_month", use_container_width=True):
                    current_month = st.session_state.calendar_month
                    if current_month.month == 1:
                        st.session_state.calendar_month = date(current_month.year - 1, 12, 1)
                    else:
                        st.session_state.calendar_month = date(current_month.year, current_month.month - 1, 1)
                    st.rerun()

            with month_title:
                st.markdown(
                    f"<h3 style='text-align:center;color:#19334d;margin:4px 0 15px 0;'>"
                    f"{st.session_state.calendar_month.year}년 {st.session_state.calendar_month.month}월"
                    f"</h3>",
                    unsafe_allow_html=True
                )

            with month_next:
                if st.button("›", key="calendar_next_month", use_container_width=True):
                    current_month = st.session_state.calendar_month
                    if current_month.month == 12:
                        st.session_state.calendar_month = date(current_month.year + 1, 1, 1)
                    else:
                        st.session_state.calendar_month = date(current_month.year, current_month.month + 1, 1)
                    st.rerun()

            # 요일 헤더
            weekday_cols = st.columns(7)
            weekdays = ["일", "월", "화", "수", "목", "금", "토"]
            for col, weekday in zip(weekday_cols, weekdays):
                with col:
                    st.markdown(f"<div class='calendar-weekday'>{weekday}</div>", unsafe_allow_html=True)

            # 달력 날짜 버튼
            month_matrix = pycalendar.Calendar(firstweekday=6).monthdayscalendar(
                st.session_state.calendar_month.year,
                st.session_state.calendar_month.month
            )

            for week_index, week in enumerate(month_matrix):
                day_cols = st.columns(7)
                for col_index, day_num in enumerate(week):
                    with day_cols[col_index]:
                        if day_num == 0:
                            st.write("")
                        else:
                            this_day = date(
                                st.session_state.calendar_month.year,
                                st.session_state.calendar_month.month,
                                day_num
                            )
                            day_events = [e for e in events_on(this_day)
                                          if not e.get('cert') and (e.get('mode') != 'info' or this_day.isoformat() in (e['start'], e['end']))]
                            attendance = st.session_state.attendance_records.get(this_day.isoformat(), {})
                            marker_parts = []
                            if day_events:
                                marker_parts.append("📌")
                            if attendance:
                                marker_parts.append("✓")
                            if this_day == korea_today():
                                marker_parts.append("오늘")
                            marker = " ".join(marker_parts)
                            is_selected = this_day == st.session_state.selected_calendar_date
                            label = f"{day_num}\n{marker}" if marker else str(day_num)
                            if st.button(
                                label,
                                key=f"calendar_day_{this_day.isoformat()}",
                                type="primary" if is_selected else "secondary",
                                use_container_width=True
                            ):
                                st.session_state.selected_calendar_date = this_day
                                st.rerun()

            st.markdown(
                "<div class='calendar-legend'>📌 교육·개인 일정 있음　 ✓ 출결 기록 있음　 날짜를 누르면 상세 내용을 확인할 수 있습니다.</div>",
                unsafe_allow_html=True
            )

            st.divider()
            selected_day = st.session_state.selected_calendar_date
            st.markdown(
                f"<div class='calendar-subtitle'>🗓️ {selected_day.strftime('%Y년 %m월 %d일')} 상세 관리</div>",
                unsafe_allow_html=True
            )

            # 날짜별 할 일: 화면 전환으로 위젯이 사라져도 완료 사전은 유지됩니다.
            tasks = [e for e in events_on(selected_day)
                     if not e.get('cert') and e.get('mode') not in ('info', 'window')]
            title = '오늘의 할 일' if selected_day == korea_today() else f'{selected_day:%m월 %d일} 할 일'
            st.subheader(title)
            if tasks:
                count = sum(bool(st.session_state.calendar_done.get(task_key(e, selected_day))) for e in tasks)
                st.progress(count / len(tasks), text=f'{len(tasks)}개 중 {count}개 완료')
                for item in tasks:
                    tid = task_key(item, selected_day)
                    wk = 'todo_' + tid
                    st.session_state[wk] = st.session_state.calendar_done.get(tid, False)
                    st.checkbox(item['title'], key=wk, on_change=update_done, args=(tid, wk))
            else:
                st.info('선택한 날짜에 등록된 할 일이 없습니다.')
            st.caption('기간 신청은 한 번 완료, 여러 날의 교육·프로젝트는 날짜별 완료로 관리합니다.')
            st.divider()
            st.subheader('가장 가까운 자격증 시험')
            st.multiselect('표시할 자격증', CERT_NAMES,
                           default=st.session_state.cert_preferences, key='cert_filter',
                           on_change=remember_cert_filter)
            cert_notices = nearest_cert_exams(selected_day)
            st.caption(f'{selected_day:%Y년 %m월 %d일} 기준 · 자격증별 가장 가까운 시험')
            if cert_notices:
                cards = []
                for item, registrations in cert_notices:
                    exam_dates = item['start'] + (' ~ ' + item['end'] if item['start'] != item['end'] else '')
                    periods = []
                    for registration in registrations:
                        period = registration['start']
                        if registration['start'] != registration['end']:
                            period += ' ~ ' + registration['end']
                        if registration['stage'] == '접수 마감':
                            period += ' 마감'
                        if period not in periods:
                            periods.append(period)
                    registration_dates = ' / '.join(periods) if periods else '별도 공지'
                    url, label, _ = registration_destination(item['cert'])
                    cards.append(f"""
                    <article class="cert-exam-card">
                      <div class="cert-card-badge">{html.escape(item['attempt'])} · {html.escape(item['stage'])}</div>
                      <h3>{html.escape(item['cert'])}</h3>
                      <dl>
                        <dt>시험일</dt><dd>{html.escape(exam_dates)}</dd>
                        <dt>접수 기간</dt><dd>{html.escape(registration_dates)}</dd>
                      </dl>
                      <a class="cert-apply-link" href="{html.escape(url, quote=True)}" target="_blank" rel="noopener noreferrer">{html.escape(label)} ↗</a>
                    </article>
                    """)
                st.html('<div class="cert-exam-grid">' + ''.join(cards) + '</div>')
            else:
                st.caption('선택한 자격증에 대해 기준일 이후 확인된 시험 일정이 없습니다.')
            st.divider()


            attendance_col, schedule_col = st.columns(2, gap="medium")

            # 출결 관리
            with attendance_col:
                st.markdown("<div class='calendar-subtitle'>✅ 출결 기록</div>", unsafe_allow_html=True)
                saved_attendance = st.session_state.attendance_records.get(selected_day.isoformat(), {})
                with st.form("attendance_form_" + selected_day.isoformat(), clear_on_submit=False):
                    attendance_status = st.selectbox(
                        "출결 상태",
                        # 날짜별 위젯 상태
                        ["미기록", "출석", "지각", "결석", "공결"],
                        key="attendance_status_" + selected_day.isoformat(), index=["미기록", "출석", "지각", "결석", "공결"].index(saved_attendance.get("status", "미기록"))
                    )
                    attendance_memo = st.text_input(
                        "메모",
                        key="attendance_memo_" + selected_day.isoformat(),
                        value=saved_attendance.get("memo", ""),
                        placeholder="출결 관련 메모를 입력하세요."
                    )
                    save_attendance = st.form_submit_button("출결 저장", use_container_width=True)

                if save_attendance:
                    if attendance_status == "미기록":
                        st.session_state.attendance_records.pop(selected_day.isoformat(), None)
                    else:
                        st.session_state.attendance_records[selected_day.isoformat()] = {
                            "status": attendance_status,
                            "memo": attendance_memo
                        }
                    st.success("출결 정보가 저장되었습니다.")
                    st.rerun()

                if saved_attendance:
                    st.caption(
                        f"현재 기록: {saved_attendance.get('status', '')}"
                        + (f" · {saved_attendance.get('memo')}" if saved_attendance.get("memo") else "")
                    )

            # 일정 등록 및 조회
            with schedule_col:
                st.markdown("<div class='calendar-subtitle'>📝 일정 등록</div>", unsafe_allow_html=True)
                with st.form("schedule_form_" + selected_day.isoformat(), clear_on_submit=True):
                    event_title = st.text_input("일정 이름", key="title_" + selected_day.isoformat(), placeholder="예: 데이터 분석 강의")
                    event_type = st.selectbox("일정 유형", ["교육", "과제", "시험", "프로젝트", "개인", "기타"])
                    event_start = st.date_input("시작일", value=selected_day, key="start_" + selected_day.isoformat())
                    event_end = st.date_input("종료일", value=selected_day, key="end_" + selected_day.isoformat())
                    event_memo = st.text_input("상세 내용", placeholder="장소 또는 준비 사항")
                    save_event = st.form_submit_button("일정 추가", use_container_width=True)

                if save_event:
                    if not event_title.strip():
                        st.warning("일정 이름을 입력해 주세요.")
                    elif event_end < event_start:
                        st.warning("종료일은 시작일보다 빠를 수 없습니다.")
                    else:
                        st.session_state.calendar_events.append({
                            "id": str(uuid.uuid4()),
                            "title": event_title.strip(),
                            "type": event_type,
                            "start": event_start.isoformat(),
                            "end": event_end.isoformat(),
                            "mode": "once",
                            "official": False,
                            "memo": event_memo.strip()
                        })
                        st.success("일정이 추가되었습니다.")
                        st.rerun()

            # 선택 날짜 일정 목록 및 삭제
            selected_events = [e for e in events_on(selected_day) if not e.get('cert')]
            if selected_events:
                st.markdown("**등록된 일정**")
                for event in selected_events:
                    event_col, delete_col = st.columns([8, 1])
                    with event_col:
                        date_range = event["start"] if event["start"] == event["end"] else f"{event['start']} ~ {event['end']}"
                        st.markdown(
                            f"📌 **{html.escape(event['title'])}**　`{html.escape(event['type'])}`<br>"
                            f"<span style='color:#8b9aa6;font-size:12px;'>{date_range}"
                            f"{' · ' + html.escape(event['memo']) if event['memo'] else ''}</span>",
                            unsafe_allow_html=True
                        )
                        if event.get('official'):
                            st.caption('출처: ' + event.get('source', '백서') + ' · 시간: ' + event.get('period', '시간 미정'))
                        if event.get('source_url'):
                            st.markdown(f"[일정 출처 열기]({event['source_url']})")
                        if event.get('mode') == 'window':
                            st.caption('시험 시행기간 안내 · 실제 응시일은 수험표 기준입니다. 확정한 개인 시험일은 개인 일정으로 등록하세요.')
                        if event.get('mode') == 'info':
                            st.caption('이용 가능 기간 안내 · 매일 완료할 의무가 있는 일정이 아닙니다.')
                    with delete_col:
                        if not event.get('official') and st.button("🗑️", key=f"delete_event_{event['id']}"):
                            st.session_state.calendar_events = [
                                item for item in st.session_state.calendar_events
                                if item["id"] != event["id"]
                            ]
                            st.rerun()
            else:
                st.caption("선택한 날짜에 등록된 일정이 없습니다.")

        selected = st.session_state.selected_calendar_date
        screen_text = "캘린더 선택일: " + str(selected) + ". 일정: " + "; ".join(
            f"{e['title']} ({e['start']}~{e['end']})" for e in events_on(selected))
    else:

        # 인사말 및 검색창
        title_col, search_col = st.columns(
            [5, 4]
        )

        with title_col:

            st.html("""
            <div class="greeting">
                Hello, AIVLE! 👋
            </div>
            <div class="sub-greeting">
                오늘도 새로운 지식을 함께 배워봐요.
            </div>
            """)

        with search_col:

            st.text_input(
                "검색",
                placeholder="궁금한 내용을 검색해 보세요.",
                label_visibility="collapsed",
                key="search_input",
                on_change=submit_search
            )

        # ======================================
        # 환영 카드
        # ======================================
        card1, card2 = st.columns(2)

        with card1:

            st.html("""
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
            """)

        with card2:

            st.html("""
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
            """)

        # ======================================
        # 주요 기능 카드
        # ======================================
        st.html("""
        <div class="section-title">
            Quick Menu
        </div>
        """)

        f1, f2, f3 = st.columns(3)

        with f1:

            st.html("""
            <div class="feature-card">
                <div class="feature-icon">📚</div>
                <div class="feature-title">학습 자료</div>
                <div class="feature-desc">
                    교육 문서 기반 질문
                </div>
            </div>
            """)

        with f2:

            st.html("""
            <div class="feature-card">
                <div class="feature-icon">🧠</div>
                <div class="feature-title">학습 Q&A</div>
                <div class="feature-desc">
                    AI 문서 검색 및 답변
                </div>
            </div>
            """)

        with f3:

            st.html("""
            <div class="feature-card">
                <div class="feature-icon">🚀</div>
                <div class="feature-title">미니프로젝트</div>
                <div class="feature-desc">
                    프로젝트 정보 확인
                </div>
            </div>
            """)

        quick_cols = st.columns(3)
        for col,label,target in zip(quick_cols,["교육과정 열기","학습 Q&A","포트폴리오 열기"],["edu","intro","portfolio"]):
            with col:
                st.button(label,key="quick_"+target,on_click=navigate,args=(target,),use_container_width=True)

# ==========================================
# 8. 오른쪽 프로필 및 추천 질문
# ==========================================
with right:
    st.html(f"""<div class="profile-card"><div class="profile-icon">{S['emoji']}</div>
    <div class="profile-name">{html.escape(profile['name'])}</div>
    <div class="profile-desc">{S['label']} · {html.escape(profile['track'])}</div></div>""")
    with st.expander("✏️ 프로필 설정"):
        with st.form("profile_form"):
            name = st.text_input("이름(닉네임)",value=profile['name'])
            stage_choice = st.selectbox("나의 단계",list(STAGES),index=list(STAGES).index(stage),format_func=lambda k:STAGES[k]['label'])
            tracks = ["DX 컨설턴트","AI 개발자"]
            track = st.selectbox("트랙",tracks,index=tracks.index(profile['track']))
            if st.form_submit_button("프로필 저장"):
                st.session_state.profile={"name":name.strip() or "에이블러","stage":stage_choice,"track":track}
                st.rerun()
    if st.session_state.active_page == 'calendar':
        with st.container(key='upcoming_panel'):
            st.subheader('🔔 다가오는 일정')
            horizon = st.selectbox('미리 보기', [3, 7, 14, 30], index=1, format_func=lambda n: f'{n}일 이내')
            reminders = []
            for item in visible_events():
                if item.get('cert') or item.get('mode', 'once') != 'once' or st.session_state.calendar_done.get(task_key(item, korea_today())):
                    continue
                remaining = (date.fromisoformat(item['end']) - korea_today()).days
                if -7 <= remaining <= horizon:
                    reminders.append((item['end'], remaining, item))
            for _, remaining, item in sorted(reminders, key=lambda r: (r[0], r[2]['id'])):
                badge = f'{-remaining}일 지남' if remaining < 0 else ('오늘' if remaining == 0 else f'D-{remaining}')
                with st.container(border=True):
                    st.write(f"**{badge} · {item['title']}**")
                    st.caption(item['end'])
            if not reminders:
                st.caption('해당 기간에 미완료 마감·행사 일정이 없습니다.')
            st.caption('최근 7일 미완료 일정 포함 · 앱 안에서 확인하는 알림입니다.')

    with st.container(key="chat_panel"):
        st.markdown("### 🤖 AIVLE 학습 도우미")
        st.caption("대화·작성 문서·완료 표시는 현재 접속 세션에 보관됩니다.")
        documents=st.session_state.get("uploaded_documents",[])
        if documents:
            if st.session_state.get("active_document", 0) >= len(documents):
                st.session_state.active_document = 0
            selected_doc=st.selectbox("등록 문서 선택",range(len(documents)),
                format_func=lambda i:documents[i]['name'],key="active_document")
            if st.button("선택 문서로 질문",key="activate_document"):
                doc=documents[selected_doc]
                st.session_state.upload_chain=doc['chain']
                st.session_state.upload_name=doc['name']
                st.session_state.answer_source="업로드 문서"
        sources=["AIVLE School 백서"]+(["업로드 문서"] if st.session_state.upload_chain else [])
        if st.session_state.answer_source not in sources:
            st.session_state.answer_source=sources[0]
        st.radio("답변 기준",sources,key="answer_source",horizontal=True)
        st.toggle("현재 화면 내용 함께 보내기",key="send_screen")
        for msg in st.session_state.messages[-8:]:
            with st.chat_message(msg['role']): st.markdown(msg['content'])
        if st.session_state.last_sources:
            with st.expander("📄 직전 답변의 근거 문서"):
                for src in st.session_state.last_sources: st.write(src)
        with st.form("chat_form",clear_on_submit=True):
            question=st.text_input("질문",placeholder="궁금한 내용을 질문하세요.")
            submitted=st.form_submit_button("질문 보내기 ➤",use_container_width=True)
        question_text = question.strip() if submitted else st.session_state.pending_prompt
        if question_text:
            st.session_state.pending_prompt=None
            try:
                with st.spinner("문서에서 답변을 찾고 있습니다..."):
                    ensure_rag_imports()
                    from langchain_core.messages import HumanMessage, AIMessage
                    history=[HumanMessage(content=m['content']) if m['role']=='user' else AIMessage(content=m['content'])
                             for m in st.session_state.messages[-6:]]
                    with st.chat_message("assistant"):
                        if st.session_state.answer_source=="업로드 문서":
                            rewritten=rewrite_question(question_text,history)
                            answer=st.write_stream(st.session_state.upload_chain.stream({"input":rewritten}))
                            st.session_state.last_sources=[st.session_state.upload_name]
                        else:
                            stream,docs,search_query=answer_stream(question_text,history,profile_text,
                                screen_text if st.session_state.send_screen else "")
                            answer=st.write_stream(stream)
                            st.session_state.last_sources=[f"쪽 {d.metadata.get('page','?')}: {d.page_content[:200]}" for d in docs]
                st.session_state.messages.extend([{'role':'user','content':question_text},{'role':'assistant','content':answer}])
                now=datetime.now(ZoneInfo('Asia/Seoul'))
                st.session_state.archive.append({'id':uuid.uuid4().hex,'date':now.strftime('%Y-%m-%d'),
                    'time':now.strftime('%H:%M'),'stage':S['label'],'page':st.session_state.active_page,
                    'source':st.session_state.answer_source,'question':question_text,'answer':answer})
                st.rerun()
            except Exception as exc:
                st.error(f"답변을 생성하지 못했습니다: {exc}")
    st.markdown("### 💡 추천 질문")
    for i,q in enumerate(S['questions']):
        st.button(q,key=f"recommend_{i}",on_click=ask,args=(q,),use_container_width=True)
