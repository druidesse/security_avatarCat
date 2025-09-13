이 프로그램은 cursor.ai를 이용해서 작성되었습니다. 비 개발자라 코드 이슈나 수정 사항이 발생할 수 있고, 혹은 컴퓨터에 문제가 생길 수 있습니다. 바이브 코딩의 위험성은 잘 알려져 있습니다. 저는 이 문제를 책임질 수 없으며, 이 레포지토리는 사이버대학 학부생 수준에서 간단하게 AI를 사용하여 작성되었습니다.

This program uses cursor.ai to simply shut down the Linux OS and computer instead of restarting it in the event of a security issue on Linux.
As a non-developer, you may encounter code issues or modifications, or your computer may malfunction. The risks of Vibe coding are well known.
I cannot be held responsible for this issue, and this repository was created using simple AI at the undergraduate level of a cyber university.

참고로 약간의 위트를 위해 중요한 알림이 뜨는 부분에서는 프로그램이 냥체를 쓰고 있습니다.

For your information, the program uses cat's words in the parts where important notifications appear, just for a bit of wit.

# 보안 모니터링 프로그램

윈도우 시스템에서 새로운 프로세스가 시작되고 시스템 필수 자원을 편집하려 할 때 보안 경고를 표시하는 프로그램입니다.

## 기능

- 새로운 프로세스 시작 감지
- 시스템 필수 자원 접근 감지
- 의심스러운 프로세스 자동 일시중지
- 사용자에게 보안 경고 알림 표시
- 사용자 선택에 따른 프로세스 재개 또는 종료

## 시스템 요구사항

- Windows 운영체제
- Python 3.7 이상
- 관리자 권한

## 설치 방법

1. 필요한 패키지 설치:
```bash
pip install -r requirements.txt
```

2. 관리자 권한으로 프로그램 실행:
```bash
python security_monitor.py
```

## 사용 방법

1. 프로그램을 관리자 권한으로 실행합니다.
2. 프로그램이 백그라운드에서 실행되며 새로운 프로세스를 모니터링합니다.
3. 의심스러운 프로세스가 감지되면 자동으로 일시중지되고 보안 경고가 표시됩니다.
4. 사용자가 "예"를 선택하면 프로세스가 재개되고, "아니오"를 선택하면 프로세스가 종료됩니다.

## 모니터링 대상 경로

다음 경로들에 대한 접근을 모니터링합니다:
- C:\Windows\System32
- C:\Windows\SysWOW64
- C:\Windows\WinSxS
- C:\Program Files\Windows Defender
- C:\Program Files (x86)\Windows Defender
- C:\Windows\System32\drivers
- C:\Windows\System32\config
- C:\Windows\System32\catroot
- C:\Windows\System32\catroot2

## 로그

프로그램 실행 중 모든 활동은 `security_monitor.log` 파일에 기록됩니다.

## 주의사항

- 이 프로그램은 관리자 권한이 필요합니다.
- 시스템의 중요한 프로세스도 모니터링 대상이 될 수 있으므로 주의가 필요합니다.
- 프로그램을 종료하려면 Ctrl+C를 누르세요.

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.
