
import os
import streamlit as st
from openai import OpenAI

# OpenAI 클라이언트 생성
client = OpenAI()

# 페이지 설정
st.set_page_config(page_title="다국어 번역기", page_icon="😊")
st.title("😊간단한 다국어 번역기")
st.write("한국어를 입력하면, 다양한 언어로 번역합니다.")

# 사용자 입력(텍스트)
korean_text = st.text_area(
    "번역할 한글 문장을 입력하세요.",
    height=150,
    placeholder="예: 인공지능은 우리의 일상과 업무 방식을 빠르게 변화시키고 있습니다."
)
language = st.selectbox("언어선택",["영어", "일본어", "중국어", "불어", "독일어"], index=0)

# 번역 버튼
if st.button("번역하기"):

    if not korean_text.strip():
        st.warning("한국어가 입력되지 않았스빈다.")
    else:
        with st.spinner("번역 중입니다..."):

            # 시스템 역할
            sys_role = """
            당신은 한국에서 활동하는 국제번역가 입니다.
            당신은 주로 영어, 일본어, 중국어, 불어, 독일어로 한국어를 번역을 합니다.


            """

            # 프롬프트 구성
            prompt = f"""
            다음 문장을 {language}로 번역하세요.
            ---
            "{korean_text}"
            """

            # GPT 호출
            response = client.responses.create(
                model="gpt-4o-mini",
                input=[
                    {"role": "system", "content": sys_role},
                    {"role": "user", "content": prompt}
                ]
            )

            # 결과 출력
            translated_text = response.output_text
            st.write(translated_text)

            st.subheader(f"{language}로 번역한 결과")
            st.success("번역이 성공적으로 완료되었습니다.")
