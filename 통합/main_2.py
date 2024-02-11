# threading, concurrent.futrues 두 개 다 사용

import threading
import time
from concurrent.futures import ThreadPoolExecutor
from scan import *

def run_scan(task,metadata, host, results, lock):
    try:
        result = task(host)
        with lock:
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
    
    