#162포트는 SNMP TRAP메시지를 수신하고 처리하는 용도로 사용
#서비스 포트 구현에는 따로 필요가 없다고 함
#아직 미완성... 응답을 확인할 수 없음

from pysnmp.hlapi import *
import time

def check_snmp_service(host, port):
    community = 'public'  # SNMP 커뮤니티 문자열 설정
    timeout = 10  # SNMP 응답 대기 시간 (초)

    error_indication, error_status, error_index, var_binds = next(
        getCmd(SnmpEngine(),
               CommunityData(community),
               UdpTransportTarget((host, port), timeout=timeout),
               ContextData(),
               ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)))
    )

    if error_indication:
        print(f"에러: {error_indication}")
    elif error_status:
        print(f"에러 상태: {error_status}")
    else:
        print(f"Port {port} is open and SNMP service is responding on {host}")
        for var_bind in var_binds:
            print(f"SNMP 정보: {var_bind[0].prettyPrint()}, 값: {var_bind[1].prettyPrint()}")

if __name__ == '__main__':
    host = 'localhost'  # SNMP 서비스가 실행 중인 호스트 주소
    port = 162  # SNMP 포트 번호 (기본값은 162)

    check_snmp_service(host, port)
