import pickle
import time
from selenium import webdriver
from cryptography.fernet import Fernet

driver = webdriver.Chrome()
driver.get("https://www.naver.com/")

print("⏳ 1분 안에 네이버 로그인을 직접 완료해 주세요!")
time.sleep(60)

# 1. 🔑 나만의 절대 열쇠(Key) 생성
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# 2. 쿠키 데이터를 가져와서 바이트(Byte) 형태로 변환
cookies = driver.get_cookies()
raw_cookie_data = pickle.dumps(cookies)

# 3. 🔒 열쇠를 이용해 쿠키 데이터를 암호화 (잠그기!)
encrypted_cookie_data = cipher_suite.encrypt(raw_cookie_data)

# 4. 암호화된 데이터를 파일로 저장
with open("naver_cookies.enc", "wb") as f:
    f.write(encrypted_cookie_data)

print("✅ 쿠키 암호화 저장 완료! (해커가 훔쳐가도 절대 못 풉니다)")
print("\n🚨 [매우 중요] 아래 열쇠를 복사해서 .env 파일에 넣으세요 🚨")
print(f"COOKIE_KEY={key.decode()}")

driver.quit()
