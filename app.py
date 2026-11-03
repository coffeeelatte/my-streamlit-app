
import streamlit as st

# 1. 페이지 설정
st.set_page_config((page_title="AI비서 에이블", page_icon="😊"
    page_title="에이블의 기능들",
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

elif service == "글자 수 세기":
    st.title("글자 수 세기")

    text = st.text_area("글을 입력하세요")

    if st.button("글자 수 확인"):
        st.success(f"공백 포함 총 {len(text)}자입니다.")

elif service == "계산기":
    st.title("두 수 더하기")

    num1 = st.number_input("첫 번째 숫자", value=0.0)
    num2 = st.number_input("두 번째 숫자", value=0.0)

    if st.button("계산하기"):
        result = num1 + num2
        st.success(f"계산 결과: {result}")
