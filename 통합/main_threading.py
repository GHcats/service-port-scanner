# threading모듈만 사용

import threading
import time
from scan import port123_ntp, port445_smb, port902_vmware_soap, port3306_mysql, IMAP_conn, SNMP_conn, IMAPS_conn

def run_scan(task, metadata, host, results, lock):
    try:
        result = task(host)
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
        (port123_ntp, {'port': 123}),
        (port445_smb, {'port': 445}),
        (port902_vmware_soap, {'port': 902}),  # port902_vmware_soap 수정으로 인해 이제 902 포트만 스캔
        (port3306_mysql, {'port': 3306}),
        (IMAP_conn, {'port': 143}),
        (IMAPS_conn, {'port': 993}),
        (SNMP_conn, {'port': 161})
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

    # 결과 출력
    sorted_results = sorted(results, key=lambda x: x['port'])
    print("***결과출력***")
    for result in sorted_results:
        print(result)

if __name__ == "__main__":
    host = '127.0.0.1'  # 스캔할 호스트 주소
    startTime = time.time()
    scan_all(host)
    endTime = time.time()
    print("Executed Time:", (endTime - startTime))
