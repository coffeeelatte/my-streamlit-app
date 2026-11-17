import calendar
import html
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

import streamlit as st

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

COLORS = {'교육': '#dcecfb', '프로젝트': '#e8e1f8', '취업지원': '#d8f1ec', '개인': '#fff0d9', '자격증': '#ffe4e9'}


def occurs(e, day):
    return date.fromisoformat(e['start']) <= day <= date.fromisoformat(e['end'])


def completion_key(e, day):
    return e['id'] + (':' + day.isoformat() if e['mode'] == 'daily' else '')


def month_shift(day, amount):
    index = day.year * 12 + day.month - 1 + amount
    year, month = divmod(index, 12)
    return date(year, month + 1, 1)


def reminder_items(events, today, done, horizon=7):
    reminders = []
    for e in events:
        if e['mode'] != 'once' or done.get(completion_key(e, today), False):
            continue
        deadline = date.fromisoformat(e['end'])
        days = (deadline - today).days
        # 최근 7일 미완료 및 향후 알림 기간만 표시합니다.
        if -7 <= days <= horizon:
            label = f'{-days}일 지남' if days < 0 else ('오늘' if days == 0 else f'D-{days}')
            reminders.append((deadline, label, e))
    return sorted(reminders, key=lambda item: (item[0], item[2]['id']))


def render_calendar(events=None, key='aivle_calendar'):
    """팀 앱 메인 영역에서 호출합니다. 데이터·체크는 현재 브라우저 세션별로 분리됩니다."""
    today = korea_today()
    if key not in st.session_state:
        st.session_state[key] = {'selected': today, 'month': today.replace(day=1),
                                 'done': {}, 'personal': []}
    state = st.session_state[key]
    all_events = list(EVENTS if events is None else events) + state['personal']

    def choose(day):
        state['selected'] = day
        state['month'] = day.replace(day=1)
        st.session_state[key + '_date'] = day

    def change_month(amount):
        choose(month_shift(state['month'], amount))

    def date_changed():
        choose(st.session_state[key + '_date'])

    def mark(eid, widget):
        state['done'][eid] = st.session_state[widget]

    st.markdown('<div class="greeting">My AIVLE Calendar 🗓️</div>', unsafe_allow_html=True)
    st.caption(f'한국시간 기준 오늘 · {today:%Y년 %m월 %d일} | 에이블스쿨 10기 DX')
    st.caption('교육 · 프로젝트 · 취업지원 일정을 한눈에 확인하세요.')

    prev, heading, nxt, current = st.columns([1, 4, 1, 2])
    prev.button('◀', key=key+'_prev', on_click=change_month, args=(-1,), use_container_width=True)
    heading.markdown(f'### {state["month"]:%Y년 %m월}')
    nxt.button('▶', key=key+'_next', on_click=change_month, args=(1,), use_container_width=True)
    current.button('오늘', key=key+'_today', on_click=choose, args=(today,), use_container_width=True)
    st.session_state.setdefault(key + '_date', state['selected'])
    st.date_input('날짜로 바로 이동', key=key+'_date', min_value=date(2020,1,1),
                  max_value=date(2040,12,31), on_change=date_changed)

    with st.container(border=True):
        for col, name in zip(st.columns(7), ['월', '화', '수', '목', '금', '토', '일']):
            col.markdown(f'**{name}**')
        month = state['month']
        for week in calendar.Calendar(firstweekday=0).monthdatescalendar(month.year, month.month):
            for col, day in zip(st.columns(7), week):
                with col:
                    # 장기 이용 기간은 시작·종료일만 달력에 표시해 반복 표시를 줄입니다.
                    displayed = [e for e in all_events if occurs(e, day) and
                                 (e['mode'] != 'info' or day.isoformat() in (e['start'], e['end']))]
                    label = str(day.day) + (' 오늘' if day == today else '')
                    st.button(label, key=f'{key}_day_{day}', disabled=day.month != month.month,
                              type='primary' if day == state['selected'] else 'secondary',
                              use_container_width=True, on_click=choose, args=(day,))
                    for e in displayed[:2]:
                        color = COLORS.get(e['category'], '#e9eef2')
                        st.markdown(f'<div class="cal-event" style="background:{color}" title="{html.escape(e["title"], quote=True)}">{html.escape(e["title"])}</div>', unsafe_allow_html=True)
                    if len(displayed) > 2:
                        st.caption(f'+{len(displayed)-2}개')
                    if not displayed:
                        st.markdown('<div style="height:32px"></div>', unsafe_allow_html=True)

    selected = state['selected']
    active = [e for e in all_events if occurs(e, selected)]
    tasks = [e for e in active if e['mode'] != 'info']
    info = [e for e in active if e['mode'] == 'info']
    st.subheader('오늘의 할 일' if selected == today else f'{selected.month:02}월 {selected.day:02}일 할 일')
    st.caption(f'{selected:%Y.%m.%d} · 체크는 개인의 준비·참여 완료 표시이며 공식 출결 처리가 아닙니다.')
    completed = sum(bool(state['done'].get(completion_key(e, selected))) for e in tasks)
    if tasks:
        st.progress(completed / len(tasks), text=f'{len(tasks)}개 중 {completed}개 완료')
        for e in tasks:
            ck = completion_key(e, selected)
            wk = key + '_check_' + ck
            # 위젯이 사라져도 완료 기록은 별도 done 사전에 보관합니다.
            st.session_state[wk] = state['done'].get(ck, False)
            st.checkbox(e['title'], key=wk, on_change=mark, args=(ck, wk))
    else:
        st.info('이 날짜에 등록된 할 일이 없습니다.')

    with st.expander('＋ 선택한 날짜에 개인 할 일 추가'):
        with st.form(key + '_personal_form', clear_on_submit=True):
            title = st.text_input('할 일', max_chars=100)
            memo = st.text_area('메모', max_chars=1000)
            if st.form_submit_button('추가하기'):
                if title.strip():
                    from uuid import uuid4
                    state['personal'].append(event('personal-'+uuid4().hex, title.strip(),
                        selected.isoformat(), category='개인', description=memo, source='직접 작성'))
                    st.rerun()
                else:
                    st.warning('할 일을 입력해 주세요.')

    if active:
        st.subheader('일정 상세')
        for e in tasks + info:
            prefix = '이용 안내 · ' if e['mode'] == 'info' else ''
            with st.expander(prefix + e['title']):
                st.write(f'**기간:** {e["start"]} ~ {e["end"]} (종료일 포함)')
                st.write(f'**시간:** {e["period"]}  |  **분류:** {e["category"]}')
                if e['description']:
                    st.write(e['description'])
                st.caption('출처: ' + e['source'])
                if e['mode'] == 'once' and e['start'] != e['end']:
                    st.caption('기간 중 한 번 완료하면 다른 날짜에서도 완료로 표시됩니다.')
    return state, all_events


