ffmpeg  -f alsa -i default -ac 2 -f video4linux2 -i /dev/video0 -vcodec libx264 /
-f flv -r 15 -q 3 -b:v 320k -s 320x240 -acodec libmp3lame -ar 44100 -ab 128k -threads 0 /
-bufsize 64k -force_key_frames 0:00:01 /




///CODIGO CON SUBTITULO 

ffmpeg -f alsa -i default -ac 2 -f video4linux2 -i /dev/video0 -vcodec libx264 /
 -vf drawtext="fontfile=/usr/share/fonts/truetype/freefont/FreeSerif.ttf: textfile=sub.txt:reload=1" /
 -f flv -r 15 -q 3 -b:v 320k -s 320x240 -acodec libmp3lame -ar 44100 -ab 128k -threads 0 -bufsize 64k -force_key_frames 0:00:01 /
 rtmp://a.rtmp.youtube.com/live2/b1dd-v5f8-f70b-9v6g