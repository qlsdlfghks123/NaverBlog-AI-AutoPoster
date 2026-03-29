import os
import time
import random
import pyperclip
from dotenv import load_dotenv

# Gemini
import google.generativeai as genai

# Selenium 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains

# 1. 환경 설정 및 로그인 정보 로드
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
user_id = os.getenv("NAVER_ID")

# 2. Gemini 글 생성 함수

def generate_contents(topic):
    print(f"🤖 Gemini가 '{topic}' 주제로 글을 작성 중입니다...")
    model = genai.GenerativeModel('gemini-2.5-flash')
    prompt = prompt = prompt = f"""
    너는 ''라는 블로그를 운영하는 친절하고 전문적인 블로거야.
    오늘 작성할 포스팅 주제는 '{topic}'이야.
    
    아래의 규칙을 엄격하게 지켜서 작성해 줘:
    1. 🌟 첫 번째 줄에는 반드시 포스팅의 '제목'만 딱 한 줄로 작성할 것. (# 기호 쓰지 말 것)
    2. 두 번째 줄부터 본문을 시작할 것.
    3. 본문의 첫 문장은 무조건 "안녕하세요, 블로거 이름입니다!"로 시작할 것.
    4. 어려운 용어는 초보자도 이해하기 쉽게 풀어서 설명할 것.
    5. 중간중간 적절한 이모지를 섞어줄 것.
    6. 글의 마무리에는 해시태그 5개를 '#태그' 형식으로 달아줄 것.
    """
    response = model.generate_content(prompt)
    full_text = response.text

    # 간단하게 제목과 본문 나누기 (첫 줄을 제목으로 가정)
    lines = full_text.split('\n')
    title = lines[0].replace('#', '').strip()
    content = '\n'.join(lines[1:]).strip()
    return title, content

# 3. 네이버 블로그 업로드 함수

def upload_to_naver(title, content):
    # 브라우저 실행 설정
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument(
        "--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=chrome_options)

    # [A] 일회용 번호 로그인 페이지 이동
    print("🌐 네이버 일회용 로그인 페이지로 이동합니다.")
    driver.get("https://nid.naver.com/nidlogin.login?mode=number")

    # [B] 사용자로부터 OTP 입력 받기
    while True:
        otp_num = input("📱 네이버 앱에서 생성된 '일회용 로그인 번호' 8자리를 입력하세요: ")

        # 입력창 찾기 및 기존 내용 지우기
        input_box = driver.find_element(By.ID, "disposable")
        input_box.clear()  # 이전에 잘못 입력한 번호가 남아있을 수 있으니 지워줍니다.
        input_box.send_keys(otp_num)

        # 로그인 버튼 클릭
        input_box.send_keys(Keys.ENTER)

        print("로그인 확인 중...")
        time.sleep(3)  # 결과가 나올 때까지 잠시 대기

        # 로그인 성공 여부 판별 (URL이 바뀌었는지 확인)
        if "nidlogin.login" not in driver.current_url:
            print("✅ 로그인 성공!")
            break  # 반복문을 빠져나가 다음 단계([C])로 이동합니다.
        else:
            print("❌ 번호가 틀렸거나 오류가 발생했습니다. 다시 입력해 주세요.")
            # 루프의 처음으로 돌아가 다시 input()을 띄웁니다.

    # [C] 글쓰기 페이지 이동
    print("📝 블로그 글쓰기 에디터로 진입합니다.")
    driver.get("https://blog.naver.com/bogoddobogo_?Redirect=Write&")
    time.sleep(7)

    # [D] iframe 전환 (네이버 에디터 필수 단계)
    driver.switch_to.frame("mainFrame")

    # 팝업 닫기 (있을 경우)
    try:
        driver.find_element(By.CLASS_NAME, "se-popup-button-cancel").click()
        time.sleep(1)
    except:
        pass

    # 팝업 닫기 후 에디터가 완전히 로딩될 때까지 넉넉히 기다립니다. (가장 중요!)
    time.sleep(5)

    # [E] 제목 입력
    print("✍️ 제목을 입력합니다.")
    title_area = driver.find_element(By.CLASS_NAME, "se-title-text")
    ActionChains(driver).move_to_element(title_area).click().perform()
    time.sleep(1)

    # 1. 제목 붙여넣기
    pyperclip.copy(title)
    time.sleep(0.5)  # 클립보드 갱신 대기 (필수)
    ActionChains(driver).key_down(Keys.CONTROL).send_keys(
        'v').key_up(Keys.CONTROL).perform()
    time.sleep(1)

    # 제목 위치(title_area)에서 마우스를 아래로 150px 내려서 하얀 빈 공간을 강제 클릭합니다.
    ActionChains(driver).move_to_element_with_offset(
        title_area, 0, 150).click().perform()
    time.sleep(1)  # 본문에 커서가 깜빡일 때까지 대기

    # [F] 본문 입력
    print("✍️ 본문을 입력합니다.")
    pyperclip.copy(content)
    time.sleep(0.5)  # 클립보드 갱신 대기 (필수)
    ActionChains(driver).key_down(Keys.CONTROL).send_keys(
        'v').key_up(Keys.CONTROL).perform()
    time.sleep(2)

    print("✅ 모든 내용 입력이 완료되었습니다! 검토 후 '발행'을 눌러주세요.")


# --- 메인 실행 흐름 ---
if __name__ == "__main__":
    blog_topic = input("오늘의 블로그 주제를 입력하세요: ")

    # 1. 글 생성
    final_title, final_content = generate_contents(blog_topic)

    # 2. 네이버 업로드
    upload_to_naver(final_title, final_content)