def render_reminders(state, events):
    st.markdown('<div class="profile-card"><div class="profile-icon">👩🏻‍💻</div><div class="profile-name">AIVLE Planner</div><div class="profile-desc">차근차근, 오늘의 한 걸음</div></div>', unsafe_allow_html=True)
    st.subheader('🔔 다가오는 일정')
    horizon = st.selectbox('미리 보기', [3, 7, 14, 30], index=1, format_func=lambda n: f'{n}일 이내', key='cal_horizon')
    reminders = reminder_items(events, korea_today(), state['done'], horizon)
    if not reminders:
        st.caption('선택한 기간에 미완료 마감·행사 일정이 없습니다.')
    for deadline, label, e in reminders:
        with st.container(border=True):
            st.markdown(f'**{label} · {e["title"]}**')
            st.caption(f'{deadline:%Y.%m.%d} · {e["category"]}')
    st.caption('앱 안에서 확인하는 알림입니다. 이메일·푸시는 발송하지 않습니다. 최근 7일 미완료 일정도 표시합니다.')
    st.divider()
    st.markdown('**AX 챌린지 자격증**')
    st.caption('시험 접수일·시험일은 자료를 받은 뒤 추가합니다.')
    st.markdown('**일정 안내**')
    st.caption('백서에 명시된 날짜를 수록했습니다. 운영 변경은 공식 공지를 확인하세요. 시간 미정은 임의로 지정하지 않았습니다.')
    st.caption('완료 체크와 개인 할 일은 현재 브라우저 세션에서 유지됩니다. 새로고침·재접속 후 영구 보존은 아직 지원하지 않습니다.')


st.set_page_config(page_title="AIVLE 일정 캘린더", page_icon="🗓️", layout="wide")
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
#MainMenu, footer {
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



st.markdown("""<style>
.cal-event {font-size:11px;color:#19334d;border-radius:6px;padding:4px 5px;margin-bottom:4px;overflow-wrap:anywhere;line-height:1.4;}
div[data-testid="stVerticalBlockBorderWrapper"] {background:white;border-radius:14px;}
button[kind="primary"] {background:#269eaa !important;color:white !important;border-color:#269eaa !important;}
</style>""", unsafe_allow_html=True)
with st.sidebar:
    st.markdown('<div class="logo-area"><strong style="color:#269eaa;font-size:24px">AIVLE</strong><br><span style="color:#91a2ae">LEARNING PLANNER</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="menu-item menu-active">🗓️ 일정 캘린더</div>', unsafe_allow_html=True)
    st.caption('10기 DX 컨설턴트 트랙')
    st.markdown('교육과 취업 준비 일정을 확인하고 오늘의 할 일을 체크해 보세요.')
left, right = st.columns([7, 3], gap="large")
with left:
    state, events = render_calendar()
with right:
    render_reminders(state, events)
