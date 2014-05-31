from base.KaicongInput import KaicongInput

class KaicongVideo(KaicongInput):
    PACKET_SIZE = 1024
    URI = "http://%s:81/livestream.cgi?user=%s&pwd=%s&streamid=3&audio=1&filename="
    
    def __init__(self, domain, callback, user="admin", pwd="123456"):
        KaicongInput.__init__(
            self, 
            callback,
            domain, 
            KaicongVideo.URI, 
            KaicongVideo.PACKET_SIZE, 
            user, 
            pwd
        )
        self.bytes = ''
    
    def handle(self, data):
        self.bytes += data
        a = self.bytes.find('\xff\xd8')
        b = self.bytes.find('\xff\xd9')
        if a!=-1 and b!=-1:
            jpg = self.bytes[a:b+2]
            self.bytes = self.bytes[b+2:]
            return jpg
            
            
if __name__ == "__main__":
    import numpy as np
    import cv2
    import sys
    
    if len(sys.argv) != 2:
        print "Usage: %s <ip_address>" % sys.argv[0]
        sys.exit(-1)
    
    def show_video(jpg):    
        img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.CV_LOAD_IMAGE_COLOR)
        cv2.imshow('i',img)
        
        # Note: waitKey() actually pushes the image out to screen
        if cv2.waitKey(1) ==27:
            exit(0)  
    
    video = KaicongVideo(sys.argv[1], show_video)
    video.run()
