# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from ytsearch import *
import json
import csv
import pandas as pd
import os
import threading
import isodate
from googleapiclient.discovery import build
from datetime import datetime

DEVELOPER_KEY = "insert_your_devkey_here"
search_query = 'coronavirus|covid|wuhan'

overall_time_range = time_range_maker('Dec 01, 2019', datetime.now())

output_dir = 'updated_yt_data'
n_post_dir = 'n_posts'
youtube = googleapiclient.discovery.build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
        developerKey=DEVELOPER_KEY)

def video_information_from_search(search_query, youtube, time_range=[-1, -1], pageToken = None, order='viewCount', regionCode='ca'):

    search = youtube_search(search_query, youtube, order=order, max_results=30, time_range=time_range, pageToken = pageToken, regionCode=regionCode)
    output_df = pd.DataFrame()
    search_response,channelId,videoId,title,publishedAt = search
    output_df['codingWeek'] = [time_range[0][:10]+'-'+ time_range[1][:10] for _ in range(len(channelId))]
    output_df['channelId'] = channelId
    output_df['videoId'] = videoId
    output_df['title'] = title
    output_df['publishedAt'] = publishedAt

    print('Finished Query. ')

    print('Total number of results: ' + str(len(output_df['videoId'])))

    if len(output_df['videoId']) == 0: # break if no videos found
        return output_df, search_response
    video_stats = youtube_videos(output_df['videoId'].tolist(), youtube)

    output_df['viewCount'] = video_stats[1]
    output_df['likeCount'] = video_stats[2]
    output_df['dislikeCount'] = video_stats[3]
    output_df['commentCount'] = video_stats[4]
    output_df['favoriteCount'] = video_stats[5]
    output_df['duration'] = video_stats[6]

    channel_stats = youtube_channels(output_df['channelId'].tolist(), youtube)
    output_df['channelTitle'] = channel_stats[1]
    output_df['subscriberCount'] = channel_stats[2]
    output_df['country'] = channel_stats[3]

    output_df['videoURL'] = ['https://www.youtube.com/watch?v='+i for i in output_df['videoId']]
    output_df['duration'] = [isodate.parse_duration(i).seconds for i in output_df['duration']]
    
    output_df = output_df.drop(columns=['favoriteCount'])
    print()
    return output_df, search

# %%
if not os.path.exists(output_dir):
    os.mkdir(output_dir)
if not os.path.exists(n_post_dir):
    os.mkdir(n_post_dir)

for time_range in overall_time_range:
    if pd.to_datetime(time_range[0]).month == 12 or pd.to_datetime(time_range[0]).month == 1:
        sq = search_query + '|SARS'
    print(time_range)
    output_df, request_info = video_information_from_search(sq, youtube, time_range=time_range)
    output_df.to_csv(output_dir+'/'+time_range[0][:10]+'__'+ time_range[1][:10] + '.csv')

# # %%

# for time_range in overall_time_range:
#     i = 0
#     last_i = 0
#     pageToken = None
#     tr = time_range
#     while True:
#         print(i)
#         search = youtube_search(search_query, youtube, order='viewCount', max_results=50, time_range=tr, pageToken = pageToken, regionCode='ca')
#         search_response,channelId,videoId,title,publishedAt = search
#         i += len(videoId)
#         if i == last_i:
#             print('Done.')
#             break
#         else:
#             last_i=i

#         if 'nextPageToken' in search_response.keys():
#             pageToken = search_response['nextPageToken']
#         else:
#             print('Done.')
#             break
#     #with open(n_post_dir+'/'+time_range[0][:10]+'__'+ time_range[1][:10] + '_nposts.txt', 'w') as R:
#     #    R.write(str(i))

# %%

# %%
