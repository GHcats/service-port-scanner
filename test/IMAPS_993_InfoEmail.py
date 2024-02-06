#실제 메일 서버 주소 사용해서 테스트 outlook.office365.com
#993 IMAPS는 IMAP과 크게 다른 것은 없고 암호화 통신을 함

# 암호화 디코딩은 못함. 선택한 메일함 전부 출력하도록 만들어짐. 필요없는 정보는 없애기

from ignore import username, password
import imaplib
import ssl
import base64

def IMAPS_conn(host, port):
    
    try:
        # IMAP 서버에 SSL 연결 설정
        imap_server = imaplib.IMAP4_SSL(host, port)
        
        # 사용자 로그인
        imap_server.login(username, password)

        # 배너정보 가져오기
        banner_info = imap_server.welcome
        
        # Base64 디코딩 및 출력 (ISO-8859-1 인코딩 사용)
        #decoded_data = base64.b64decode(banner_info)
        print("Connected to IMAP server successfully.")   
        try:
            decoded_data = base64.b64decode(banner_info).decode('utf-16')   
            print(decoded_data)
        except Exception as decode_error:
            decoded_data = banner_info.decode('utf-8')
            print('실패')
#        print("Banner Information: ", banner_info.decode('utf-8'))

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
 
    # IMAP 서버에 연결 및 로그인 시도
    IMAPS_conn(host, port)