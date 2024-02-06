#실제 메일 서버 주소 사용해서 테스트 outlook.office365.com
#993 IMAPS는 IMAP과 크게 다른 것은 없고 암호화 통신을 함

# 배너정보 출력하도록 수정하기

from ignore import username, password, host
import imaplib

def IMAPS_conn(host, port, username, password):
    
    try:
        # IMAP 서버에 SSL 연결 설정
        imap_server = imaplib.IMAP4_SSL(host, port)
        
        # 사용자 로그인
        imap_server.login(username, password)
        
        # 연결 및 로그인 성공한 경우
        print("Connected to IMAP4 server successfully.")
        return True
        
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
    imaps_connection = IMAPS_conn(host, port, username, password)
    
    #연결종료
    imaps_connection.logout()
    