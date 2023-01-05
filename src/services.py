import os
import pprint
from dataclasses import dataclass

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

class BaseYouTubeModel:

  def __init__(self, TOKEN_PATH, CLIENT_FILE):

    self.api_name = 'youtube'
    self.version = 'v3'
    self.SCOPES = ["https://www.googleapis.com/auth/youtube"]
    self.creds = authenicate(self.SCOPES, CLIENT_FILE, TOKEN_PATH)
    self.service = self.build()

  def build(self):
    return build(self.api_name, self.version, credentials=self.creds)

class YouTubeDataApi(BaseYouTubeModel):

  def __init__(self, TOKEN_PATH, CLIENT_FILE):
    super().__init__(TOKEN_PATH, CLIENT_FILE)

  def get_video_with_id(self, videoId):
    '''
    This returns a youtube videos that matches that specific video id.
    '''

    return self.service.videos().list(
        part="snippet,contentDetails,statistics", id=videoId).execute()

  @staticmethod
  def get_video_data(video_response):
    video_response = video_response['items'][0]
    # return VideoData(**video_response)
    video_information = {
        'id': video_response['id'],
        'category_id': video_response['snippet']['categoryId'],
        'channel_title': video_response['snippet']['channelTitle'],
        'channel_id': video_response['snippet']['channelId'],
        'description': video_response['snippet']['description'], 
        'published_at': video_response['snippet']['publishedAt'],
        'title': video_response['snippet']['title'], 
        'views': video_response['statistics']['viewCount'],
        'comment': video_response['statistics']['commentCount'] if 'commentCount' in video_response['statistics'].keys() else 0,
        'likes': video_response['statistics']['likeCount'] if 'likeCount' in video_response['statistics'].keys() else 0
    }
    return video_information


class VideoCategory(BaseYouTubeModel):
  
  def __init__(self, TOKEN_PATH, CLIENT_FILE):
    super().__init__(TOKEN_PATH, CLIENT_FILE)

  def get_categories(self):
    '''
    Get the Youtube data categories according to youtube api.
    '''  
    response = self.service.videoCategories().list(
        part="snippet",
        regionCode="US").execute()
    return self._get_categories(response.get('items', None))

  def _get_categories(self, category_response):

    '''
    Parse through the dictionary and return the dictionary of key: id, value: title
    '''
    categories = {}
    if category_response == None:
      return categories

    for category in category_response:
      categories[int(category.get('id'))] = category.get('snippet').get('title')
    return categories
    
@dataclass
class YouTubeData:
  id: str
  channel_title: str
  category_id: str
  channel_id: str
  description: str
  published_at: str
  title: str
  views: str
  likes: str
  comment: str

@dataclass
class VideoSnippet:
  categoryId: str
  channelTitle: str
  channelId: str
  description: str
  publishedAt: str
  title: str

@dataclass
class VideoStatistics:
  viewCount: str
  likeCount: str
  commentCount: str # make options

@dataclass
class VideoData:
  id: str
  snippet: VideoSnippet
  statistics: VideoStatistics

def authenicate(SCOPES, CLIENT_FILE, TOKEN_PATH):

  creds = None
  if os.path.exists(TOKEN_PATH):
      creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

  if not creds or not creds.valid:

      if creds and creds.expired and creds.refresh_token:
          creds.refresh(Request())
      else:
          flow = InstalledAppFlow.from_client_secrets_file(
              CLIENT_FILE, SCOPES)
          creds = flow.run_local_server(port=0)

      with open(TOKEN_PATH, 'w') as token:
          token.write(creds.to_json())
  return creds
