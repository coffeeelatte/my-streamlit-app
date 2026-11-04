
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
당신의 주요 업무 중 하나는 미팅내용을 요약하여 사용자의 업무를 파악해 전달하는 것입니다.
"""
# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant",
                                  "content": "안녕하세요. 무엇을 도와드릴까요?"}]

# 기존 대화 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# 사용자 음성 입력
# 지시 영역
with st.form("task_form"):
    uploaded_file = st.file_uploader("텍스트 파일 업로드", type=["txt"])
    audio_value = st.audio_input("무엇을 도와드릴까요?")
    submit = st.form_submit_button("실행")


# 버튼을 눌렀을 때만 실행
if submit:
    # 업로드 된 파일이 있으면 디코딩
    text = ""
    if uploaded_file is not None:
        text = uploaded_file.read().decode("utf-8")

    # 녹음이 없으면 녹음 요청
    if audio_value is None:
        st.warning("음성을 녹음해주세요.")
        st.stop()

    # 시스템 메세지
    system_content = sys_role
    if text:
        system_content += f"\n\n다음 내용을 참고하세요:\n{text}"
    input_messages = [{"role": "system", "content": system_content}]

    # STT: 음성 → 텍스트
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=("audio.wav", audio_value, "audio/wav"))

    # 사용자 메시지
    input_messages.append({"role": "user", "content": transcript.text})
    
    # 사용자 메시지 저장 및 출력
    st.session_state.messages.append(
        {"role": "user", "content": transcript.text})
    with st.chat_message("user"):
        st.markdown(transcript.text)

    # 모델 응답 생성
    with st.spinner("답변을 준비하고 있습니다..."):
      try:
          response = client.responses.create(
              model="gpt-4.1-mini",
              input=input_messages
          )
          assistant_reply = response.output_text
      except Exception as e:
          assistant_reply = f"오류가 발생했습니다: {e}"

      # 응답 저장 및 출력
      st.session_state.messages.append(
          {"role": "assistant", "content": assistant_reply}
      )
      with st.chat_message("assistant"):
          st.markdown(assistant_reply)

