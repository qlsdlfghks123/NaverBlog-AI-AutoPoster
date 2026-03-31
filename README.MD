# 🤖 네이버 블로그 자동 포스팅 봇 (feat. Gemini AI)

Google의 생성형 AI 모델인 Gemini API와 Selenium을 활용하여, 특정 주제만 입력하면 네이버 블로그에 맞춤형 포스팅을 자동으로 작성해 주는 파이썬 자동화 프로그램입니다.

## ✨ 핵심 기능 (Key Features)

* **🧠 AI 기반 맞춤형 원고 생성 (Gemini API)**
  * 단순한 텍스트 생성이 아닌 **프롬프트 엔지니어링(Prompt Engineering)**을 적용했습니다.
  * AI의 응답을 파싱하여 '제목'과 '본문' 데이터를 정확하게 분리합니다.

* **🔒 [Update] 100% 무인 자동화 및 강력한 보안 로그인 (Cookie Injection & Fernet)**

  * 기존의 번거로운 '일회용 번호 수동 입력' 방식을 폐기하고, **쿠키 인젝션(Cookie Injection)** 기법을 도입하여 클릭 한 번으로 실행되는 완전한 무인 자동화를 구현했습니다.

  * **보안 강화:** 세션 하이재킹(Session Hijacking)을 방지하기 위해 `cryptography` 라이브러리를 도입했습니다. 네이버 로그인 쿠키를 `Fernet` 대칭키 알고리즘으로 암호화하여 로컬에 저장(`.enc`)하고, 실행 시 환경변수(`.env`)의 비밀 키로 복호화하여 안전하게 주입합니다.

* **🚀 스마트에디터 DOM 구조 우회 및 텍스트 삽입 (ActionChains & Pyperclip)**
  * 네이버 스마트에디터 ONE의 복잡한 레이어 구조와 자바스크립트 이벤트 가로채기(Event Trapping)를 우회하기 위한 특수 로직이 적용되었습니다.

  * `send_keys()`의 속도 이슈와 텍스트 꼬임 현상을 방지하기 위해 **클립보드 동기화(`pyperclip`)** 방식을 사용합니다.

  * HTML 태그를 직접 찾는 대신, 기준점에서 물리적인 픽셀만큼 이동하는 **오프셋 좌표 클릭(`move_to_element_with_offset`)** 기법을 도입하여 어떤 상황에서도 정확하게 본문 영역을 타겟팅합니다.

## 🛠️ 사용 기술 (Tech Stack)
* **Language:** Python 3.x
* **Web Automation:** Selenium WebDriver, ActionChains
* **AI API:** Google Generative AI (gemini-2.5-flash)
* **Security & Utils:** * `cryptography` (Fernet 대칭키 암호화)
  * `pickle` (쿠키 데이터 직렬화)
  * `pyperclip` (클립보드 제어)
  * `python-dotenv` (환경변수 및 암호화 키 관리)

## 💡 트러블슈팅 (Troubleshooting)

* **Issue 1:** 네이버 에디터 본문 영역 클릭 시 `ElementNotInteractableException` 발생 및 커서 이동 불가 현상.
  * **Solution:** 에디터의 복잡한 래퍼(Wrapper) 태그를 무시하고, 제목 칸을 기준으로 마우스를 하강시켜 빈 여백을 강제 클릭하는 Offset 클릭 기법으로 우회 해결.

* **Issue 2:** 크롬 유저 프로필(User Data) 직접 연동 시, 누적된 캐시와 확장 프로그램 로딩으로 인한 프로세스 무한 대기(Deadlock) 및 웹소켓 통신 단절 현상.
  * **Solution:** 무거운 프로필 폴더 전체를 연동하는 대신, 인증에 필요한 핵심 '세션 쿠키'만 추출하여 가벼운 깡통(Vanilla) 크롬 세션에 주입(Injection)하는 방식으로 아키텍처를 변경하여 속도와 안정성 확보.


# 개선점이 있다면 무엇을 개선해야 할지 알려주세요! 바이브코딩으로 작성했습니다.
