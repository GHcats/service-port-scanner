#SNMP Agent

from pysnmp.hlapi import *

def SNMP_conn(host, port):

    # SNMP 커뮤니티 문자열 (공동체 문자열) 설정
    community = 'public'  # 공동체 문자열 (일반적으로 'public' 사용)

    # OID (Object Identifier) 설정
    sysname_oid = ObjectIdentity('SNMPv2-MIB', 'sysName', 0)
    sysdesc_oid = ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)

    # SNMP 요청 생성
    snmp_request = getCmd(
        SnmpEngine(),
        CommunityData(community),
        UdpTransportTarget((host, port), timeout=30, retries=1),  # 타임아웃 및 재시도 횟수 설정
        ContextData(),
        ObjectType(sysname_oid),
        ObjectType(sysdesc_oid)
    )
    
    # SNMP 요청 전송 및 응답 받기
    error_indication, error_status, error_index, var_binds = next(snmp_request)
    
     # 에러 확인
    if error_indication:
        print(f"에러: {error_indication}")
    elif error_status:
        print(f"에러 상태: {error_status}")
    else:
        for var_bind in var_binds:
            if sysname_oid.isPrefixOf(var_bind[0]):
                print(f"시스템 이름: {var_bind[1].prettyPrint()}")
            elif sysdesc_oid.isPrefixOf(var_bind[0]):
                print(f"시스템 설명: {var_bind[1].prettyPrint()}")

if __name__=='__main__':    
    # SNMP 에이전트 및 포트 설정
    host = '127.0.0.1'  # 에이전트의 주소
    port = 161  # SNMP 포트 (기본값은 161)

    SNMP_conn(host, port)
