import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import argparse
import csv
from unidecode import unidecode

DEVELOPER_KEY = "AIzaSyCpaXGzpOVrZM55K4FSgCHQu-c7SAizVsI"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def youtube_search(q, max_results=30 ,order="viewCount"):

    youtube = googleapiclient.discovery.build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
      developerKey=DEVELOPER_KEY)
    search_response = youtube.search().list(
        part="snippet",
        eventType="completed", 
        maxResults= max_results, 
        order= order, 
        q=q, 
        #publishedAfter="2020-01-T00:00:00.00Z",
        #publishedBefore="2020-01-30T00:00:00.00Z",
        type="video", 
        videoType="any",
        ).execute() 

    return(search_response)
