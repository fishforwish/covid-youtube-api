from ytsearch import youtube_search
import json

test = youtube_search("coronavirus|covid|wuhan")
print(test)

#csvFile = open('testing.csv','w')
#csvWriter = csv.writer(csvFile)
#csvWriter.writerow(["title","videoId","publishedAt","channelTitle","subscriberCount","viewCount","likeCount","dislikeCount",
 #                       "commentCount","favoriteCount"])

#youtube_search("coronavirus|covid|wuhan")
#youtube_videos(videoId)
#youtube_channels(channelId)


#csvWriter.writerow([title,videoId,publishedAt,channelTitle,subscriberCount,viewCount,likeCount,dislikeCount,
   #                             commentCount,favoriteCount])

#csvFile.close()