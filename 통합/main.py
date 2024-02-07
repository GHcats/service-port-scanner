# SNMP에서 아직 속도개선 필요
# 출력되는 내용들 수정 필요
# 테스트라서 일단은 scan의 모든 함수 직접 가져옴

import concurrent.futures
from scan import port123_ntp, port445_smb, port902_vmware_soap, port3306_mysql, IMAP_conn, SNMP_conn, IMAPS_conn

def scan_all(host):
    # 각 스캔 작업을 함수와 연관 메타데이터(포트 번호)와 함께 정의
    scan_tasks = [
        (port123_ntp, {'port': 123}),
        (port445_smb, {'port': 445}),
        (port902_vmware_soap, {'port': 902}),  # 902 포트만 스캔
        (port3306_mysql, {'port': 3306}),
        (IMAP_conn, {'port': 143}),
        (IMAPS_conn, {'port': 993}),
        (SNMP_conn, {'port': 161})
    ]

    results = []  # 결과를 저장할 리스트

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # 각 스캔 작업에 대한 future 생성
        future_to_port = {executor.submit(task[0], host): task[1] for task in scan_tasks}

        for future in concurrent.futures.as_completed(future_to_port):
            task_metadata = future_to_port[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                # 예외 발생 시 오류 메시지에 올바른 포트 번호를 포함
                error_result = {'port': task_metadata['port'], 'status': 'error', 'error_message': str(e)}
                results.append(error_result)

    # 결과를 포트 번호에 따라 정렬
    sorted_results = sorted(results, key=lambda x: x['port'] if isinstance(x, dict) else x[0]['port'])

    # 정렬된 결과 출력
    for result in sorted_results:
        print(result)

if __name__ == "__main__":
    host =  '127.0.0.1'#'pool.ntp.org' #'127.0.0.1'
    scan_all(host)