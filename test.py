from pysnmp.hlapi import *
from pysnmp.carrier.asyncore.dispatch import AsyncoreDispatcher as TransportDispatcher
from pysnmp.carrier.asyncore.dgram import udp


def trap_handler(port):
    print(f"SNMP TRAP 수신 대기 중 (Port {port})...")

    transport_dispatcher = AsyncoreDispatcher()

    # SNMP TRAP 핸들러 등록
    transport_dispatcher.registerRecvCbFun(lambda *args: process_trap(*args))

    transport_dispatcher.registerTransport(
        udp.domainName, udp.UdpSocketTransport().openServerMode(('0.0.0.0', port))
    )

    transport_dispatcher.jobStarted(1)  # 데몬 모드로 전환

    try:
        transport_dispatcher.runDispatcher()
    except KeyboardInterrupt:
        transport_dispatcher.closeDispatcher()

def process_trap(snmp_engine, state_reference, context_engine_id, context_name, var_binds, cb_ctx):
    # SNMP TRAP을 처리하는 코드를 작성합니다.
    for var_bind in var_binds:
        print(f"SNMP TRAP 수신: {var_bind[0].prettyPrint()} = {var_bind[1].prettyPrint()}")

if __name__ == '__main__':
    # SNMP 포트 (기본값은 162)
    port = 162

    trap_handler(port)
