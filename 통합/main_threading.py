# threading모듈만 사용

import threading
import time
from scan import *

def run_scan(task, metadata, host, results, lock):
    try:
        result = task(host, metadata['port'])
        with lock:
            if isinstance(result, list):
                results.extend(result)
            else:
                results.append({'port': metadata['port'], 'result': result})
    except Exception as e:
        error_result = {'port': metadata['port'], 'status': 'error', 'error_message': str(e)}
        with lock:
            results.append(error_result)

def scan_all(host):
    scan_tasks = [
    (scan_ftp_ssh_port,{'port': 21}),
    (scan_ftp_ssh_port, {'port': 22}),
    (scan_telnet_port, {'port': 23}),
    (scan_smtp_ldap_port, {'port': 25}),
    (scan_dns_port, {'port': 53}),
    (scan_http_port, {'port': 80}),
    (scan_pop3_port, {'port': 110}),
    (scan_ntp_port, {'port': 123}),
    (scan_imap_port, {'port': 143}),
    (scan_snmp_port, {'port': 161}),
    (scan_smtp_ldap_port, {'port': 389}),
    (scan_ssl_port, {'port': 443}),
    (scan_smb_port, {'port': 445}),
    (scan_ssl_port, {'port': 465}),
    (scan_udp_port, {'port': 520}),
    (scan_smtp_ldap_port, {'port': 587}),
    (scan_ssl_port, {'port': 636}),
    (scan_vmware_soap_port, {'port': 902}),
    (scan_imap_port, {'port': 993}),
    (scan_mysql_port, {'port': 3306}),
    (scan_rdp_port, {'port': 3389})
]
    
    results = []
    lock = threading.Lock()
    threads = []

    # 각 스캔 작업에 대해 스레드 생성 및 시작
    for task, metadata in scan_tasks:
        thread = threading.Thread(target=run_scan, args=(task, metadata, host, results, lock))
        threads.append(thread)
        thread.start()

    # 모든 스레드의 완료를 기다림
    for thread in threads:
        thread.join()
        
    
    # 결과를 포트 번호에 따라 정렬
    filtered_results = [r for r in results if r is not None]
    sorted_results = sorted(filtered_results, key=lambda x: x['port'] if isinstance(x, dict) else x[0]['port'])
        
    # 정렬된 결과 출력   
    for result in sorted_results:
        if isinstance(result, dict):
            for key, value in result.items():
                print(f"{key}: {value}")
        print()


if __name__ == "__main__":
    host = '127.0.0.1'  # 스캔할 호스트 주소
    startTime = time.time()
    scan_all(host)
    endTime = time.time()
    print("Executed Time:", (endTime - startTime))
