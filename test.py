def IMAP_conn(target_host, port, username, password):
    import imaplib
    service_name="IMAP"
    try:
        imap_server = imaplib.IMAP4(target_host)
        imap_server.login(username, password)
        response = imap_server.select()  # Select a mailbox (e.g., "INBOX")
        
        if response[0] == 'OK':
            return (True, service_name)
        else:
            #print("Login failed.")
            return (True, service_name)
    except imaplib.IMAP4.error as imap_error:
        #print("IMAP error:", imap_error)
        return (None, service_name)
    except Exception as e:
        #print("An unexpected error occurred:", e)
        return (None, service_name)