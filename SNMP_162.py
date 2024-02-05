# callback 함수 typeError missing 2 required positional arguments: 'var_binds' and 'cb_ctx'
# 혹시나해서 None이라고 설정해주니까 됨. 연결확인만 하면 되는 거니까 괜찮지 않을까...

# 무한 수신 대기중 수정하기

from pysnmp.hlapi import *
from pysnmp.carrier.asyncore.dispatch import AsyncoreDispatcher as TransportDispatcher
from pysnmp.carrier.asyncore.dgram import udp

# callback 함수를 SNMP_TRAP_receiver 함수 외부에 정의합니다.
def callback(snmpEngine, stateReference, contextEngineID, contextName, varBinds=None, cbCtx=None):
    try:
        print('SNMP TRAP 받음:', varBinds)
    except Exception as e:
        print('콜백 함수 인자 처리 중 오류:', e)
        print('SNMP 트랩 메시지가 수신되었지만 오류가 발생')
    
def SNMP_TRAP_receiver(config, port):
        
    # SNMP TRAP 리스너 시작
    print(f"SNMP TRAP 수신 대기 중 (Port {port})...")

    # SNMP TRAP을 수신하고 처리하는 루프
    transportDispatcher = TransportDispatcher()

    transportDispatcher.registerRecvCbFun(callback)
        

    # SNMP 트랩 수신을 위한 트랜스포트 설정
    transportDispatcher.registerTransport(
        udp.domainName, udp.UdpTransport().openServerMode(('0.0.0.0', port))
    )

    snmp_engine = SnmpEngine()
    transportDispatcher.jobStarted(1)  # jobStarted에 전달된 1은 임의의 숫자입니다.

    try:
        # 비동기적으로 SNMP 트랩 메시지를 수신
        transportDispatcher.runDispatcher()
    except Exception as ex:
        print('SNMP 트랩 수신 중 오류 발생:', ex)
    finally:
        # 청소 작업
        transportDispatcher.closeDispatcher()
        snmp_engine.transportDispatcher = None

if __name__ == '__main__':
    # SNMP 포트 (기본값은 162)
    port = 162
    host = ''

    # SNMP TRAP 수신을 위한 SNMP 포트 설정
    config = UdpTransportTarget((host, port))
    
    SNMP_TRAP_receiver(config, port)
