#!/usr/bin/python

import httplib2
import os
import sys
import json

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow



CLIENT_SECRETS_FILE = "./private/client_secret.json"

# This OAuth 2.0 access scope allows for read-only access to the authenticated
# user's account, but not other types of account access.
YOUTUBE_READONLY_SCOPE = "https://www.googleapis.com/auth/youtube.readonly"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0
  
"""

data_output = {"data": []}

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

def list_broadcasts(youtube,status):

  

  list_broadcasts_request = youtube.liveBroadcasts().list(
    broadcastStatus= status,
    part="snippet, contentDetails",
    maxResults=50
  )

  while list_broadcasts_request:
    broadcast_response = list_broadcasts_request.execute()
    for broadcast in broadcast_response.get("items", []):

      title = broadcast["snippet"]["title"]
      monitorStream = broadcast["contentDetails"]["monitorStream"]["embedHtml"]
      stream_id = broadcast["contentDetails"]["boundStreamId"]
      stream_key = getStreamKey(youtube,stream_id)
      data_output["data"].append({"title" : title , "streamkey" : stream_key, "monitor": monitorStream})

    list_broadcasts_request = youtube.liveBroadcasts().list_next(list_broadcasts_request, broadcast_response)

  

# Retrieve a list of the liveStream resources
def getStreamKey(youtube,stream_id):

  list_streams_request = youtube.liveStreams().list(
    part="cdn",
    id=stream_id,
    maxResults=1
  )
  list_streams_response = list_streams_request.execute()
  return list_streams_response["items"][0]["cdn"]["ingestionInfo"]["streamName"]

if __name__ == "__main__":
  argparser.add_argument("--status")
  args = argparser.parse_args()
  youtube = get_authenticated_service(args)
  try:
    list_broadcasts(youtube,args.status)
    print  json.dumps(data_output)
  except HttpError, e:
    print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)