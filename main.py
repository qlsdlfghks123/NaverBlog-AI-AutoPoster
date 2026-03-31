import os
import time
import pyperclip
import pickle
from dotenv import load_dotenv
from cryptography.fernet import Fernet

# Gemini 관련
import google.generativeai as genai

# Selenium 관련
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
    print(f"Gemini가 '{topic}' 주제로 글을 작성 중입니다...")
    model = genai.GenerativeModel('gemini-2.5-flash')
    prompt = f"""
    너는 ''라는 블로그를 운영하는 친절하고 전문적인 투자 블로거야.
    오늘 작성할 포스팅 주제는 '{topic}'이야.
    
    아래의 규칙을 엄격하게 지켜서 작성해 줘:
    
    1. 🌟 첫 번째 줄에는 반드시 포스팅의 '제목'만 딱 한 줄로 작성할 것. (# 기호 쓰지 말 것)
    2. 두 번째 줄부터 본문을 시작할 것.
    3. 본문의 첫 문장은 무조건 "**입니다!"로 시작할 것.
    4. 어려운 용어는 초보자도 이해하기 쉽게 풀어서 설명할 것.
    5. 중간중간 적절한 이모지를 섞어줄 것. 
    6. 글의 마무리에는 추천 해시태그 8개를 '#태그' 형식으로 달아줄 것.

    쓰고싶은 프롬포트를 넣으시면 됩니다. 위에는 예시입니다.
    
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
    # 가볍고 빠른 기본 옵션만 사용합니다.
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument(
        "--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=chrome_options)

    # 1. 쿠키를 넣으려면 일단 네이버 도메인에 먼저 접속해 있어야 합니다.
    print("네이버 도메인 진입합니다.")
    driver.get("https://www.naver.com/")
    time.sleep(2)

    # 2.암호화된 쿠키를 불러옵니다.
    print("암호화된 로그인 쿠키를 불러옵니다.")
    try:
        # .env 파일에서 키를 가져옵니다.
        cookie_key = os.getenv("COOKIE_KEY")
        cipher_suite = Fernet(cookie_key.encode())

        # 암호화된 파일을 읽어옵니다
        with open("naver_cookies.enc", "rb") as f:
            encrypted_data = f.read()

        #암호를 풉니다. (복호화)
        decrypted_data = cipher_suite.decrypt(encrypted_data)

        # 풀려난 데이터를 파이썬이 읽을 수 있게 변환하여 쿠키로 굽습니다
        cookies = pickle.loads(decrypted_data)
        for cookie in cookies:
            driver.add_cookie(cookie)

    except Exception as e:
        print(f"쿠키 해독 실패. 열쇠가 없거나 파일이 손상되었습니다: {e}")
        return

    # 3. 쿠키를 넣고 로그인합니다.
    driver.refresh()
    time.sleep(2)

    print("블로그 에디터로 진입합니다.")

    # [A] 글쓰기 페이지 이동
    print("블로그 글쓰기 에디터로 진입합니다.")
    driver.get("https://blog.naver.com/bogoddobogo_?Redirect=Write&")
    time.sleep(5)

    # [B] iframe 전환 (네이버 에디터 필수 단계)
    driver.switch_to.frame("mainFrame")

    # 팝업 닫기 (있을 경우)
    try:
        driver.find_element(By.CLASS_NAME, "se-popup-button-cancel").click()
        time.sleep(1)
    except:
        pass

    # 팝업 닫기 후 에디터가 완전히 로딩될 때까지 넉넉히 기다립니다.
    time.sleep(3)

    # [C] 제목 입력
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

    # [D] 본문 입력
    print("본문을 입력합니다.")
    pyperclip.copy(content)
    time.sleep(0.5)  # 클립보드 갱신 대기 (필수)
    ActionChains(driver).key_down(Keys.CONTROL).send_keys(
        'v').key_up(Keys.CONTROL).perform()
    time.sleep(2)

    print("모든 내용 입력이 완료되었습니다. 검토 후 '발행'을 눌러주세요.")

    # 검토는 필수입니다. 프롬포트가 완벽하지 않는 한, AI가 작성한 글은 무조건 부자연스럽습니다.
    # 자연스럽게 글을 메꾸고, 글을 올려주세요.


# --- 메인 실행 흐름 ---
if __name__ == "__main__":
    # blog_topic = input("오늘의 블로그 주제를 입력하세요: ")

    # 1. 글 생성
    # final_title, final_content = generate_contents(blog_topic)

    # 2. 네이버 업로드
    # upload_to_naver(final_title, final_content)

    #test_title = "로그인 세션 유지 테스트용입니다."
    #test_content = "테스트용입니다."

    # 네이버 업로드 함수만 단독으로 바로 실행합니다.
    # print("네이버 로그인 및 에디터 진행 테스트입니다.")
    #upload_to_naver(test_title, test_content)
