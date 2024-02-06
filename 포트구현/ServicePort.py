import imaplib
import base64
from pysnmp.hlapi import *
import logging
import socket

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def IMAP_conn(host, port, use_ssl=False):   
    try:
        if use_ssl: #993 IMAPS
            imap_server = imaplib.IMAP4_SSL(host, port)
        else: #143 IMAP
            imap_server = imaplib.IMAP4(host, port)
        print(f"Connected to {'IMAPS' if use_ssl else 'IMAP'} server successfully.")
        
        # 배너정보 가져오기
        banner_info = imap_server.welcome

        # Base64 디코딩
        banner_info_str = banner_info.decode('utf-8')
        pure_banner_info = banner_info_str.split('[')[0]
        encoded_data = banner_info_str.split('[')[1].split(']')[0]
        decoded_data = base64.b64decode(encoded_data)
        logger.info(f'배너 정보: {pure_banner_info}')
       
        # 디코딩된 데이터를 문자열로 변환 (UTF-8 인코딩 사용)
        try:
            decoded_string = decoded_data.decode('utf-8')
            logger.info(f'생성 서버: {decoded_string}')
        except UnicodeDecodeError:
            logger.warning("UTF-8 디코딩 실패")


    except imaplib.IMAP4_SSL.error as ssl_error:
        logger.error("SSL 오류:", ssl_error)
        return None

    except imaplib.IMAP4.error as imap_error:
        logger.error("IMAP 오류:", imap_error)
        return None

    except Exception as e:
        logger.error("예기치 않은 오류 발생:", e)
        return None

def SNMP_conn(host):
    port = 161
    community = 'public'

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
                logger.error(f"에러: {error_indication}")
        elif error_status:
            logger.error(f"에러 상태: {error_status}")
        else:
            for var_bind in var_binds:
                if sysname_oid.isPrefixOf(var_bind[0]):
                    logger.info(f"시스템 이름: {var_bind[1].prettyPrint()}")
                elif sysdesc_oid.isPrefixOf(var_bind[0]):
                    logger.info(f"시스템 설명: {var_bind[1].prettyPrint()}")
    except socket.timeout as timeout_error:
        logger.error(f"연결 시간 초과: {timeout_error}")

    except socket.error as socket_error:
        logger.error(f"소켓 오류: {socket_error}")

    except Exception as e:
        logger.error("예기치 않은 오류 발생:", e)

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