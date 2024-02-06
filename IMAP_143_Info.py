#실제 메일 서버 주소 사용해서 테스트 outlook.office365.com

#선택한 메일함 전부 출력하도록 만들어짐. 필요없는 정보는 없애기

from ignore import username, password, host
import imaplib
import email

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
    return {
        "제목": email_subject.decode(subject_charset or 'utf-8', errors='ignore'),
        "발신자": email_from.decode(from_charset or 'utf-8', errors='ignore'),
        "발신일": email_date,
        "수신자": email_to,
        "이메일 본문": email_body,
        "형식": email_mime_type,
        "우선 순위": email_priority
    }


def IMAP_conn(host, port, username, password):
    
    try:    
        # IMAP 서버에 연결
        imap_server = imaplib.IMAP4(host, port)

        # IMAP 서버에 로그인
        imap_server.login(username, password)
        
        print("Connected to IMAP server successfully.")
        
        # 이메일함 목록 가져오기
        status, mailbox_list = imap_server.list()
        print("Available Mailboxes:")
        for mailbox in mailbox_list:
            print(mailbox.decode("utf-8"))
            
            
        # 이메일함 선택 (예: 'INBOX')
        mailbox = input("\nmailbox: ")
        imap_server.select(mailbox)
        
        # 이메일 검색
        status, email_ids = imap_server.search(None, 'ALL')
        email_ids = email_ids[0].split()
        
        if not email_ids:
            print("이메일함이 비어있습니다.")
            imap_server.logout()
            return

        for email_id in email_ids:
            # 이메일 내용 가져오기
            status, email_data = imap_server.fetch(email_id, '(RFC822)')
            email_message = email.message_from_bytes(email_data[0][1])
                 
            # 이메일 정보 추출
            email_info_dict = email_info(email_message)
                        
            print("Email Information: ")
            for key, value in email_info_dict.items():
                print(f"{key}: {value}")  
            
            # 이메일 본문 출력
            print("\nEmail Body:")
            print(email_info_dict["이메일 본문"])
            print("-" * 30)  # 구분선      
        
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
    

if __name__ == '__main__':
    host = "outlook.office365.com" #outlook.office365.com
    port = 993
    username = username
    password = password

    # IMAP 서버에 연결 및 로그인 시도
    IMAP_conn(host, port, username, password)
