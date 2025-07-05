# %%
import pandas as pd
import config
import requests
import re
import lxml
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
import swifter
import time

# %%

src_file = config.WORKSPACE + 'data/song_info.json'
df_song = pd.read_json(src_file, orient='records', lines=True)

# %%
df_song.drop(['img_url', 'comments'], axis=1, inplace=True)

# %%
def to_search_version(row: pd.Series) -> pd.Series:
    singers_name = ','.join([
        singer['singer_name'] for singer in row.singers
    ])
    row['singers_name'] = singers_name

    return row

# %%
df_song = df_song.swifter.apply(to_search_version, axis=1)

# %%
df_song.drop(['singers'], inplace=True, axis=1)

# %%
dest_file = config.WORKSPACE + 'data/song_search.json'
df_song.to_json(dest_file, orient='records', mode='w', lines=True, force_ascii=False)

# %%



