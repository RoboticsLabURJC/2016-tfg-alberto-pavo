
import httplib2
import os
import sys
import json

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow


# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret.
CLIENT_SECRETS_FILE = "client_secret.json"


YOUTUBE_READONLY_SCOPE = "https://www.googleapis.com/auth/youtube.readonly"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

"""

def get_authenticated_service(args):
  flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
    scope=YOUTUBE_READONLY_SCOPE,
    message=MISSING_CLIENT_SECRETS_MESSAGE)

  storage = Storage("%s-oauth2.json" % sys.argv[0])
  credentials = storage.get()

  if credentials is None or credentials.invalid:
    credentials = run_flow(flow, storage, args)

  return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    http=credentials.authorize(httplib2.Http()))

# Retrieve a list of the liveStream resources associated with the currently
# authenticated user's channel.
def list_streams(youtube,stream_id):
  
  stream = youtube.liveStreams().list(
    part="snippet, cdn",
    id= stream_id, #recupero solo el id que me interesa
    maxResults=50
  ).execute()

  stream_key = stream["items"][0]["cdn"]["ingestionInfo"]["streamName"]
  print("Este es tu Stream Key" + stream_key)
  outfile = open('ffmpeg.sh', 'a+') 
  outfile.write("/" + stream_key)
  outfile.close()
  os.system("chmod 0755 ffmpeg.sh")
  os.system("./ffmpeg.sh")
  

if __name__ == "__main__":
  argparser.add_argument("--stream-id") 
  args = argparser.parse_args()
  youtube = get_authenticated_service(args)
  try:
    list_streams(youtube,"SZvq_huJb9LOJXRK0YqEDA1478945098060469")
  except HttpError, e:
    print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
  except IndexError:
    #Error que se puede dar al buscar un stream key que no exista
    print "No livestream with this Stream Key"