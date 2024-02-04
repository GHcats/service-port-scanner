import imaplib

# IMAP 서버 정보
imap_server = "outlook.office365.com"  # IMAP 서버 주소
imap_port = 143  # 포트 번호 (143은 기본값)

# 계정 정보
username = "cytmdgml@gmail.com"
password = "WODQKSEKF*"

# IMAP 서버에 연결
imap_connection = imaplib.IMAP4(imap_server, imap_port)

# IMAP 서버에 로그인
imap_connection.login(username, password)

# 이제 IMAP 서버에 연결되었고 로그인되었습니다.

# 원하는 작업을 수행할 수 있습니다.

# 연결 종료
imap_connection.logout()
