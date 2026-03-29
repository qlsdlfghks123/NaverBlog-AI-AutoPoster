# 🤖 네이버 블로그 자동 포스팅 봇 (feat. Gemini AI)

Google의 생성형 AI 모델인 Gemini API와 Selenium을 활용하여, 특정 주제만 입력하면 네이버 블로그에 맞춤형 포스팅을 자동으로 작성해 주는 파이썬 자동화 프로그램입니다.

## ✨ 핵심 기능 (Key Features)

* **🧠 AI 기반 맞춤형 원고 생성 (Gemini API)**
  * 단순한 텍스트 생성이 아닌 **프롬프트 엔지니어링(Prompt Engineering)**을 적용했습니다.
  * '개미의 마이크로 투자자'라는 블로그 페르소나를 AI에 부여하여, 정해진 인사말, 이모지 활용, 해시태그 삽입 등 일관된 스타일의 포스팅을 생성합니다.
  * AI의 응답을 파싱하여 '제목'과 '본문' 데이터를 정확하게 분리합니다.

* **🛡️ 안전한 네이버 로그인 자동화 (Selenium)**
  * 캡차(CAPTCHA)나 봇 탐지를 우회하기 위해, 네이버 앱의 '일회용 로그인 번호(8자리)'를 콘솔에서 직접 입력받아 안전하게 세션을 획득합니다.
  * 이 과정은 어떻게 해야 봇 탐지를 우회할 수 있을지, 연구를 해봐야겠네요. 일회용 로그인 번호를 입력해야한다는 단점이 있어요.

* **🚀 스마트에디터 DOM 구조 우회 및 텍스트 삽입 (ActionChains & Pyperclip)**
  * 네이버 스마트에디터 ONE의 복잡한 레이어 구조와 자바스크립트 이벤트 가로채기(Event Trapping)를 우회하기 위한 특수 로직이 적용되었습니다.
  * `send_keys()`의 속도 이슈와 텍스트 꼬임 현상을 방지하기 위해 **클립보드 동기화(`pyperclip`)** 방식을 사용합니다.
  * HTML 태그를 직접 찾는 대신, 기준점에서 물리적인 픽셀만큼 이동하는 **오프셋 좌표 클릭(`move_to_element_with_offset`)** 기법을 도입하여 어떤 상황에서도 정확하게 본문 영역을 타겟팅합니다.

## 🛠️ 사용 기술 (Tech Stack)
* **Language:** Python 
* **Web Automation:** Selenium WebDriver, ActionChains
* **AI API:** Google Generative AI (gemini-2.5-flash)
* **Utils:** Pyperclip (클립보드 제어), python-dotenv (환경변수 관리)

## 💡 트러블슈팅 (Troubleshooting)
* **Issue:** 네이버 에디터 본문 영역 클릭 시 `ElementNotInteractableException` 발생 및 커서 이동 불가 현상.
* **Solution:** 에디터의 복잡한 래퍼(Wrapper) 태그를 무시하고, 제목 칸을 기준으로 마우스를 하강시켜 빈 여백을 강제 클릭하는 Offset 클릭 기법으로 해결.

## 🚀 향후 목표 (To-Do)
* [ ] 로컬 폴더의 이미지를 본문에 자동으로 첨부하는 기능 추가
* [ ] Python `schedule` 라이브러리를 활용한 매일 아침 시황 자동 포스팅 기능

지적할 부분이 있다면 지적해주세요. 저는 아직 AI를 이용한 코딩만 할 줄 아는 수준이라서, 미흡한 부분이 많다고 생각하네요.. 