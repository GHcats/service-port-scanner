import threading, time, random, socket

#전역변수
resultLock = threading.Semaphore(value=1)

#스레드 개수를 제어할 세마포어
maxConnection = 100
connection_lock = threading.BoundedSemaphore(value = maxConnection)

#결과를 저장하는 dict
port_result = {}

#메인함수
def main():
    tgtHost = ""

    for portNum in range(1024):
        #도어락 설정
        connection_lock.acquire()
        
        #스레드 초기화
        t = threading.Thread(target=scanPort, args=(tgtHost, portNum))
        t.start()
    time.sleep(5)

    print(port_result)

    with open("portScanResult.csv","w") as f:
        f.write("portNum, banner\n")
        for p in sorted(port_result.keys()):
            f.write("{}, {}".format(p, port_result[p]))

    print("\n\n\n++++++++++ the result ++++++++++")
    print('portNum' + '\t' + 'banner')
    for p in sorted(port_result.keys()):
        print("{} \t {}".format(p, port_result[p][:20].strip()))
    print(">> the result in portScanResult.csv")

def scanPort(tgtHost, portNum):
    try:
        with socket.socket() as s:
            data = None

            s.settimeout(2)
            s.connect((tgtHost, portNum))
            s.send("Python Connect\n".encode())

    except Exception as e:
        if str(e) == "time out":
            data = str(e)
        else:
            data = 'error'
    finally:
        if data is None:
            data = "no_data"
        elif data == 'error':
            connection_lock.release()
            return
        resultLock.acquire()
        print("[+] Port {} opened: {}".format(portNum, data[:20]).strip())
        resultLock.release()
        port_result[portNum]=data
        connection_lock.release()
        

if __name__ == '__main__':
    startTime = time.time()
    main()
    endTime = time.time()
    print("exceuted Time:", (endTime-startTime))