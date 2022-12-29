import pandas as pd
import pprint

from services import YouTubeApi, YouTubeData

youtube = YouTubeApi()
def main(filename):
  history_data = pd.read_csv(filename)
  data = []

  for videoId in history_data.videoId:
    response = youtube.get_video_with_id(videoId)
    video_info = youtube.get_video_data(response)
    data.append(video_info)

  pd.DataFrame(data).to_csv('../feed_history.csv')

if __name__ == '__main__':
    main('feed_history_videoId.csv')
  
