#친절한 문구 추가하기

import imaplib
import email
from pysnmp.hlapi import *

#메일 내용을 출력하도록 만들었는디
def email_info(email_message):
    email_subject = email_message["Subject"]
    email_from = email_message["From"]
    email_date = email_message["Date"]
    email_to = email_message["To"]
    email_mime_type = email_message.get_content_type()
    email_priority = email_message["X-Priority"]  # 이메일 우선 순위
    
    email_body = ""
    email_headers = ""

    # 이메일 본문 추출
    if email_mime_type == "text/plain":
        email_body = email_message.get_payload()
    elif email_mime_type == "text/html":
        email_body = "HTML 이메일입니다."

    # 이메일 헤더 정보 추출
    for key, value in email_message.items():
        email_headers += f"{key}: {value}\n"

    return {
        "제목": email_subject,
        "발신자": email_from,
        "발신일": email_date,
        "수신자": email_to,
        "이메일 본문": email_body,
        "이메일 헤더": email_headers,
        "형식": email_mime_type,
        "우선 순위": email_priority
    }
    
def IMAP_conn(host, port, use_ssl=False):
    username = input('username: ')
    password = input('password: ')
    
    try:
        if use_ssl:
            imap_server = imaplib.IMAP4_SSL(host, port)
        else:
            imap_server = imaplib.IMAP4(host, port)

        imap_server.login(username, password)
        print(f"Connected to {'IMAPS' if use_ssl else 'IMAP'} server successfully.")

        status, mailbox_list = imap_server.list()
        print("Available Mailboxes:")
        for mailbox in mailbox_list:
            print(mailbox.decode("utf-8"))

        mailbox = input("\nmailbox: ")
        imap_server.select(mailbox)

        status, email_ids = imap_server.search(None, 'ALL')
        email_ids = email_ids[0].split()

        if not email_ids:
            print("이메일함이 비어있습니다.")
            imap_server.logout()
            return

        for email_id in email_ids:
            status, email_data = imap_server.fetch(email_id, '(RFC822)')
            email_message = email.message_from_bytes(email_data[0][1])
            email_info_dict = email_info(email_message)

            print("Email Information: ")
            for key, value in email_info_dict.items():
                print(f"{key}: {value}")

            print("\nEmail Body:")
            print(email_info_dict["이메일 본문"])
            print("-" * 30)

        imap_server.logout()
        return imap_server

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
        UdpTransportTarget((host, port), timeout=30, retries=1),
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

    # IMAPS 연결 (SSL 사용)
    IMAP_conn(host, 993, use_ssl=True)

    # SNMP 연결
    SNMP_conn(host)
