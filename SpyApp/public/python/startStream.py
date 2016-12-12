import os
import sys
import argparse

def list_streams(stream_key):
  
  print stream_key
  os.system("chmod +rw ./public/static/ffmpeg.sh")
  outfile = open('./public/static/ffmpeg.sh', 'a+') 
  outfile.write("rtmp://a.rtmp.youtube.com/" + stream_key)
  outfile.close()
  os.system("chmod 0755 ./public/static/ffmpeg.sh")
  os.system("./public/static/ffmpeg.sh")
  print "Streaming Started"
  
if __name__ == "__main__":

  print(sys.argv[1])
  list_streams(sys.argv[1])
