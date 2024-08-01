import textwrap
import google.generativeai as genai
import streamlit as st
import pathlib
import toml

def to_markdown(text):
    text = text.replace('•', '*')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

# secrets.toml 파일 경로
secrets_path = pathlib.Path(__file__).parent.parent / ".streamlit/secrets.toml"

# secrets.toml 파일 읽기
with open(secrets_path, "r") as f:
    secrets = toml.load(f)

# secrets.toml 파일에서 API 키 값 가져오기
api_key = secrets.get("api_key")

# few-shot 프롬프트 구성 함수 수정
def generate_science_competition_info(api_key, competition_name):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config={
            "temperature": 0.7,
            "top_p": 0.9,
            "top_k": 40,
            "max_output_tokens": 256,
        },
        safety_settings=[
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        ]
    )
    prompt = f"""
    다음 과학 대회에 대한 안내문을 작성해줘.
    학기초에 학생들이 참가할 수 있도록, 대회 목적, 참가 방법, 일정 등의 정보를 간략하게 포함해야 해.

    대회 이름: {competition_name}

    안내문:
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"API 호출 실패: {e}")
        return None

# 스트림릿 앱 인터페이스 구성
st.title("교내 과학 대회 안내")

# 사용자 입력 받기
competition_name = st.selectbox("대회를 선택하세요.", ["학생과학발명품경진대회", "청소년과학페어", "과학전람회"])

if st.button("안내"):
    # API 키로 안내문 생성 시도
    competition_info = generate_science_competition_info(api_key, competition_name)

    # 결과 출력
    if competition_info is not None:
        st.markdown(to_markdown(competition_info))
    else:
        st.error("API 호출에 실패했습니다. 나중에 다시 시도해주세요.")
