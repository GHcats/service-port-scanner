from pysnmp.carrier.asyncore.dispatch import AsyncoreDispatcher
from pysnmp.carrier.asyncore.dgram import udp
from pysnmp.entity import engine, config
from pysnmp.proto import api

# SNMP 엔진 초기화
snmp_engine = engine.SnmpEngine()

# 로컬 주소에서 트랩 리스너 시작
config.addTransport(
    snmp_engine,
    udp.domainName,
    udp.UdpTransport().openServerMode(('0.0.0.0', 162))
)

# SNMPv1/2c/3 사용 설정
config.addV1System(snmp_engine, 'my-area', 'public')

# 트랩 콜백 함수 정의
def trap_callback(snmp_engine, state_reference, context_engine_id, context_name, var_binds, cb_ctx):
    print("트랩 수신:")
    for name, val in var_binds:
        print(f"{name.prettyPrint()} = {val.prettyPrint()}")

# 트랩 콜백 함수 등록
snmp_engine.registerTransportDispatcher(AsyncoreDispatcher())
snmp_engine.transportDispatcher.jobStarted(1)  # 작업 시작 표시

try:
    print("SNMP 트랩 리스너 시작...")
    snmp_engine.transportDispatcher.runDispatcher()
except:
    snmp_engine.transportDispatcher.closeDispatcher()
    raise
