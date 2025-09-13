#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
보안 모니터링 프로그램
새로운 프로세스가 시작되고 시스템 필수 자원을 편집하려 할 때 알림을 표시합니다.
"""

import psutil
import win32gui
import win32con
import win32process
import win32api
import win32security
import ctypes
from ctypes import wintypes
import threading
import time
import tkinter as tk
from tkinter import messagebox
import sys
import os
from datetime import datetime
import logging

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('security_monitor.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class SecurityMonitor:
    def __init__(self):
        self.running = True
        self.monitored_processes = {}  # pid: process_info
        self.suspicious_processes = {}  # pid: process_info
        self.system_critical_paths = [
            r"C:\Windows\System32",
            r"C:\Windows\SysWOW64", 
            r"C:\Windows\WinSxS",
            r"C:\Program Files\Windows Defender",
            r"C:\Program Files (x86)\Windows Defender",
            r"C:\Windows\System32\drivers",
            r"C:\Windows\System32\config",
            r"C:\Windows\System32\catroot",
            r"C:\Windows\System32\catroot2"
        ]
        
        # 윈도우 API 상수
        self.PROCESS_TERMINATE = 0x0001
        self.PROCESS_SUSPEND_RESUME = 0x0800
        self.STATUS_SUCCESS = 0x00000000
        
    def is_system_critical_path(self, file_path):
        """파일 경로가 시스템 필수 경로인지 확인"""
        if not file_path:
            return False
            
        file_path = file_path.lower()
        for critical_path in self.system_critical_paths:
            if file_path.startswith(critical_path.lower()):
                return True
        return False
    
    def get_process_file_path(self, pid):
        """프로세스의 실행 파일 경로를 가져옵니다"""
        try:
            process = psutil.Process(pid)
            return process.exe()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            return None
    
    def monitor_new_processes(self):
        """새로운 프로세스 모니터링"""
        current_processes = set()
        
        while self.running:
            try:
                # 현재 실행 중인 프로세스 목록 가져오기
                new_processes = set()
                for proc in psutil.process_iter(['pid', 'name', 'create_time']):
                    try:
                        pid = proc.info['pid']
                        new_processes.add(pid)
                        
                        # 새로운 프로세스인지 확인
                        if pid not in current_processes and pid not in self.monitored_processes:
                            process_info = {
                                'pid': pid,
                                'name': proc.info['name'],
                                'create_time': proc.info['create_time'],
                                'file_path': self.get_process_file_path(pid),
                                'start_time': time.time()
                            }
                            
                            self.monitored_processes[pid] = process_info
                            logging.info(f"새로운 프로세스 감지: {proc.info['name']} (PID: {pid})")
                            
                            # 시스템 필수 자원 접근 여부 확인
                            if self.check_system_resource_access(pid):
                                self.handle_suspicious_process(process_info)
                
                current_processes = new_processes
                
                # 종료된 프로세스 정리
                for pid in list(self.monitored_processes.keys()):
                    if pid not in new_processes:
                        del self.monitored_processes[pid]
                        if pid in self.suspicious_processes:
                            del self.suspicious_processes[pid]
                
                time.sleep(1)  # 1초마다 체크
                
            except Exception as e:
                logging.error(f"프로세스 모니터링 중 오류: {e}")
                time.sleep(5)
    
    def check_system_resource_access(self, pid):
        """프로세스가 시스템 필수 자원에 접근하는지 확인"""
        try:
            process = psutil.Process(pid)
            
            # 열린 파일 핸들 확인
            try:
                open_files = process.open_files()
                for file_info in open_files:
                    if self.is_system_critical_path(file_info.path):
                        logging.warning(f"프로세스 {pid}가 시스템 필수 파일에 접근: {file_info.path}")
                        return True
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                pass
            
            # 메모리 맵 확인
            try:
                memory_maps = process.memory_maps()
                for mmap in memory_maps:
                    if self.is_system_critical_path(mmap.path):
                        logging.warning(f"프로세스 {pid}가 시스템 필수 메모리 맵에 접근: {mmap.path}")
                        return True
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                pass
                
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
            
        return False
    
    def suspend_process(self, pid):
        """프로세스 일시중지"""
        try:
            # 프로세스 핸들 열기
            handle = win32api.OpenProcess(
                win32con.PROCESS_SUSPEND_RESUME, 
                False, 
                pid
            )
            
            # 프로세스 일시중지
            result = ctypes.windll.ntdll.NtSuspendProcess(handle)
            win32api.CloseHandle(handle)
            
            if result == self.STATUS_SUCCESS:
                logging.info(f"프로세스 {pid} 일시중지 성공")
                return True
            else:
                logging.error(f"프로세스 {pid} 일시중지 실패: {result}")
                return False
                
        except Exception as e:
            logging.error(f"프로세스 {pid} 일시중지 중 오류: {e}")
            return False
    
    def resume_process(self, pid):
        """프로세스 재개"""
        try:
            # 프로세스 핸들 열기
            handle = win32api.OpenProcess(
                win32con.PROCESS_SUSPEND_RESUME, 
                False, 
                pid
            )
            
            # 프로세스 재개
            result = ctypes.windll.ntdll.NtResumeProcess(handle)
            win32api.CloseHandle(handle)
            
            if result == self.STATUS_SUCCESS:
                logging.info(f"프로세스 {pid} 재개 성공")
                return True
            else:
                logging.error(f"프로세스 {pid} 재개 실패: {result}")
                return False
                
        except Exception as e:
            logging.error(f"프로세스 {pid} 재개 중 오류: {e}")
            return False
    
    def terminate_process(self, pid):
        """프로세스 종료"""
        try:
            process = psutil.Process(pid)
            process.terminate()
            logging.info(f"프로세스 {pid} 종료 성공")
            return True
        except Exception as e:
            logging.error(f"프로세스 {pid} 종료 중 오류: {e}")
            return False
    
    def show_security_alert(self, process_info):
        """보안 경고 알림 표시"""
        def show_alert():
            root = tk.Tk()
            root.withdraw()  # 메인 윈도우 숨기기
            
            # 항상 최상위에 표시
            root.attributes('-topmost', True)
            root.lift()
            root.focus_force()
            
            message = f"""
