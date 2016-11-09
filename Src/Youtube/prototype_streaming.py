

import httplib2
import os
import sys

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret.
CLIENT_SECRETS_FILE = "client_secret.json"

YOUTUBE_READ_WRITE_SCOPE = "https://www.googleapis.com/auth/youtube"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0
  
"""
def get_authenticated_service(args):
  flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
    scope=YOUTUBE_READ_WRITE_SCOPE,
    message=MISSING_CLIENT_SECRETS_MESSAGE)

  storage = Storage("%s-oauth2.json" % sys.argv[0])
  credentials = storage.get()

  if credentials is None or credentials.invalid:
    credentials = run_flow(flow, storage, args)

  return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    http=credentials.authorize(httplib2.Http()))

# Create a liveBroadcast resource and set configuration
def insert_broadcast(youtube, options):
  insert_broadcast_response = youtube.liveBroadcasts().insert(
   part="snippet,status,contentDetails",
    body=dict(
      snippet=dict(
        title=options.broadcast_title,
        scheduledStartTime=options.start_time,
        scheduledEndTime=options.end_time
      ),
      status=dict(
        privacyStatus=options.privacy_status
      ),
      contentDetails=dict(
        monitorStream=dict(
          enableMonitorStream = 'true'
          )

        )  
    )
  ).execute()

  snippet = insert_broadcast_response["snippet"]

  print "Broadcast '%s' with title '%s' was published at '%s'." % (
    insert_broadcast_response["id"], snippet["title"], snippet["publishedAt"])
  return insert_broadcast_response["id"]

# Create a liveStream resource and set configuration
def insert_stream(youtube, options):
  insert_stream_response = youtube.liveStreams().insert(
    part="snippet,cdn",
    body=dict(
      snippet=dict(
        title=options.stream_title
      ),
      cdn=dict(
        format="240p",
        ingestionType="rtmp"
      )
    )
  ).execute()

  snippet = insert_stream_response["snippet"]
  print ("Tu stream ID es : " + insert_stream_response["id"])
  return insert_stream_response["id"]

# Bind the broadcast to the video stream.
def bind_broadcast(youtube, broadcast_id, stream_id):
  bind_broadcast_response = youtube.liveBroadcasts().bind(
    part="id,contentDetails",
    id=broadcast_id,
    streamId=stream_id
  ).execute()

if __name__ == "__main__":
  argparser.add_argument("--broadcast-title", help="Broadcast title",
    default="Prueba")
  argparser.add_argument("--privacy-status", help="Broadcast privacy status",
    default="private")
  argparser.add_argument("--start-time", help="Scheduled start time",
    default='2016-10-24T19:30:00.000+02:00')
  argparser.add_argument("--end-time", help="Scheduled end time",
    default='2016-10-24T19:35:00.000+02:00')
  argparser.add_argument("--stream-title", help="Stream title",
    default="Creado ahora mismo")
  args = argparser.parse_args()

  youtube = get_authenticated_service(args)
  try:
    broadcast_id = insert_broadcast(youtube, args)
    stream_id = insert_stream(youtube, args)
    bind_broadcast(youtube, broadcast_id, stream_id)
  except HttpError, e:
    print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)