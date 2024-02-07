# 멀티스레드에 사용되는 banner 코드
# 근데 왜 이렇게 오래 걸리지?
# 얘가 찐임

import imaplib
import base64
from pysnmp.hlapi import *
import socket
import time

def IMAP_conn(host, port, use_ssl=False):   
    #host = "outlook.office365.com"
    host = "imap.gmail.com"
    
    try:
        if use_ssl: #993 IMAPS
            imap_server = imaplib.IMAP4_SSL(host, port)
        else: #143 IMAP
            imap_server = imaplib.IMAP4(host, port)
        print(f"\nConnected to {'IMAPS' if use_ssl else 'IMAP'} server successfully.\n")
        
        # 배너정보 가져오기
        banner_info = imap_server.welcome
        print(f'배너정보: {banner_info}')
        
        # 디코딩 과정 원래 있었는데 생략

    except imaplib.IMAP4_SSL.error as ssl_error:
        print("SSL 오류:", ssl_error)
        return None

    except imaplib.IMAP4.error as imap_error:
        print("IMAP 오류:", imap_error)
        return None

    except Exception as e:
        print(f"{port}포트 \n예기치 않은 오류 발생\n{e}\n")
        return None
    finally:
        print(f"\n{'IMAPS' if use_ssl else 'IMAP'} 스캔 완료.\n")
        print("************************************")

def SNMP_conn(host):
    port = 161
    community = 'public'
    host = '127.0.0.1'

    # OID 객체 생성
    sysname_oid = ObjectIdentity('SNMPv2-MIB', 'sysName', 0) #시스템 이름
    sysdesc_oid = ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0) #시스템 설명 정보
    
    try: 
        #SNMPD 요청 생성 및 응답
        snmp_request = getCmd(
            SnmpEngine(),
            CommunityData(community),
            UdpTransportTarget((host, port), timeout=10, retries=1),
            ContextData(),
            ObjectType(sysname_oid),
            ObjectType(sysdesc_oid)
        )

        #요청에 대한 결과 추출
        error_indication, error_status, error_index, var_binds = next(snmp_request)
        
        if error_indication:
                print(f"에러: {error_indication}")
        elif error_status:
            print(f"에러 상태: {error_status}")
        else:
            for var_bind in var_binds:
                if sysname_oid.isPrefixOf(var_bind[0]):
                    print(f"시스템 이름: {var_bind[1].prettyPrint()}")
                elif sysdesc_oid.isPrefixOf(var_bind[0]):
                    print(f"시스템 설명: {var_bind[1].prettyPrint()}")
    except socket.timeout as timeout_error:
        print(f"연결 시간 초과: {timeout_error}")

    except socket.error as socket_error:
        print(f"소켓 오류: {socket_error}")

    except Exception as e:
        print("예기치 않은 오류 발생:", e)
    finally:
        print("SNMP 스캔 완료")

if __name__ == '__main__':
    host = '127.0.0.1'
    
    startTime = time.time()

    # IMAP 연결
    IMAP_conn(host, 143, use_ssl=False)
    
    # IMAPS 연결 (SSL 사용)
    IMAP_conn(host, 993, use_ssl=True)

    # SNMP 연결
    SNMP_conn(host)
    print('SNMP 스캔 완료')
    
    endTime = time.time()
    print("Executed Time:", (endTime - startTime))

    
    

