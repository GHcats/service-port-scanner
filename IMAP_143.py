#outlook 서비스가 993포트로 이용중이어서 안 되는 것 같음.
#993이 됐으니까 되지 않을까..?
#143 IMAP는 평문통신을 함

# 배너그래빙 정보 출력하도록 수정하기

from ignore import username, password, host
import imaplib

def IMAP_conn(server, port, username, password):
    try:    
        # IMAP 서버에 연결
        imap_connection = imaplib.IMAP4(host, port)

        # IMAP 서버에 로그인
        imap_connection.login(username, password)
        
        print("Connected to IMAP server successfully.")
        return True
    
    except imaplib.IMAP4.error as imap_error:
        print("IMAP error:", imap_error)
        return None
    
    except Exception as e:
        print("An unexpected error occurred:", e)
        return None
        
    
if __name__ == '__main__':
    host = "outlook.office365.com" #outlook.office365.com
    port = 143
    username = username
    password = password

    # IMAP 서버에 연결 및 로그인 시도
    imap_connection = IMAP_conn(host, port)
    
    #연결종료
    imap_connection.logout()

