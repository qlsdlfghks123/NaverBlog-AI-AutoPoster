import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
# 1. 인증된 API 키 설정
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

# 2. AI 모델 선택
model = genai.GenerativeModel('gemini-2.5-flash')


def generate_blog_post(user_topic):
    # 3. 블로그 맞춤형 프롬프트
    prompt = f"""
    너는 '개미의 마이크로 투자'라는 블로그를 운영하는 10년차 전문 투자자야.
    주제: {user_topic}
    
    위 주제로 네이버 블로그 포스팅을 작성해줘.
    - 제목은 클릭하고 싶게 매력적으로 지어줘.
    - 사회초년생도 이해하기 쉽게 친절한 말투로 써줘.
    - 소제목을 나누고 가독성 좋게 이모지도 섞어줘.
    - 마지막엔 해시태그 5개를 달아줘.
    """

    response = model.generate_content(prompt)
    return response.text


# 4. 실행 및 결과 출력
user_topic = input("오늘 블로그에 쓸 주제를 입력하세요: ")
result = generate_blog_post(user_topic)

print("\n" + "="*50)
print(result)
print("="*50)
