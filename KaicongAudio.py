from base.KaicongInput import KaicongInput
import audioop

class KaicongAudio(KaicongInput):
    HEADER_SZ = 32 # Bytes
    PACKET_SZ = 544 # Bytes
    SAMPLE_SZ = 2 # Bytes
    
    RATE_HZ = 8000
    NCHANNELS = 1 
    
    URI = "http://%s:81/audiostream.cgi?user=%s&pwd=%s&streamid=2&filename="
    
    def __init__(self, domain, callback=None, user="admin", pwd="123456"):
        KaicongInput.__init__(
            self, 
            callback,
            domain, 
            KaicongAudio.URI, 
            KaicongAudio.PACKET_SZ, 
            user, 
            pwd
        )

    def handle(self, data):
        # Strip the header at the beginning of the data
        data = data[KaicongAudio.HEADER_SZ:]
        
        # Decompress from ADPCM (differential) to PCM-16L (WAV) format
        result = ""
        state = None
        for i in xrange(0, len(data), KaicongAudio.SAMPLE_SZ):
            adpcmfragment = data[i:i+KaicongAudio.SAMPLE_SZ]
            (sample, state) = audioop.adpcm2lin(
                                adpcmfragment, 
                                KaicongAudio.SAMPLE_SZ, 
                                state)
            result += sample
    
        print len(result)
        return result
        
        
if __name__ == "__main__":
    #Demo of kaicong audio
    import numpy as np
    import sys
    import pyaudio 
    import wave 

    if len(sys.argv) != 2:
        print "Usage: %s <ip_address>" % sys.argv[0]
        sys.exit(-1)
    
    class Speaker:
        def __init__(self):
            CHUNK_SZ = 1016
            self.p = pyaudio.PyAudio() 
            self.stream = self.p.open(format = pyaudio.paInt16, 
                            channels = KaicongAudio.NCHANNELS, 
                            rate = KaicongAudio.RATE_HZ, 
                            input = True, 
                            output = True, 
                            frames_per_buffer = CHUNK_SZ) 
            
        def play(self, numpy_buf):
            signal = wave.struct.pack("%dh"%(len(numpy_buf)), *list(numpy_buf))
            self.stream.write(signal) 
            
        def __del__(self):
            self.stream.stop_stream() 
            self.stream.close() 
            self.p.terminate() 
        
    spkr = Speaker()    
    def play(data):
        spkr.play(np.fromstring(data, dtype=np.int16))
            
    audio = KaicongAudio(sys.argv[1], play)
    audio.run()
    
        
