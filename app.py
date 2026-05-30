import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(
    page_title="AI Stock Research Analyzer",
    page_icon="📈",
    layout="wide"
)

st.title("📈 AI Stock Research Analyzer")
st.markdown("AI 기반 주식 분석 및 투자 인사이트 제공 시스템")

# 입력 영역
col1, col2 = st.columns(2)

with col1:
    company = st.text_input(
        "기업명 입력",
        "NVIDIA"
    )

with col2:
    analysis_type = st.selectbox(
        "분석 유형",
        [
            "Basic Analysis",
            "Growth Potential",
            "Risk Analysis",
            "Investment Strategy"
        ]
    )

risk_level = st.select_slider(
    "투자 성향",
    options=["Conservative", "Balanced", "Aggressive"]
)

if st.button("주식 분석 실행"):

    prompt = f"""
    Analyze the stock: {company}

    Analysis Type: {analysis_type}
    Investor Risk Profile: {risk_level}

    Provide:

    1. Company Overview
    2. Key Growth Drivers
    3. Potential Risks
    4. Market Outlook
    5. Investment Recommendation
    6. Beginner-Friendly Explanation

    Format clearly with headings.

    모든 답변은 한국어로 작성해주세요.
    """

    with st.spinner("분석 중..."):

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        result = response.choices[0].message.content

    st.success("분석 완료!")

    st.markdown("## 📊 Analysis Result")
    st.markdown(result)

# 하단 설명
st.markdown("---")
st.info("※ 본 분석은 AI 기반 참고 자료이며 실제 투자 판단의 책임은 사용자에게 있습니다.")
