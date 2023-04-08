import hydra
from hydra.core.config_store import ConfigStore
from pathlib import Path

import pandas as pd

from conf.config import AuthsConfig
from db import loading_data
from selenium_scrape import json_data, load_youtube_data_with, setup_selenium_scroller

cs = ConfigStore.instance()
cs.store(name="auths_config",node=AuthsConfig)

@hydra.main(version_base=None, config_path="conf", config_name="config")
def main(cfg: AuthsConfig):
  
  # headers_path = Path(f'{cfg.paths.auths}/{cfg.files.headers}')
  token_path = Path(f'{cfg.paths.auths}/{cfg.files.token}')
  client_path = Path(f'{cfg.paths.auths}/{cfg.files.client}')
  video_id_file = Path(f'{cfg.paths.data}/{cfg.data_files.video_id}')
  video_info_file = Path(f'{cfg.paths.data}/{cfg.data_files.video_info}')

  url = f'{cfg.params.root_url}{cfg.params.query}'
  country = cfg.params.query.split("=")[-1]
  print(f"Search youtube for the {country}")

  driver = setup_selenium_scroller(cfg.params.root_url,
                                   url , "", cfg.params.max_trials, cfg.params.time_sleep)
  
  youtube_data_list = load_youtube_data_with(driver, country)

  if youtube_data_list:
    youtube_data = pd.DataFrame(
      youtube_data_list).drop_duplicates().to_dict()
    
    pd.DataFrame(youtube_data).to_csv(video_id_file)  

  loading_data(video_id_file, video_info_file,
                token_path, client_path)
  
if __name__=='__main__':
  main()