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

</style>
""", unsafe_allow_html=True)


# ==========================================
# 3. RAG 설정
# ==========================================
CHROMA_DIR = "chroma_db"
COLLECTION = "aivle_docs"


# 문서 포맷팅 함수
def format_docs(docs):
    return "\n\n".join(
        doc.page_content for doc in docs
    )


# Embedding 및 검색기
@st.cache_resource
def get_retriever():
    from langchain_openai import OpenAIEmbeddings
    from langchain_chroma import Chroma

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


# RAG 체인
@st.cache_resource
def get_chain():
    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser

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
        category='자격증', type='자격증', mode='window' if window else 'once',
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

CERT_NAMES = sorted({e['cert'] for e in CERT_EVENTS})
DEFAULT_CERTS = [name for name in CERT_NAMES if name != 'IT-PMP']


def remember_cert_filter():
    st.session_state.cert_preferences = list(st.session_state.cert_filter)


def visible_events():
    chosen = st.session_state.get('cert_preferences', DEFAULT_CERTS)
    return [e for e in st.session_state.calendar_events
            if not e.get('cert') or e['cert'] in chosen]


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
    # 나머지 팀 메뉴(기존 디자인)
    st.html("""
    <div class="menu-item">
        👋　소개
    </div>
    <div class="menu-item">
        📚　교육과정
    </div>
    <div class="menu-item">
        💼　취업과정
    </div>
    <div class="menu-item">
        🗂️　포트폴리오
    </div>
    <div class="menu-item">
        📂　파일 불러오기
    </div>
    <div class="menu-item">
        🧩　온톨로지
    </div>
    """)

    st.markdown("<br>", unsafe_allow_html=True)

    # 관리자
    st.html("""
    <p style="font-size:14px;font-weight:800;color:white;">
        ⚙️ 관리자
    </p>
    """)

    uploaded_file = st.file_uploader(
        "파일 업로드",
        type=["pdf", "txt", "docx"]
    )

    if uploaded_file is not None:
        st.success(
            f"{uploaded_file.name} 선택됨"
        )

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
with left:
    if st.session_state.active_page == 'calendar':
        # ======================================
        # 출결 및 일정 관리 달력
        # ======================================
        st.html("""
        <div class="section-title">📅 출결 & 일정 관리</div>
        <div class="calendar-caption">
            백서 일정과 오늘의 할 일을 확인하세요. 출결 기록은 개인 메모이며 공식 출결과 연동되지 않습니다.
        </div>
        """)

        st.multiselect('표시할 자격증', CERT_NAMES,
                       default=st.session_state.cert_preferences, key='cert_filter',
                       on_change=remember_cert_filter)
        st.caption('자격증은 참고 일정으로 표시하며 할 일에 자동 등록하지 않습니다. 응시할 시험은 개인 일정으로 추가하세요.')
        st.caption(f'한국시간 기준 오늘 · {korea_today():%Y년 %m월 %d일}')
        if st.button('오늘로 이동', key='calendar_today'):
            st.session_state.selected_calendar_date = korea_today()
            st.session_state.calendar_month = korea_today().replace(day=1)
            st.rerun()
        jump = st.date_input('날짜로 바로 이동', value=st.session_state.selected_calendar_date,
                             key='calendar_jump_' + st.session_state.selected_calendar_date.isoformat())
        if jump != st.session_state.selected_calendar_date:
            st.session_state.selected_calendar_date = jump
            st.session_state.calendar_month = jump.replace(day=1)
            st.rerun()
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
                                          if e.get('mode') != 'info' or this_day.isoformat() in (e['start'], e['end'])]
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
                "<div class='calendar-legend'>📌 일정 있음　 ✓ 출결 기록 있음　 날짜를 누르면 상세 내용을 확인할 수 있습니다.</div>",
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
            st.subheader('자격증 접수·시험 안내')
            cert_notices = [e for e in events_on(selected_day) if e.get('cert')]
            st.caption('선택한 날짜의 참고 정보입니다. 개인 응시 일정이나 완료 체크 대상이 아닙니다.')
            if cert_notices:
                for item in cert_notices:
                    with st.container(border=True):
                        st.write('**' + item['title'] + '**')
                        st.caption(item['start'] + (' ~ ' + item['end'] if item['start'] != item['end'] else ''))
                        if item.get('mode') == 'window':
                            st.caption('시행기간 안내 · 개인 응시일은 수험표에서 확인하세요.')
                        if item.get('memo'):
                            st.caption(item['memo'])
                        st.markdown(f"[접수·시험 안내 확인]({item['source_url']})")
            else:
                st.caption('선택한 자격증의 접수·시험 안내가 없습니다.')
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

        # ======================================
        # 채팅 영역
        # ======================================
        st.html("""
        <div class="section-title">
            💬 AI Learning Assistant
        </div>
        """)

        with st.container(key="chat_panel"):

            st.html("""
            <div class="chat-heading">
                🤖 AIVLE School 학습 도우미
            </div>
            <div class="chat-description">
                궁금한 내용을 질문하면 관련 문서를 찾아
                답변해 드립니다.
            </div>
            """)

            # 최초 안내 메시지
            if not st.session_state.messages:

                st.info(
                    "안녕하세요! 😊 무엇이 궁금하신가요? "
                    "아래 입력창에 질문을 작성해 주세요."
                )

            # 기존 대화 출력
            for message in st.session_state.messages:

                role = (
                    "user"
                    if message["role"] == "user"
                    else "assistant"
                )

                with st.chat_message(role):
                    st.markdown(message["content"])

            # 채팅 입력창
            with st.form(
                "chat_form",
                clear_on_submit=True
            ):

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

    # 프로필
    st.html("""
    <div class="profile-card">
        <div class="profile-icon">
            👩🏻‍💻
        </div>
        <div class="profile-name">
            AIVLE Assistant
        </div>
        <div class="profile-desc">
            Your Learning Partner
        </div>
    </div>
    """)

    if st.session_state.active_page == 'calendar':
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
        st.divider()
        st.markdown('**AX 챌린지 자격증**')
        st.caption('2026년 시험·접수 일정과 공식 발표가 확인된 2027년 1~3월 COS Pro 일정을 제공합니다. 확인 기준: ' + CERT_CHECKED)
        with st.expander('자격증 일정 이용 안내'):
            st.markdown('[Azure Associate·Expert 시험 예약](https://learn.microsoft.com/en-us/credentials/certifications/register-schedule-exam)')
            st.write('Azure는 개별 예약형입니다. 예약한 시험일을 개인 일정으로 추가하세요.')
            st.caption('ADP·DAP 일정은 사용자가 공식 문서와 대조해 확인한 내용입니다.')
            st.write('IT-PMP는 교육기관 게재 공고를 근거로 합니다. 필요하면 자격증 필터에서 선택하세요. 시행기관 원문은 미대조입니다.')
            st.write('구 정보처리기능사는 프로그래밍기능사, 구 전자계산기기사·전자계산기조직응용기사는 컴퓨터시스템기사 명칭으로 표시합니다. 변경 명칭의 AX 인정 여부는 교육 운영진에게 확인하세요.')
            st.write('추가 9종의 AX 적용일은 제공받은 안내 기준 2026-11-09입니다. 시험 일정 표시와 지원금·공결 인정 여부는 별개입니다.')
        st.caption('교육 일정은 백서, 시험 일정은 각 일정의 출처 기준입니다. 접수 전 최신 공지를 확인하세요.')
        st.caption('완료·개인 일정·출결 메모는 현재 접속 세션에서 유지됩니다. 재접속 후 영구 보존은 지원하지 않습니다.')
    else:
        # 학습 도우미 안내
        st.html("""
        <div class="info-card">
            <div class="info-title">
                📘 학습 도우미 안내
            </div>
            <p>
                AIVLE School 교육 자료를 기반으로
                질문에 대한 답변을 제공합니다.<br><br>
                <b style="color:#29445b;">
                    RAG 기반 문서 검색
                </b><br>
                관련 문서를 검색하고 답변을 생성합니다.
            </p>
        </div>
        """)

        # 추천 질문
        st.html("""
        <div class="section-title">
            💡 추천 질문
        </div>
        """)

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

        st.html("""
        <div class="info-card">
            <div class="info-title">
                🕒 Recent Activity
            </div>
            <p>
                최근 대화 기록
            </p>
        </div>
        """)

        recent_questions = [
            msg["content"]
            for msg in reversed(st.session_state.messages)
            if msg["role"] == "user"
        ]

        if recent_questions:

            for q in recent_questions[:5]:
                st.caption("💬 " + q[:35])

        else:

            st.caption("아직 대화 기록이 없습니다.")


# ==========================================
# 9. RAG 질문 처리
# ==========================================
prompt = None

# 직접 입력한 질문
if submitted and question.strip():

    prompt = question.strip()

# 추천 질문 또는 검색창 질문
elif st.session_state.active_page == "home" and st.session_state.pending_prompt:

    prompt = st.session_state.pending_prompt


if prompt:

    st.session_state.pending_prompt = None

    # 사용자 질문 저장
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    try:

        chain = get_chain()

        with st.spinner(
            "관련 문서를 검색하고 있습니다..."
        ):

            with st.chat_message("assistant"):

                response_stream = chain.stream({
                    "input": prompt
                })

                full_response = st.write_stream(
                    response_stream
                )

        # AI 답변 저장
        st.session_state.messages.append(
            {"role": "assistant", "content": full_response}
        )

    except Exception as e:

        st.error(
            f"답변 생성 중 오류가 발생했습니다: {e}"
        )

    st.rerun()
