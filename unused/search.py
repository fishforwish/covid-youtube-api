# In[ ]:




# Sample Python code for youtube.search.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from googleapiclient.discovery import build
import argparse
import csv
from unidecode import unidecode

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "credentials.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    #search for videos matching query
    search_response = youtube.search().list(
        part="snippet", 
        maxResults=30, 
        order="viewCount", 
        q="covid|coronavirus|wuhan", 
        publishedAfter="2019-12-15T00:00:00.00Z",
        publishedBefore="2019-12-21T00:00:00.00Z",
        type="video", 
        videoType="any",
        ).execute()
    
    #videos = []
    #channels = []
    #playlists = []
    
    csvFile = open('dec15-21.csv','w')
    csvWriter = csv.writer(csvFile)
    csvWriter.writerow(["Title","URL","Video Id","Published At","Channel Title","Subscriber Count","View Count","Like Count","Dislike Count",
                        "Comment Count"])
   

    #get info from api
    #use search api to get title, videoid, date published, and channelid
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            #videos.append("%s (%s)" % (search_result["snippet"]["title"],\
            #                           search_result["id"]["videoId"]))
            title = search_result["snippet"]["title"]
            title = unidecode(title)  
            videoId = search_result["id"]["videoId"]
            publishedAt = search_result["snippet"]["publishedAt"]
            channelId = search_result["snippet"]["channelId"]
            
            URL = "https://www.youtube.com/watch?v=" + videoId

            #use channel id to get channel name and sub count
            channel_response = youtube.channels().list(
                id = channelId,
                part = "snippet",
                ).execute()
            for channel_result in channel_response.get("items", []):
                channelTitle = channel_result["snippet"]["title"]
                channelTitle = unidecode(channelTitle)

            channel_response2 = youtube.channels().list(
                id = channelId,
                part = "statistics",
                ).execute()
            for channel_result2 in channel_response2.get("items", []):
              #  subscriberCount = channel_result2["statistics"]["subscriberCount"]
                if 'subscriberCount' not in channel_result2["statistics"]:
                    subscriberCount = "N/A"
                else:
                    subscriberCount = channel_result2["statistics"]["subscriberCount"]

            #use video id to get video stats
            video_response = youtube.videos().list(
                id=videoId,
                part="statistics"
                ).execute()
            for video_result in video_response.get("items",[]):
                viewCount = video_result["statistics"]["viewCount"]
                if 'likeCount' not in video_result["statistics"]:
                    likeCount = "N/A"
                else:
                    likeCount = video_result["statistics"]["likeCount"]
                if 'dislikeCount' not in video_result["statistics"]:
                    dislikeCount = "N/A"
                else:
                    dislikeCount = video_result["statistics"]["dislikeCount"]
                if 'commentCount' not in video_result["statistics"]:
                    commentCount = "N/A"
                else:
                    commentCount = video_result["statistics"]["commentCount"]

            csvWriter.writerow([title,URL,videoId,publishedAt,channelTitle,subscriberCount,viewCount,likeCount,dislikeCount,
                                commentCount])

    csvFile.close()

        #response = request.execute()

    #print(response)

if __name__ == "__main__":
    main()