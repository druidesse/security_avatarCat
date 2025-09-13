@echo off
echo 보안 모니터링 프로그램을 관리자 권한으로 실행합니다...
echo.

REM 관리자 권한 확인
net session >nul 2>&1
if %errorLevel% == 0 (
    echo 관리자 권한으로 실행 중입니다.
    echo.
    python security_monitor.py
) else (
    echo 관리자 권한이 필요합니다. UAC 창이 나타날 수 있습니다.
    echo.
    powershell -Command "Start-Process cmd -ArgumentList '/c cd /d \"%~dp0\" && python security_monitor.py' -Verb RunAs"
)

pause
