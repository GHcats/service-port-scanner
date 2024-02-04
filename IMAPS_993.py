#IMAPS 993port
def IMAPS_conn(target_host, port, username, password):
    import imaplib
    
    try:
        #IMAP서버에 SSL 연결 설정
        imap_server = imaplib.IMAP4_SSL(target_host,port)
        
        #서버 오픈
        imap_server.open(target_host, port)
        
        #로그인
        response, _ = imap_server.login(username, password)
        
        if response == 'OK':
            #메일수집
            imap_server.select()
            print("Login OK")
            return (True)
        else:
            print("Login failed.")
            return (True)
        
    except imaplib.IMAP4_SSL.error as ssl_error:
        print("SSL error:", ssl_error)
        return (None)
    
    except imaplib.IMAP4.error as imap_error:
        print("IMAP error:", imap_error)
        return (None)
    
    except Exception as e:
        print("An unexpected error occurred:", e)
        return (None)

if __name__ == '__main__':
    host="127.0.0.1"
    port=993
    username = "username"
    pwd = "pwd"
    IMAPS_conn(host, port, username, pwd)
    
