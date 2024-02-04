import nmb.NetBIOS as NetBIOS

# NetBIOS 세션을 만듭니다.
session = NetBIOS.NetBIOS()

# NetBIOS 서버의 이름 또는 IP 주소를 지정합니다.
server_name = "ServerName"

# 서버에 연결합니다.
try:
    server_ip = session.get_host_by_name(server_name)
    server_socket = session.session(host=server_ip, port=139)
    print("Connected to {} on port 139.".format(server_name))
    
    # 메시지를 보냅니다.
    message = b"Hello, NetBIOS!"
    server_socket.send(message)
    
    # 서버로부터 응답을 받습니다.
    response = server_socket.recv(1024)
    print("Received response:", response.decode("utf-8"))

except Exception as e:
    print("Error:", str(e))

finally:
    # 연결을 종료합니다.
    server_socket.close()
