# 현모님, 운지님, 영창님, 동진님, 최승희 통합
# 포트 오픈 여부 판별하도록 수정

# 스캔 부분은 일단 통합 먼저 하고 정리하자
# servicename + tcp, udp도 출력하도록 수정하기
# IMAP, IMAPS, LDAP, LDAPS 코드 합칠 수 있으면 합치기
# 동진님 파트 출력 기준이 애매해서 다시 한번 확인하기

import socket
import struct
import time
import uuid
import imaplib
import telnetlib
import ssl
from pysnmp.hlapi import *
from smbprotocol.connection import Connection
from scapy.all import sr, IP, TCP, UDP, ICMP, sr1


# 현모님이 구현한 방식
def SYN_scan(host, port):
    try:
        # 소켓 생성
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)  # 타임아웃 설정

        # SYN 패킷 전송
        result = sock.connect_ex((host, port))

        # 결과 확인
        if result == 0:
            return True  # 포트가 열려있음
        else:
            return False  # 포트가 닫혀있음
        
    except Exception as e:
        return None  # 예외 발생 시 None 반환
    finally:
        sock.close()

# 동진님이 구현한 방식
def syn_scan(ip, port):
    packet = IP(dst=ip)/TCP(dport=port, flags="S")
    # sr 함수는 (발송된 패킷, 받은 응답) 튜플의 리스트를 반환
    # 여기서는 받은 응답만 필요하므로, _ 를 사용해 발송된 패킷 부분을 무시
    ans, _ = sr(packet, timeout=2, verbose=0)  # ans는 받은 응답 리스트
    for sent, received in ans:
        if received and received.haslayer(TCP):
            if received[TCP].flags & 0x12:  # SYN-ACK 확인
                return True  # 포트열림
            elif received[TCP].flags & 0x14:  # RST-ACK 확인
                return False  # 포트 닫힘
    return False  # 응답없거나 다른에러

def udp_scan(host):
    port = 520
    response_data = {
        'port': port,
        'state': 'open or filterd'
    }
    packet = IP(dst=host)/UDP(dport=port)
    response = sr1(packet, timeout=2, verbose=0)
    
    if response is None:
        response_data['error_message'] = 'No response (possibly open or filtered).'
    elif response.haslayer(ICMP):
        if int(response.getlayer(ICMP).type) == 3 and int(response.getlayer(ICMP).code) == 3:
            response_data['state'] = 'closed'
        else:
            response_data['error_message'] = f"ICMP message received (type: {response.getlayer(ICMP).type}, code: {response.getlayer(ICMP).code})."
            #print(f"Port {port}: ICMP message received (type: {response.getlayer(ICMP).type}, code: {response.getlayer(ICMP).code}).")
    else:
        response_data['error_message'] = 'Received unexpected response.'
        #print(f"Port {port}: Received unexpected response.")


def scan_smtp_port(host):
    port = 25
    
    response_data = {
        'port': port,
        'state': 'closed'
    }
    
    if syn_scan(host, port):
        try:
            # SMTP 서버에 연결
            connection = socket.create_connection((host, port), timeout=10)
            # 서버로부터 응답 받기
            banner = connection.recv(1024).decode('utf-8')
            response_data['state'] = 'open'
            response_data['banner'] = banner
        except socket.error as err:
            response_data['state'] = 'open'
            response_data['error_message'] = 'error'
        finally:
            # 연결 종료
            if 'connection' in locals():
                connection.close()
    else:
        response_data['state'] = 'Closed or filtered.'
    
    return response_data


def scan_smtps_port(host):
    port = 587
    response_data = {
        'port': port,
        'state': 'closed'
    }
    
    if syn_scan(host, port):
        try:
            context = ssl.create_default_context()
            with socket.create_connection((ip, port)) as sock:
                with context.wrap_socket(sock, server_hostname=ip) as ssock:
                    banner = ssock.recv(1024).decode('utf-8')
                    response_data['state'] = open
                    response_data['banner'] = banner
        except Exception as err:
            response_data['state'] = 'error'
            response_data['error_message'] = str(err)
    else:
        response_data['state'] = 'Closed or filtered.'