보안 경고!

프로세스: {process_info['name']}
PID: {process_info['pid']}
파일 경로: {process_info.get('file_path', '알 수 없음')}

해당 작업은 윈도우의 필수요소를 건드린다냥!!
그래도 이거 진짜로 할 거냥??
            """
            
            result = messagebox.askyesno("보안 경고", message, icon='warning')
            
            if result:  # 예를 선택한 경우
                if self.resume_process(process_info['pid']):
                    logging.info(f"사용자가 프로세스 {process_info['pid']} 실행 허용")
                else:
                    logging.error(f"프로세스 {process_info['pid']} 재개 실패")
            else:  # 아니오를 선택한 경우
                if self.terminate_process(process_info['pid']):
                    logging.info(f"사용자가 프로세스 {process_info['pid']} 실행 거부 - 프로세스 종료")
                else:
                    logging.error(f"프로세스 {process_info['pid']} 종료 실패")
            
            # 모니터링 목록에서 제거
            if process_info['pid'] in self.suspicious_processes:
                del self.suspicious_processes[process_info['pid']]
            
            root.destroy()
        
        # 별도 스레드에서 GUI 실행
        alert_thread = threading.Thread(target=show_alert)
        alert_thread.daemon = True
        alert_thread.start()
    
    def handle_suspicious_process(self, process_info):
        """의심스러운 프로세스 처리"""
        pid = process_info['pid']
        
        # 이미 처리 중인 프로세스는 무시
        if pid in self.suspicious_processes:
            return
        
        self.suspicious_processes[pid] = process_info
        
        # 프로세스 일시중지
        if self.suspend_process(pid):
            logging.warning(f"의심스러운 프로세스 {pid} 일시중지됨")
            # 알림 표시
            self.show_security_alert(process_info)
        else:
            logging.error(f"프로세스 {pid} 일시중지 실패")
            # 일시중지 실패 시 모니터링 목록에서 제거
            if pid in self.suspicious_processes:
                del self.suspicious_processes[pid]
    
    def start_monitoring(self):
        """모니터링 시작"""
        logging.info("보안 모니터링 시작")
        
        # 관리자 권한 확인
        if not self.is_admin():
            logging.error("관리자 권한이 필요합니다.")
            return False
        
        # 프로세스 모니터링 스레드 시작
        monitor_thread = threading.Thread(target=self.monitor_new_processes)
        monitor_thread.daemon = True
        monitor_thread.start()
        
        return True
    
    def is_admin(self):
        """관리자 권한 확인"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    def stop_monitoring(self):
        """모니터링 중지"""
        self.running = False
        logging.info("보안 모니터링 중지")

def main():
    """메인 함수"""
    print("보안 모니터링 프로그램을 시작합니다...")
    
    # 관리자 권한 확인
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print("이 프로그램은 관리자 권한으로 실행되어야 합니다.")
        print("관리자 권한으로 다시 실행해주세요.")
        input("엔터를 눌러 종료...")
        return
    
    monitor = SecurityMonitor()
    
    try:
        if monitor.start_monitoring():
            print("보안 모니터링이 시작되었습니다.")
            print("프로그램을 종료하려면 Ctrl+C를 누르세요.")
            
            # 메인 스레드에서 대기
            while monitor.running:
                time.sleep(1)
                
    except KeyboardInterrupt:
        print("\n프로그램을 종료합니다...")
        monitor.stop_monitoring()
    except Exception as e:
        logging.error(f"프로그램 실행 중 오류: {e}")
        print(f"오류가 발생했습니다: {e}")

if __name__ == "__main__":
    main()
