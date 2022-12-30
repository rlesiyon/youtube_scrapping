import pandas as pd

from services import YouTubeApi, YouTubeData

youtube = YouTubeApi()

def loading_data(filename, saveto):
  history_data = pd.read_csv(filename)
  data = []

  for videoId in history_data['video id']:
    response = youtube.get_video_with_id(videoId)
    video_info = youtube.get_video_data(response)
    data.append(video_info)

  pd.DataFrame(data).to_csv(saveto)

if __name__ == '__main__':
    loading_data('../data/youtube_search_id.csv', '../data/youtube_search.csv')
  
