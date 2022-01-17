class RedMQException(Exception):
    '''
    
    '''

    def __init__(self, *argv, **argkw):
        super().__init__(*argv, **argkw)

class RedMQRequestException(RedMQException):
    '''
    
    '''

    def __init__(self, http_status, http_headers, http_body):
        super().__init__()
        self.http_status = http_status
        self.http_headers = http_headers
        self.http_body = http_body

    