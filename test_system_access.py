#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
테스트용 스크립트 - 시스템 필수 자원에 접근을 시도합니다.
이 스크립트는 보안 모니터링 프로그램의 동작을 테스트하기 위해 사용됩니다.
"""

import os
import time

def test_system_access():
    """시스템 필수 자원에 접근을 시도합니다."""
    print("시스템 필수 자원 접근 테스트를 시작합니다...")
    print("보안 모니터링 프로그램이 실행 중이라면 경고가 표시될 것입니다.")
    print()
    
    # 테스트할 시스템 경로들
    test_paths = [
        r"C:\Windows\System32\notepad.exe",
        r"C:\Windows\System32\calc.exe",
        r"C:\Windows\System32\drivers\etc\hosts",
        r"C:\Windows\System32\config\SAM"
    ]
    
    for i, path in enumerate(test_paths, 1):
        print(f"테스트 {i}: {path} 접근 시도")
        try:
            # 파일 존재 여부 확인
            if os.path.exists(path):
                print(f"  - 파일이 존재합니다: {path}")
                
                # 읽기 권한 확인
                try:
                    with open(path, 'rb') as f:
                        f.read(1)  # 1바이트만 읽기
                    print(f"  - 읽기 권한이 있습니다.")
                except PermissionError:
                    print(f"  - 읽기 권한이 없습니다.")
                except Exception as e:
                    print(f"  - 읽기 중 오류: {e}")
            else:
                print(f"  - 파일이 존재하지 않습니다.")
                
        except Exception as e:
            print(f"  - 오류 발생: {e}")
        
        print()
        time.sleep(2)  # 2초 대기
    
    print("테스트 완료!")

if __name__ == "__main__":
    print("=" * 60)
    print("보안 모니터링 프로그램 테스트 스크립트")
    print("=" * 60)
    print()
    print("주의: 이 스크립트는 보안 모니터링 프로그램의 동작을 테스트하기 위한 것입니다.")
    print("보안 모니터링 프로그램이 실행 중일 때만 의미가 있습니다.")
    print()
    
    input("엔터를 눌러 테스트를 시작하세요...")
    print()
    
    test_system_access()
    
    input("\n엔터를 눌러 종료하세요...")
