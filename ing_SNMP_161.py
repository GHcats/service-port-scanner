from pysnmp.hlapi import *

# SNMP 에이전트 및 포트 설정
target = '192.168.0.3'  # 에이전트의 주소
port = 161  # SNMP 포트 (기본값은 161)

# SNMP 커뮤니티 문자열 (공동체 문자열) 설정
community = 'public'  # 공동체 문자열 (일반적으로 'public' 사용)

# OID (Object Identifier) 설정 (예: 시스템 이름 가져오기)
oid = ObjectIdentity('SNMPv2-MIB', 'sysName', 0)

# SNMP 요청 생성
snmp_request = getCmd(
    SnmpEngine(),
    CommunityData(community),
    UdpTransportTarget((target, port), timeout=2, retries=1),  # 타임아웃 및 재시도 횟수 설정
    ContextData(),
    ObjectType(oid)
)

# SNMP 요청 전송 및 응답 받기
error_indication, error_status, error_index, var_binds = next(snmp_request)

# 에러 확인
if error_indication:
    print(f"에러: {error_indication}")
else:
    if error_status:
        print(f"에러 상태: {error_status}")
    else:
        for var_bind in var_binds:
            print(f"연결 성공! {var_bind[0].prettyPrint()} = {var_bind[1].prettyPrint()}")
