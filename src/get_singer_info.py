import re
import requests
import lxml
import numpy as np
import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
import config


source_file = config.WORKSPACE + 'data/raw_singers.csv'
df_singers = pd.read_csv(source_file)
restore_file = config.WORKSPACE + 'data/singer_info.json'


def get_singer_info(row):
    response = requests.get(
        url=config.SINGER_ORG_URL,
        headers=config.HEADERS,
        cookies=config.COOKIES,
        params={
            'id': row.singer_id,
        }
    )
    soup = bs(response.text, 'lxml')
    singer_abstract = soup.find('meta', property="og:abstract")['content']
    img_url = soup.find('meta', property="og:image")['content']
    
    row['singer_abstract'] = singer_abstract
    row['img_url'] = img_url
    
    return row


tqdm.pandas()
df_singers: pd.DataFrame = df_singers.progress_apply(get_singer_info, axis=1)

df_singers.to_json(
    restore_file,
    orient='records',
    force_ascii=False,
)
