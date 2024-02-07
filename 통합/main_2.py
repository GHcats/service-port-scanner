# threading 구현 도전중
# concurrent.futrues만 사용할 떄랑 크게 시간 차이 안 남

import threading
import time
from concurrent.futures import ThreadPoolExecutor
from scan import port123_ntp, port445_smb, port902_vmware_soap, port3306_mysql, IMAP_conn, SNMP_conn, IMAPS_conn

def run_scan(task,metadata, host, results, lock):
    try:
        result = task(host)
        with lock:
            # port902_vmware_soap 함수의 결과가 리스트인 경우 처리
            if isinstance(result, list):
                results.extend(result)
            else:
                results.append(result)
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

    with ThreadPoolExecutor(max_workers=len(scan_tasks)) as executor:
        futures = [executor.submit(run_scan, task,metadata, host, results, lock) for task, metadata in scan_tasks]

    [f.result() for f in futures]
    sorted_results = sorted(results, key=lambda x: x['port'])
    print("***결과출력***")
    for result in sorted_results:
        print(result)

if __name__ == "__main__":
    host = '127.0.0.1' #'pool.ntp.org' #'127.0.0.1'
    
    startTime = time.time()
    
    scan_all(host)
    endTime = time.time()
    
    print("Executed Time:", (endTime - startTime))
    
    