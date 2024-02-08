# 포트 오픈 여부 판별하도록 수정

import socket
import struct
import time
import uuid
import imaplib
from pysnmp.hlapi import *
from smbprotocol.connection import Connection


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

def port902_vmware_soap(host, timeout=1):
    ports = [902]  # 902 포트만 스캔
    response_data = []

    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        
        try:
            sock.connect((host, port))

            # SOAP 요청 본문 준비
            soap_request = f"""POST /sdk HTTP/1.1
            Host: {host}:{port}
            Content-Type: text/xml; charset=utf-8
            Content-Length: {{length}}
            SOAPAction: "urn:internalvim25/5.5"

            <?xml version="1.0" encoding="utf-8"?>
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:vim25="urn:vim25">
            <soapenv:Header/>
            <soapenv:Body>
                <vim25:RetrieveServiceContent>
                <vim25:_this type="ServiceInstance">ServiceInstance</vim25:_this>
                </vim25:RetrieveServiceContent>
            </soapenv:Body>
            </soapenv:Envelope>"""

            body = soap_request.format(length=len(soap_request))
            sock.sendall(body.encode('utf-8'))

            # 서비스로부터 응답 받기
            response = sock.recv(4096)

            if response:
                response_data.append({
                    'port': port,
                    'status': 'open',
                    'response': response.decode('utf-8', errors='ignore')
                })
            else:
                response_data.append({'port': port, 'status': 'no response'})

        except socket.error as e:
            response_data.append({'port': port, 'status': 'error', 'error': str(e)})
        finally:
            sock.close()

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
    
    host = "outlook.office365.com"
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
        response_data['error_message'] = e
        
    return response_data
        
        
def IMAPS_conn(host):
    host = "outlook.office365.com"
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
        
        # 디코딩 과정 생략
        # # 배너정보 가져오기
        # banner_info = imap_server.welcome
        
        # response_data.append({'port': port, 'status': 'open'})
        
        # # Base64로 인코딩된 데이터 추출
        # # 먼저 바이트 문자열에서 문자열로 변환
        # banner_info_str = banner_info.decode('utf-8')
        # pure_banner_info = banner_info_str.split('[')[0]
        # encoded_data = banner_info_str.split('[')[1].split(']')[0]
       
        # # Base64 디코딩
        # decoded_data = base64.b64decode(encoded_data)
        # print(f'banner_info: {pure_banner_info}')
       
        # # 디코딩된 데이터를 문자열로 변환 (UTF-8 인코딩 사용)
        # try:
        #     decoded_string = decoded_data.decode('utf-8')
        #     print(f'생성서버: {decoded_string}')
        # except UnicodeDecodeError:
        #     print("UTF-8 디코딩 실패")
            
    except imaplib.IMAP4_SSL.error as ssl_error:
        #print("SSL error:", ssl_error)
        response_data['error_message'] = ssl_error
        return response_data
    
    except imaplib.IMAP4.error as imap_error:
        response_data['status'] = 'error'
        response_data['error_message'] = imap_error
        return response_data

    except Exception as e:
        #print(f"{port}포트 \n예기치 않은 오류 발생\n{e}\n")
        response_data['status'] = 'error'
        response_data['error_message'] = e
        return response_data
        
        
    return response_data
  
    
# snmp 꺼져있을 때 더 오래걸림
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
        response_data['error_message'] = e
    
    return response_data
    