from pysnmp.hlapi import *

def SNMP_TRAP_receiver(config, port):

    # SNMP 엔진 설정
    snmp_engine = SnmpEngine()

    # SNMP TRAP 리스너 시작
    #원래는 trap을 이용해야 하는데 recvNotification이 없음
    # snmp_context = ContextData()
    # snmp_trap_listener = next(
    #     recvNotification(  # 이 부분을 recvNotification 함수로 변경
    #         snmp_engine,
    #         CommunityData('public'),  # 커뮤니티 문자열 설정 (실제 환경에서 보안을 고려해야 합니다)
    #         config,
    #         snmp_context
    #     )
    # )
    
    print(f"SNMP TRAP 수신 대기 중 (Port {port})...")
    
    # SNMP TRAP을 수신하고 처리하는 루프
    for (error_indication, error_status, error_index, var_binds) in next(
        getCmd(
            snmp_engine,
            CommunityData('public'),  # 커뮤니티 문자열 설정 (실제 환경에서 보안을 고려해야 합니다)
            config,
            ContextData(),
            ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)),
        )
    )
        # if error_indication:
        #     print(f"에러: {error_indication}")
        # else:
        #     if error_status:
        #         print(f"에러 상태: {error_status}")
        #     else:
        #         for var_bind in var_binds:
        #             print(f"SNMP TRAP 수신: {var_bind[0].prettyPrint()} = {var_bind[1].prettyPrint()}")
    while True:
        try:
            for (error_indication, error_status, error_index, var_binds) in next(...):
                # SNMP 트랩을 처리하는 기존의 코드
                pass
        except RequestTimedOut:
            # 타임아웃을 처리합니다. 에러 로깅이나 요청 재시도 등
            print("SNMP 요청이 타임아웃 되었습니다.")
        except StopIteration:
            # 이터레이터의 끝을 처리, 해당되는 경우
            break

        
if __name__ == '__main__':
    # SNMP 포트 (기본값은 162)
    port = 162

    # SNMP TRAP 수신을 위한 SNMP 포트 설정
    config = UdpTransportTarget(('192.168.0.35', port))
    
    SNMP_TRAP_receiver(config, port)
   