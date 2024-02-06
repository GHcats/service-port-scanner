import imaplib
import base64

def IMAP_conn(host, port):
    try:
        # IMAP 서버에 연결
        imap_server = imaplib.IMAP4(host, port)        
        
        print("Connected to IMAP server successfully.")   
        
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

        
    except imaplib.IMAP4.error as imap_error:
        print("IMAP error:", imap_error)
        
    except Exception as e:
        print("An unexpected error occurred:", e)

if __name__ == '__main__':
    host = "outlook.office365.com"
    port = 143

    # IMAP 서버에 연결 및 로그인 시도
    IMAP_conn(host, port)