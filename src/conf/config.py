from dataclasses import dataclass

@dataclass
class Path:
  auths: str
  log: str
  data: str

@dataclass
class Files:
  client: str
  token: str
  headers: str

@dataclass
class Params:
  root_url: str
  query: str
  time_sleep: str
  max_trials: str

@dataclass
class DataFiles:
  video_id: str
  video_info: str

@dataclass
class AuthsConfig:
  paths: Path
  files: Files
  params: Params
  data_files: DataFiles
