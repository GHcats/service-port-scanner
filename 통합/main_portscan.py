# 포트 오픈 여부 판단하도록 수정
# 3초 걸림
# 몇개 열렸는지 보여주고, 열려있는 포트의 배너정보를 출력함
# 지금은 모든 정보를 출력함

import concurrent.futures
import time
from scan import *

def scan_all(host):
    # 각 스캔 작업을 함수와 연관 메타데이터(포트 번호)와 함께 정의
    scan_tasks = [
        #운지님
        (port123_ntp, {'port': 123}),
        (port445_smb, {'port': 445}),
        (port902_vmware_soap, {'port': 902}),  # 902 포트만 스캔
        (port3306_mysql, {'port': 3306}),
        #승희
        (IMAP_conn, {'port': 143}),
        (IMAP_conn, {'port': 993}),
        #(IMAPS_conn, {'port': 993}),
        (SNMP_conn, {'port': 161}),
        #현모님
        (Telnet_scan, {'port': 23}),
        #(SMTP_scan, {'port': 25}),
        (DNS_scan, {'port': 53}),
        #영창님
        (scan_ftp_port, {'port': 21}),
        (scan_ssh_port, {'port': 22}),
        #동진님
        (scan_smtp_port, {'port': 25}),  # 25번 포트 
        (scan_smtp_port, {'port': 587}),  # 587번 포트 
        (udp_scan, {'port': 520}), #520번 포트 
        (scan_ldaps_port, {'port': 636}), #636번 포트 
        (scan_smtps_port, {'port': 465}),  # SMTPS 스캔 
        (scan_ldap_port, {'port': 389}),  # LDAP 스캔 
        #다솜님
        (port80_http, {'port': 80}),
        (pop3_banner_grabbing, {'port': 110})
    ]

    results = []  # 결과를 저장할 리스트
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # 각 스캔 작업에 대한 future 생성
        futures = []
        for task, metadata in scan_tasks:
            future = executor.submit(task, host, metadata['port'])
            futures.append((future, metadata))

        for future, metadata in futures:
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                # 예외 발생 시 오류 메시지에 올바른 포트 번호를 포함
                error_result = {'port': metadata['port'], 'status': 'error', 'error_message': str(e)}
                results.append(error_result)


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
    #'pool.ntp.org' #'127.0.0.1'
    host =  '127.0.0.1'
    
    startTime = time.time()
    
    scan_all(host)
    
    endTime = time.time()
    
    print("Executed Time:", (endTime - startTime))