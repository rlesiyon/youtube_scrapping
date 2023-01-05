import pandas as pd

from services import YouTubeDataApi

def loading_data(filename, saveto, client, token):
  youtube = YouTubeDataApi(client, token)
  history_data = pd.read_csv(filename)
  data = []

  for videoId in history_data['videoId']:
    response = youtube.get_video_with_id(videoId)
    video_info = youtube.get_video_data(response)
    data.append(video_info)

  pd.DataFrame(data).to_csv(saveto)

