import time
import socket
import threading

resultLock = threading.Semaphore(value=1)

#스레드 개수를 제어할 세마포어
maxConnection = 100
connection_lock = threading.BoundedSemaphore(value = maxConnection)

#결과를 저장하는 dict
port_result = {}

#TCP방식
def port_scan(host, port):
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


def main(host):
    for portNum in range(1024):
        connection_lock.acquire()
        
        #스레드 초기화
    t = threading.Thread(target=port_scan, args=(host, portNum))
    t.start()
    time.sleep(5)

    print(port_result)

    print("\n\n\n++++++++++ the result ++++++++++")
    print('portNum' + '\t' + 'banner')
    for p in sorted(port_result.keys()):
        print("{} \t {}".format(p, port_result[p][:20].strip()))
    
if __name__ == "__main__":
    host =  '127.0.0.1'
    
    startTime = time.time()
    main(host)
    
    endTime = time.time()
    
    print("Executed Time:", (endTime - startTime))