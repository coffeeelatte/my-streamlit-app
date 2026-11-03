
import os
import streamlit as st
from openai import OpenAI

# 1. 페이지 설정
st.set_page_config(page_title="AI비서 에이블", 
                   page_icon="😊",
                   layout="wide"
)

# 2. 사이드바: 서비스 선택
st.sidebar.title("서비스 메뉴")

service = st.sidebar.radio(
    "사용할 서비스를 선택하세요",
    ["홈", "글자 수 세기", "계산기"]
)

# 3. 본문: 선택한 서비스에 따라 다른 화면 표시
if service == "홈":
    st.title("나의 서비스 모음")
    st.write("왼쪽 사이드바에서 사용할 서비스를 선택하세요.")



elif service == "멀티턴 챗":
  # OpenAI 클라이언트 생성
  client = OpenAI()

  # 페이지 설정
  st.title("🤖 OpenAI API 기반 챗봇")
  st.caption("Streamlit + OpenAI API 실습 예제")

  # 세션 상태 초기화
  if "messages" not in st.session_state:
      st.session_state.messages = [{"role": "assistant",
                                  "content": "안녕하세요. 무엇을 도와드릴까요?"}]

  # 기존 대화 출력
  for message in st.session_state.messages:
      with st.chat_message(message["role"]):
          st.markdown(message["content"])

  # 사용자 입력
  user_input = st.chat_input("메시지를 입력하세요...")

  if user_input:
      # 사용자 메시지 저장 및 출력
      st.session_state.messages.append(
          {"role": "user", "content": user_input}
      )
      with st.chat_message("user"):
          st.markdown(user_input)
      
      # 모델 응답 생성
      try:
        response = client.responses.create(
            model="gpt-4o-mini",
            input=st.session_state.messages
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




elif service == "계산기":
    st.title("두 수 더하기")

    num1 = st.number_input("첫 번째 숫자", value=0.0)
    num2 = st.number_input("두 번째 숫자", value=0.0)

    if st.button("계산하기"):
        result = num1 + num2
        st.success(f"계산 결과: {result}")
