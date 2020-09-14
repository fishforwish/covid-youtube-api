# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from ytsearch import *
import json
import csv
import pandas as pd
import os
import threading


# %%
youtube = googleapiclient.discovery.build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)


# %%
def to_yt_time(time):
    """
    Converts pandas timestamps into Google strings. Not the most robust implementation, but it works
    Args:
        time (pd.Timestamp)
    Returns:
        str
    """
    return str(time)[:10] +'T' + str(time)[11:19]+'Z'

def time_range_maker(start_time, end_time, step=7, end_behavior='clip'):
    """
    Creates a series of beginning and end datetimes for (default) weekly intervals between start_time and end_time.
    Args:
        start_time, end_time (str or datetime-like)
        step (int): number of days in an interval
        end_behavior: 'clip': If your last week has less than 7 days in it, remove it.   
                    'full_length': If your last week has less than 7 days in it, return results coming before end_time.
    Returns:
        list([str, str])
    """
    current_time = pd.to_datetime(start_time)
    pd_end_time = pd.to_datetime(end_time)
    step_timedelta = pd.Timedelta(step, unit='D')
    microstep_timedelta = pd.Timedelta(1, unit = 's')
    
    times_in_range = []
    while current_time <= pd_end_time:
        next_time = current_time+step_timedelta
        times_in_range.append([to_yt_time(current_time+microstep_timedelta), to_yt_time(next_time)])
        current_time = next_time

    times_in_range = times_in_range[:-1]

    if end_behavior == 'clip':
        return times_in_range
    elif end_behavior == 'full_length':
        times_in_range.append([to_yt_time(current_time-step_timedelta+microstep_timedelta), to_yt_time(pd_end_time)])
        return times_in_range


def video_information_from_search(search_query, youtube, time_range=[-1, -1], pageToken = None, order='viewCount'):
    """
    Given a search query, return various statistics about the search query.
    Clearly not fully optimized (threading would make it much faster), but it works. 
    Args:
        search_query (str)
        youtube: googleapiclient.discovery.build object
    Returns:
        pd.DataFrame
    """
    print('Beginning Query:')
    search = youtube_search(search_query, youtube, order=order, max_results=30, time_range=time_range, pageToken = pageToken)
    output_df = pd.DataFrame()
    search_response,channelId,videoId,title,publishedAt = search

    output_df['channelId'] = channelId
    output_df['videoId'] = videoId
    output_df['title'] = title
    output_df['publishedAt'] = publishedAt
    
    print('Finished Query. ')
    
    print('Start getting video stats')
    video_stats_dump = []
    def subfunction_video_info(N, ID, youtube):
        video_stats_dump.append((N, youtube_videos(ID, youtube)))

    # Oops, I accidentally made a 'thread' that doesn't do anything. 
    video_workers = [threading.Thread(target=subfunction_video_info, args = (N, ID, youtube)) for N, ID in enumerate(output_df['videoId'])]
    for worker in video_workers:
        worker.start()
        worker.join()

    video_stats = [x[1] for x in sorted(video_stats_dump, key=lambda x: x[0])]
    output_df['viewCount'] = [stat[1] for stat in video_stats]
    output_df['likeCount'] = [stat[2] for stat in video_stats]
    output_df['dislikeCount'] = [stat[3] for stat in video_stats]
    output_df['commentCount'] = [stat[4] for stat in video_stats]
    output_df['favoriteCount'] = [stat[5] for stat in video_stats]

    print('Start getting channel stats')
    channel_stats_dump = []

    def subfunction_channel_info(N, ID, youtube):
        channel_stats_dump.append((N, youtube_channels(ID, youtube)))

    # Oops, I accidentally made a 'thread' that doesn't do anything. 
    channel_workers = [threading.Thread(target=subfunction_channel_info, args = (N, ID, youtube)) for N, ID in enumerate(output_df['channelId'])]
    for worker in channel_workers:
        worker.start()
        worker.join()

    channel_stats = [x[1] for x in sorted(channel_stats_dump, key=lambda x: x[0])]

    output_df['channelTitle'] = [stat[2] for stat in channel_stats]
    output_df['subscriberCount'] = [stat[3] for stat in channel_stats]

    return output_df, search_response


# %%
if not os.path.exists('yt_data'):
    os.mkdir('yt_data')


# %%
for time_range in time_range_maker('Jan 01, 2020', 'August 12, 2020'):
    print(time_range)
    output_df, request_info = video_information_from_search('coronavirus|covid|wuhan', youtube, time_range=time_range)
    output_df.to_csv('yt_data/'+time_range[0][:10]+'__'+ time_range[1][:10] + '.csv')
    break
