

class KaicongOutput():
    
    def __init__(self, domain, uri_format, user="admin", pwd="123456"):
        """ domain:   Camera IP address or web domain 
                      (e.g. 385345.kaicong.info)
        """
        self.running = False
        self.uri = uri_format.format(domain, user, pwd)
        
        
