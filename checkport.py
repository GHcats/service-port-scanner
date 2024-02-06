import socket

def check_port(host, port):
    try:
        # 소켓 생성
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)  # 연결 시도 타임아웃을 설정 (1초로 설정)

        # 호스트와 포트로 연결 시도
        s.connect((host, port))

        # 연결이 성공하면 포트가 열려 있다고 판단
        print(f"Port {port} is open on {host}")
    except (socket.timeout, ConnectionRefusedError):
        # 연결 시도가 실패하면 포트가 닫혀 있다고 판단
        print(f"Port {port} is closed on {host}")
    finally:
        # 소켓 닫기
        s.close()

# 호스트와 포트를 지정하여 호출
host = "outlook.office365.com"  # 연결 확인할 호스트 IP 주소
port = 145 # 확인할 포트 번호
check_port(host, port)
