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

# This OAuth 2.0 access scope allows for read and write access to the authenticated
YOUTUBE_READ_WRITE_SCOPE = "https://www.googleapis.com/auth/youtube"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.
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

def stop_broadcast(youtube,brID):

	broadcast_request = youtube.liveBroadcasts().transition(
    broadcastStatus= "complete",
    id = brID,
    part = "status")
	broadcast_request.execute()


if __name__ == "__main__":
	argparser.add_argument("--brID")
	args = argparser.parse_args()
	youtube = get_authenticated_service(args)
	try:
		stop_broadcast(youtube,args.brID)
		os.system("pkill ffmpeg")
		print("Event Stoped")
	except:
		print("ERROR")
   	
