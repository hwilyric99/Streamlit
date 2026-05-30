import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# 환경 변수 로드
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(
    page_title="AI English Conversation Coach",
    page_icon="🗣️",
    layout="wide"
)

st.title("🗣️ AI English Conversation Coach")
st.write("영어 회화를 쉽고 재미있게 연습해보세요!")

# 사이드바
st.sidebar.header("학습 설정")

scenario = st.sidebar.selectbox(
    "상황 선택",
    ["Cafe", "Airport", "Shopping", "Job Interview", "Daily Conversation"]
)

level = st.sidebar.selectbox(
    "영어 수준",
    ["Beginner", "Intermediate"]
)

topic = st.text_input("연습하고 싶은 주제를 입력하세요", "Ordering coffee")

if st.button("대화 생성하기"):

    prompt = f"""
    Create an English conversation practice lesson.

    Scenario: {scenario}
    Level: {level}
    Topic: {topic}

    Please provide:

    1. Short English dialogue
    2. Korean translation
    3. Key expressions with explanation
    4. Easier alternative expressions
    5. Practice question for the learner

    Keep it beginner-friendly if level is Beginner.
    """

    with st.spinner("AI가 대화를 생성 중입니다..."):

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        result = response.choices[0].message.content

    st.success("생성 완료!")

    st.markdown("## 📚 학습 결과")
    st.write(result)
