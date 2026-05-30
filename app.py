
# 유튜브 내용 요약하는 Streamlit을 만들어서 배포해보기
import traceback
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import YoutubeLoader  # 유튜브 로더 추가
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()

# 1. 프롬프트 개선 (출력 형식을 조금 더 명확하게 지시)
SUMMARIZE_PROMPT = """다음 제공된 유튜브 영상 스크립트의 핵심 내용을 약 300자 내외로 알기 쉽게 요약해주세요.
반드시 한국어로 자연스럽게 작성해야 합니다.

========
{content}
========
"""

def init_page():
    st.set_page_config(page_title="유튜브 영상 요약기", page_icon="🤗")
    st.header("유튜브 영상 요약기 🤗")
    st.sidebar.title("Options")

def select_model(temperature = 0):
    models = ("gpt-5.5", "gpt-5.4-mini")
    model = st.sidebar.radio("Choose a model:", models)
    if model == 'gpt-5.5':
        return ChatOpenAI(temperature = temperature, model = 'gpt-5.5')
    else:
        return ChatOpenAI(temperature = temperature, model = 'gpt-5.4-mini')

def init_chain():
    llm = select_model()
    prompt = ChatPromptTemplate.from_messages([
        ('user', SUMMARIZE_PROMPT)])
    chain = prompt | llm | StrOutputParser()
    return chain

# 2. 기존 웹 크롤링 대신 유튜브 자막을 가져오는 함수로 변경
def get_youtube_content(url):
    with st.spinner('유튜브 영상에서 자막 다운로드 중...'):
        try:
            # 한국어('ko')를 먼저 시도하고, 없으면 영어('en') 자막을 가져옵니다.
            loader = YoutubeLoader.from_youtube_url(url, add_video_info=False, language=['ko', 'en'])
            docs = loader.load()

            # 자막 텍스트만 합쳐서 반환합니다.
            return docs[0].page_content
        except Exception as e:
            st.error(f"자막을 가져오지 못했습니다. 자막이 지원되지 않는 영상이거나 에러가 발생했습니다: {e}")
            return None


def get_content(url):
    with st.spinner('웹 사이트 정보 찾는중...'):
        url = requests.get(url)
        html = BeautifulSoup(url.text)
        if html.main:
            return html.main.text
        elif html.article:
            return html.article.text
        else:
            return html.body.text

def main():
    init_page()
    chain = init_chain()

    # 입력창 안내 문구를 유튜브 URL로 변경
    if url := st.text_input("유튜브 URL을 입력하세요: ", key = 'input'):
        if content := get_youtube_content(url):
            st.markdown("## Summary")
            st.write_stream(chain.stream({'content' : content}))
            st.markdown("-----")
            st.markdown("## Original Transcript (자막 원본)")
            st.write(content)

main()