def scan_ldap_port(host):
    port = 636
    response_data = {
        'port': port,
        'state': 'closed'
    }
    
    if syn_scan(host, port):
        try:
            connection = socket.create_connection((host, port), timeout=10)
            banner = connection.recv(1024).decode('utf-8')
            response_data['state'] = 'open'
            response_data['banner'] = banner
        except socket.error as err:
            response_data['state'] = 'error'
            response_data['error_message'] = str(err)
        finally:
            if 'connection' in locals():
                connection.close()
    else:
        response_data['state'] = 'Closed or filtered.'
    
    return response_data

def scan_ldaps_port(host):
    port = 389
    response_data = {
        'port': port,
        'state': 'closed'
    }

    if syn_scan(host, port):
        try:
            # SSL/TLS 연결을 위한 컨텍스트 생성
            context = ssl.create_default_context()
            # SMTP 서버에 SSL/TLS 연결
            with socket.create_connection((host, port)) as sock:
                with context.wrap_socket(sock, server_hostname=host) as ssock:
                    # 서버로부터 응답(배너) 받기
                    banner = ssock.recv(1024).decode('utf-8')
                    response_data['state'] = 'open'
                    response_data['banner'] = banner
        except Exception as err:
            response_data['state'] = 'error'
            response_data['error_message'] = str(err)
    else:
        response_data['state'] = 'Closed or filtered.'
    
    return response_data

def Telnet_scan(host):
    port = 23
    service_name = "Telnet"
    
    response_data = {
        'port': port,
        'state': 'closed'
    }
    
    try:
        tn = telnetlib.Telnet(host, port, timeout=5)  # Telnet 객체 생성 및 서버에 연결 (타임아웃 설정)
        banner = tn.read_until(b"\r\n", timeout=5).decode('utf-8').strip()  # 배너 정보 읽기
        tn.close()  # 연결 종료
        response_data['state'] = 'open'
        response_data['banner'] = banner
        #return {'port': port, 'status': 'open', 'service_name': service_name, 'banner': banner}
    except ConnectionRefusedError:
        response_data['error_message'] = '연결거부'
        #return {'port': port, 'status': 'closed', 'service_name': service_name, 'banner': None}  # 연결이 거부되었을 때
    except Exception as e:
        response_data['state'] = 'error'
        response_data['error_message'] = str(e)
        #return {'port': port, 'status': 'error', 'service_name': service_name, 'banner': None}  # 그 외 예외 발생 시
    return response_data

def SMTP_scan(host):
    port = 25
    service_name = "SMTP"
    response_data = {
        'port': port,
        'state': 'closed'
    }
    try:
        # 소켓 생성
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)  # 타임아웃 설정

        # SMTP 서버에 연결
        sock.connect((host, port))
        banner = sock.recv(1024).decode('utf-8').strip()  # 배너 정보 읽기
        sock.sendall(b"QUIT\r\n")  # QUIT 명령 전송
        sock.close()  # 연결 종료
        response_data['state'] = 'open'
        response_data['banner'] = 'banner'
        #return {'port': port, 'status': 'open', 'service_name': service_name, 'banner': banner}
    except Exception as e:
        response_data['state'] = 'error'
        response_data['error_message'] = str(e)
        #return {'port': port, 'status': 'error', 'service_name': service_name, 'banner': None}  # 예외 발생 시
    return response_data

def DNS_scan(host):
    port = 53
    response_data = {
        'port': port,
        'state': 'closed'
    }
    try:
        # UDP 소켓 생성
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(1)  # 타임아웃 설정

        # DNS 서버에 데이터 전송
        sock.sendto(b'', (host, port))

        # 데이터 수신 시 포트가 열려 있다고 가정
        # UDP 스캔은 응답이 없어도 포트가 열려 있다고 가정합니다.
        response_data['state'] = 'open'
        response_data['banner'] = 'None'
        #return {'port': port, 'status': 'open', 'service_name': 'DNS', 'banner': None}
    except Exception as e:
        response_data['error_message'] = str(e)
        #return {'port': port, 'status': 'closed', 'service_name': 'DNS', 'banner': None}
    finally:
        sock.close()
    return response_data


