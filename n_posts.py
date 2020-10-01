# %%
from master_controller import *
from ytsearch import *
import json
import csv
import pandas as pd
import os
import threading
import isodate
from googleapiclient.discovery import build
from datetime import datetime

if not os.path.exists(n_post_dir):
    os.mkdir(n_post_dir)
    
for time_range in overall_time_range:
    i = 0
    last_i = 0
    pageToken = None
    tr = time_range
    
    # Normally collect number of posts for each week, however, I just realized that Dec and Jan were off
    if pd.to_datetime(time_range[0]).month == 12 or pd.to_datetime(time_range[0]).month == 1:
        sq = search_query + '|SARS'
        while True:
            print(i)
            search = youtube_search(sq, youtube, order='viewCount', max_results=50, time_range=tr, pageToken = pageToken, regionCode='ca')
            search_response,channelId,videoId,title,publishedAt = search
            i += len(videoId)
            if i == last_i:
                print('Done.')
                break
            else:
                last_i=i

            if 'nextPageToken' in search_response.keys():
                pageToken = search_response['nextPageToken']
            else:
                print('Done.')
                break
        with open(n_post_dir+'/'+time_range[0][:10]+'__'+ time_range[1][:10] + '_nposts.txt', 'w') as R:
            R.write(str(i))

# %%
