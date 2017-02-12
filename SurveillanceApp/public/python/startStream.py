import os
import sys
import argparse

def list_streams(stream_key,resolution,bitrate):
  
  print stream_key
  os.system("chmod +rw ./public/static/ffmpeg.sh")
  outfile = open('./public/static/ffmpeg.sh', 'w') 
  outfile.write('ffmpeg -f alsa -ac 2 -i default -f video4linux2 -framerate 15 -video_size ' + resolution +
    ' -i /dev/video0 -vcodec libx264 -preset veryfast -minrate ' + bitrate  + ' -maxrate 1000k -bufsize 1000k -vf "format=yuv420p"  -g 30 -vf drawtext="fontfile=/usr/share/fonts/truetype/freefont/FreeSerif.ttf:fontsize=24:fontcolor=yellow:textfile=./public/static/subtitles.txt:reload=1:x=100:y=50" -c:a libmp3lame -b:a 128k -ar 44100 -force_key_frames 0:00:04 -f flv rtmp://a.rtmp.youtube.com/live2/' + stream_key)
  outfile.close()
  os.system("chmod 0755 ./public/static/ffmpeg.sh")
  os.system("./public/static/ffmpeg.sh")
  
if __name__ == "__main__":
  try:
    list_streams(sys.argv[1],sys.argv[2],sys.argv[3])
  except:
    print("ERROR")