def port123_ntp(host, timeout=1):
    port = 123
    message = '\x1b' + 47 * '\0'
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(timeout)
    response_data = {}

    # NTP 서버로 메시지 전송 및 응답 처리
    sock.sendto(message.encode('utf-8'), (host, port))
    response, _ = sock.recvfrom(1024)
    sock.close()

    unpacked = struct.unpack('!B B B b 11I', response)
    t = struct.unpack('!12I', response)[10] - 2208988800
    response_data = {
        'port': port,
        'status': 'open',
        'stratum': unpacked[1],
        'poll': unpacked[2],
        'precision': unpacked[3],
        'root_delay': unpacked[4] / 2**16,
        'root_dispersion': unpacked[5] / 2**16,
        'ref_id': unpacked[6],
        'server_time': time.ctime(t)
    }
    return response_data

def port445_smb(host, timeout=1):
    response_data = {}
    connection = Connection(uuid.uuid4(), host, 445)
    connection.connect(timeout=timeout)
    response_data = {
        'port': 445,
        'status': 'open',
        'negotiated_dialect': connection.dialect
    }
    connection.disconnect()
    return response_data

def port902_vmware_soap(host, port=902, timeout=1):
    response_data = {'port': port, 'status': 'closed'} 

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((host, port))

        soap_request = f"""POST /sdk HTTP/1.1\r
                            Host: {host}:{port}\r
                            Content-Type: text/xml; charset=utf-8\r
                            Content-Length: {{length}}\r
                            SOAPAction: "urn:internalvim25/5.5"\r
                            \r
                            <?xml version="1.0" encoding="utf-8"?>
                            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:vim25="urn:vim25">
                            <soapenv:Header/>
                            <soapenv:Body>
                                <vim25:RetrieveServiceContent>
                                <vim25:_this type="ServiceInstance">ServiceInstance</vim25:_this>
                                </vim25:RetrieveServiceContent>
                            </soapenv:Body>
                            </soapenv:Envelope>"""

        body = soap_request.format(length=len(soap_request) - 2)
        sock.sendall(body.encode('utf-8'))

        response = sock.recv(4096)
        sock.close()

        if response:
            response_data['status'] = 'open'
            response_data['response'] = response.decode('utf-8', errors='ignore')
        else:
            response_data['status'] = 'no response'

    except socket.error as e:
        response_data['status'] = 'error'
        response_data['error_message'] = str(e)

    return response_data

def port3306_mysql(host, timeout=1):
    port = 3306
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    s.connect((host, port))
    packet = s.recv(1024)
    s.close()

    if packet:
        end_index = packet.find(b'\x00', 5)
        server_version = packet[5:end_index].decode('utf-8')
        thread_id = struct.unpack('<I', packet[0:4])[0]
        cap_low_bytes = struct.unpack('<H', packet[end_index + 1:end_index + 3])[0]
        cap_high_bytes = struct.unpack('<H', packet[end_index + 19:end_index + 21])[0]
        server_capabilities = (cap_high_bytes << 16) + cap_low_bytes
        response_data = {
            'port': port,
            'status': 'open',
            'server_version': server_version,
            'thread_id': thread_id,
            'server_capabilities': f'{server_capabilities:032b}'
        }
        return response_data
    

def IMAP_conn(host):
    
    host = "outlook.office365.com" #임시로 설정
    port = 143
    #host = "imap.gmail.com"
    
    response_data = {
        'port': port,
        'status': 'closed',
        'banner': None,
    }
    
    try:
        imap_server = imaplib.IMAP4(host, port)
                
        # 배너정보 가져오기
        banner_info = imap_server.welcome
        response_data['status'] = 'open'
        response_data['banner'] = banner_info
        
        # 디코딩 과정 원래 있었는데 생략
               
        
    except imaplib.IMAP4.error as imap_error:
        #print("IMAP 오류:", imap_error)
        response_data['status'] = 'error'
        response_data['error_message'] = imap_error
        

    except Exception as e:
        #print(f"{port}포트 \n예기치 않은 오류 발생\n{e}\n")
        response_data['status'] = 'error'
        response_data['error_message'] = str(e)
        
    return response_data
        
        
