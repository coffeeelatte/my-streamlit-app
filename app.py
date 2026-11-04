
import os, base64, json, requests
import streamlit as st
from openai import OpenAI

# OpenAI 클라이언트 생성
client = OpenAI()

# 페이지 설정
st.set_page_config(page_title="AI 비서 에이블", page_icon="😊", layout="wide")
st.title("😊 AI음성비서 에이블입니다.")
st.write("음성으로 질문하시면 답변해 드립니다.")

# 역할 지정
sys_role = """
당신은 다양한 업무를 처리하는 AI 개인 비서 "에이블"입니다.
개인 비서처럼 친절하게 응대합니다.
답변은 사용자가 듣기 편하도록 구어체를 사용합니다.
"""
# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant",
                                  "content": "안녕하세요. 무엇을 도와드릴까요?"}]

# 대화 영역 생성: 높이가 고정되어 있어야 자동 스크롤이 작동함
chat_area = st.container(
    height=450,
    border=False,
    autoscroll=True
)

# 기존 대화 출력
with chat_area:
  for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# 사용자 음성 입력
# 지시 영역
# 화면 하단에 입력 영역 고정
with st.bottom:
    with st.form("task_form"):
        uploaded_file = st.file_uploader(
            "텍스트 파일 업로드",
            type=["txt"]
        )

        audio_value = st.audio_input("무엇을 도와드릴까요?")
        submit = st.form_submit_button("실행")


# 버튼을 눌렀을 때만 실행
# 버튼을 눌렀을 때만 실행
if submit:
    # 1. 녹음 여부 확인
    if audio_value is None:
        st.warning("음성을 녹음해주세요.")
        st.stop()

    # 2. 참고자료 읽기
    text = ""

    if uploaded_file is not None:
        try:
            text = uploaded_file.getvalue().decode("utf-8-sig")
        except UnicodeDecodeError:
            st.error("텍스트 파일을 UTF-8 형식으로 저장한 뒤 업로드해주세요.")
            st.stop()

    # 3. 시스템 메시지 구성
    system_content = sys_role

    if text:
        system_content += f"\n\n다음 내용을 참고하세요:\n{text}"

    # 4. STT: 음성 → 텍스트
    with st.spinner("음성을 텍스트로 변환하고 있습니다..."):
        try:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=("audio.wav", audio_value.getvalue(), "audio/wav")
            )
            user_text = transcript.text.strip()

        except Exception as e:
            st.error(f"음성 변환 중 오류가 발생했습니다: {e}")
            st.stop()

    if not user_text:
        st.warning("인식된 내용이 없습니다. 다시 녹음해주세요.")
        st.stop()

    # 5. 사용자 메시지 저장 및 출력
    st.session_state.messages.append(
        {"role": "user", "content": user_text}
    )

    with chat_area:
      with st.chat_message("user"):
        st.markdown(user_text)

    # 6. 시스템 지침 + 이전 대화 + 이번 질문 전달
    # 이번 질문은 위에서 messages에 이미 저장했으므로 다시 추가하지 않음
    input_messages = [
        {"role": "system", "content": system_content}
    ] + st.session_state.messages

    # 7. 답변 생성
    with st.spinner("답변을 준비하고 있습니다..."):
        try:
            response = client.responses.create(
                model="gpt-4.1-mini",
                input=input_messages
            )
            assistant_reply = response.output_text

        except Exception as e:
            st.error(f"답변 생성 중 오류가 발생했습니다: {e}")
            st.stop()

    # 8. 정상적으로 생성된 답변만 저장 및 출력
    st.session_state.messages.append(
        {"role": "assistant", "content": assistant_reply}
    )

    # 답변을 화면에 출력
    with chat_area:
      with st.chat_message("assistant"):
        st.markdown(assistant_reply)

        # TTS: 답변 텍스트 → 음성
        with st.spinner("답변을 음성으로 변환하고 있습니다..."):
            try:
                speech = client.audio.speech.create(
                    model="gpt-4o-mini-tts",
                    voice="nova",
                    input = assistant_reply)
                audio_bytes = speech.content
                
                # 음성 출력
                st.caption("🔊 AI 음성 재생")
                st.audio(speech.content, format="audio/mp3",autoplay=True)

            except Exception as e:
                st.error(f"음성 생성 중 오류가 발생했습니다: {e}")
