#포트 여는 것부터 막힘

import xmlrpc.client

def check_rpc_connection(host, port):
    # RPC 서버의 주소 설정
    server_address = f"http://{host}:{port}"  # RPC 서버의 주소와 포트를 지정

    try:
        # RPC 클라이언트 생성
        client = xmlrpc.client.ServerProxy(server_address)

        # 원격 메서드 호출 (이 예제에서는 더미 메서드인 "ping"을 호출)
        response = client.ping()

        # 연결 및 호출 결과 확인
        if response == "pong":
            return True
        else:
            return False

    except Exception as e:
        # 오류 처리
        print(f"연결 오류: {e}")
        return False

# RPC 서버의 호스트와 포트 설정
rpc_host = "127.0.0.1"  # RPC 서버의 호스트를 적절히 변경
rpc_port = 135  # RPC 서버의 포트를 적절히 변경

# RPC 연결 확인
if check_rpc_connection(rpc_host, rpc_port):
    print(f"RPC 서버 ({rpc_host}:{rpc_port})와 연결 성공")
else:
    print(f"RPC 서버 ({rpc_host}:{rpc_port})와 연결 실패")