def IMAPS_conn(host):
    host = "outlook.office365.com" #임시로 설정
    port = 993
    
    response_data = {
        'port': port,
        'status': 'closed',
        'banner': None,
    }
    
    try:
        # IMAP 서버에 SSL 연결 설정
        imap_server = imaplib.IMAP4_SSL(host, port)
                
        # 배너정보 가져오기
        banner_info = imap_server.welcome
        banner_info = imap_server.welcome
        response_data['status'] = 'open'
        response_data['banner'] = banner_info
        
            
    except imaplib.IMAP4_SSL.error as ssl_error:
        #print("SSL error:", ssl_error)
        response_data['error_message'] = ssl_error
    
    except imaplib.IMAP4.error as imap_error:
        response_data['status'] = 'error'
        response_data['error_message'] = imap_error

    except Exception as e:
        #print(f"{port}포트 \n예기치 않은 오류 발생\n{e}\n")
        response_data['status'] = 'error'
        response_data['error_message'] = str(e)
        
        
    return response_data

#승희님 161    
def SNMP_conn(host):
    port = 161
    community = 'public'
    host = '192.168.0.35' # 가상머신 서버
    
    response_data = {
        'port': port,
        'status': 'closed',
    }

    # OID 객체 생성
    sysname_oid = ObjectIdentity('SNMPv2-MIB', 'sysName', 0) #시스템 이름
    sysdesc_oid = ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0) #시스템 설명 정보 
    #print("객체 생성")
    
    try: 
        #SNMPD 요청 생성 및 응답
        snmp_request = getCmd(
            SnmpEngine(),
            CommunityData(community),
            UdpTransportTarget((host, port), timeout=0.5, retries=1),
            ContextData(),
            ObjectType(sysname_oid),
            ObjectType(sysdesc_oid)
        )
        
        #요청에 대한 결과 추출
        error_indication, error_status, error_index, var_binds = next(snmp_request)
                
        if error_indication:
            response_data['status'] = 'error'
            response_data['error_message'] = error_indication
        elif error_status:
            response_data['status'] = 'error'
            response_data['error_message'] = 'SNMP error status'
        else:
            response_data['status'] = 'open'
            for var_bind in var_binds:
                if sysname_oid.isPrefixOf(var_bind[0]):
                    response_data['sysname'] = var_bind[1].prettyPrint()
                elif sysdesc_oid.isPrefixOf(var_bind[0]):
                    response_data['sysinfo'] = var_bind[1].prettyPrint()
    except socket.timeout as timeout_error:
        response_data['status'] = 'error'
        response_data['error_message'] = timeout_error

    except socket.error as socket_error:
        response_data['status'] = 'error'
        response_data['error_message'] = socket_error

    except Exception as e:
        response_data['status'] = 'error'
        response_data['error_message'] = str(e)
    
    return response_data


#영창님 21
def scan_ftp_port(host):
    port = 21 #ftp 포트
    response_data = {
        'port': port,
        'status': 'closed',
        'banner': None,
        'error_message': None
    }
    
    try:
        # FTP 서버에 연결 시도
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)  # 연결 시도 시간 초과 설정
        result = sock.connect_ex((host, port))
        
        if result == 0:
            # 포트가 열려 있을 때
            banner = sock.recv(1024).decode('utf-8')
            response_data['status'] = 'open'
            response_data['banner'] = banner
        else:
            # 포트가 닫혀 있거나 필터링됐을 때
            response_data['status'] = 'closed'
        
    except socket.error as err:
        response_data['status'] = 'error'
        response_data['error_message'] = str(err)
        
    finally:
        # 소켓 닫기
        sock.close()
        
    return response_data


#영창님 22
def scan_ssh_port(host):
    port = 22 #ssh 포트
    response_data = {
        'port': port,
        'status': 'closed',
        'banner': None,
        'error_message': None
    }
    
    try:
        # SSH 서버에 연결 시도
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)  # 연결 시도 시간 초과 설정
        result = sock.connect_ex((host, port))
        
        if result == 0:
            # 포트가 열려 있을 때
            banner = sock.recv(1024).decode('utf-8')
            response_data['status'] = 'open'
            response_data['banner'] = banner
        else:
            # 포트가 닫혀 있거나 필터링됐을 때
            response_data['status'] = 'closed'
        
    except socket.error as err:
        response_data['status'] = 'error'
        response_data['error_message'] = str(err)
        
    finally:
        # 소켓 닫기
        sock.close()
        
    return response_data

    