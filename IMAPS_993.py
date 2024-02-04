from ignore import username, password, host

def imap_conn(server, port, username, password):
    import imaplib
        
    try:
        # IMAP 서버에 SSL 연결 설정
        imap_server = imaplib.IMAP4_SSL(server, port)
        
        # 사용자 로그인
        imap_server.login(username, password)
        
        # 연결 및 로그인 성공한 경우
        print("Connected to IMAP server successfully.")
        return imap_server
        
    except imaplib.IMAP4_SSL.error as ssl_error:
        print("SSL error:", ssl_error)
        
    except imaplib.IMAP4.error as imap_error:
        print("IMAP error:", imap_error)
        
    except Exception as e:
        print("An unexpected error occurred:", e)
    
    # 연결 또는 로그인 실패한 경우 None 반환
    return None

if __name__ == '__main__':
    host = "outlook.office365.com" #outlook.office365.com
    port = 993

    # IMAP 서버에 연결 및 로그인 시도
    imap_connection = imap_conn(host, port, username, password)
    
    #연결종료
    imap_connection.logout()
    