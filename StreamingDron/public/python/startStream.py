import os
import sys
import argparse
from subprocess import Popen

def list_streams(path,stream_key,resolution,bitrate):
  
  command ='ffmpeg -f alsa -ac 2 -i default -f image2 -framerate 15 -loop 1 -i ' + path + ' -vcodec libx264 -preset veryfast -minrate ' + bitrate  + ' -maxrate 1000k -bufsize 1000k -vf "format=yuv420p"  -g 30 -vf drawtext="fontfile=/usr/share/fonts/truetype/freefont/FreeSerif.ttf:fontsize=24:fontcolor=yellow:textfile=./public/static/subtitles.txt:reload=1:x=100:y=50" -c:a libmp3lame -b:a 128k -ar 44100 -force_key_frames 0:00:04 -f flv rtmp://a.rtmp.youtube.com/live2/'+ stream_key
  os.system(command)
  
if __name__ == "__main__":
  try:
    subProcess = Popen(['python3','./public/JdeRobot/ffmpegAdapter/ffmpeg-adapter.py', '--Ice.Config=./public/JdeRobot/ffmpegAdapter/adapter_conf.cfg'])
    list_streams(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
  except:
    print("ERROR")
