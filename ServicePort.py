import imaplib
import base64
from pysnmp.hlapi import *

def IMAP_conn(host, port, use_ssl=False):
    
    try:
        if use_ssl: #993 IMAPS
            imap_server = imaplib.IMAP4_SSL(host, port)
        else: #143 IMAP
            imap_server = imaplib.IMAP4(host, port)
        print(f"Connected to {'IMAPS' if use_ssl else 'IMAP'} server successfully.")
        
        # 배너정보 가져오기
        banner_info = imap_server.welcome

        # Base64로 인코딩된 데이터 추출
        # 먼저 바이트 문자열에서 문자열로 변환
        banner_info_str = banner_info.decode('utf-8')
        pure_banner_info = banner_info_str.split('[')[0]
        encoded_data = banner_info_str.split('[')[1].split(']')[0]
       
        # Base64 디코딩
        decoded_data = base64.b64decode(encoded_data)
        print(f'banner_info: {pure_banner_info}')
       
        # 디코딩된 데이터를 문자열로 변환 (UTF-8 인코딩 사용)
        try:
            decoded_string = decoded_data.decode('utf-8')
            print(f'생성서버: {decoded_string}')
        except UnicodeDecodeError:
            print("UTF-8 디코딩 실패")


    except imaplib.IMAP4_SSL.error as ssl_error:
        print("SSL error:", ssl_error)
        return None

    except imaplib.IMAP4.error as imap_error:
        print("IMAP error:", imap_error)
        return None

    except Exception as e:
        print("An unexpected error occurred:", e)
        return None

def SNMP_conn(host):
    port = 161
    community = 'public'

    sysname_oid = ObjectIdentity('SNMPv2-MIB', 'sysName', 0)
    sysdesc_oid = ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)

    snmp_request = getCmd(
        SnmpEngine(),
        CommunityData(community),
        UdpTransportTarget((host, port), timeout=10, retries=1),
        ContextData(),
        ObjectType(sysname_oid),
        ObjectType(sysdesc_oid)
    )

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

if __name__ == '__main__':
    host = '127.0.0.1'

    # IMAP 연결
    IMAP_conn(host, 143, use_ssl=False)
    print('IMAP 스캔 완료')

    # IMAPS 연결 (SSL 사용)
    IMAP_conn(host, 993, use_ssl=True)
    print('IMAPS 스캔 완료')

    # SNMP 연결
    SNMP_conn(host)
    print('SNMP 스캔 완료')
