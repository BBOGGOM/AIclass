import textwrap
import google.generativeai as genai
import streamlit as st

def to_markdown(text):
    text = text.replace('•', '*')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

api_key = "AIzaSyBL61qYRwNy2CBHxjy73AiRw8iD8MeAp80"

def try_generate_content(api_key, prompt):
    genai.configure(api_key=api_key)
   
    model = genai.GenerativeModel(
        model_name="gemini-1.0-pro",
        generation_config={
            "temperature": 0.9,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        },
        safety_settings=[
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        ]
    )
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"API 호출 실패: {e}")
        return None

st.title("유전 형질 판별기 🧬")

st.markdown(
    """
    유전 형질을 입력하면 그것이 우성 형질인지 열성 형질인지 알려주는 웹앱입니다.
    예시: 눈 색깔, 머리 색깔, 혈액형, 곱슬머리, 귀 모양, 왼손잡이, 코 모양
    """
)

example_traits = [
    "눈 색깔", "머리 색깔", "혈액형", "곱슬머리", "귀 모양", 
    "왼손잡이", "코 모양", "보조개", "주근깨", "치아 모양", 
    "쌍꺼풀", "귓볼 모양", "턱 모양", "피부 색깔", "체모 밀도",
    "알러지 반응", "혀말기", "안면형태", "손가락 길이", "발 모양"
]
trait = st.selectbox("유전 형질을 선택하세요 또는 직접 입력하세요:", example_traits + ["직접 입력"])

if trait == "직접 입력":
    trait = st.text_input("유전 형질을 입력하세요:")

if st.button("확인"):
    if trait:
        prompt = f"유전 형질 '{trait}'가 우성 형질인지 열성 형질인지 설명해주세요."
        result = try_generate_content(api_key, prompt)
        if result:
            st.markdown(to_markdown(result))
        else:
            st.error("정보를 가져오는 데 실패했습니다. 나중에 다시 시도해주세요.")
    else:
        st.warning("유전 형질을 입력하세요.")


st.markdown('제작자: BBOGGOM')