# %%
import numpy as np
import pandas as pd
import re
import requests
import lxml
from bs4 import BeautifulSoup as bs
from tqdm import tqdm
import time
import config

# %%
sex = "女歌手"
df_singers = pd.read_csv(rf"../data/{sex}.csv")

# %%

df_songs = pd.DataFrame({"singer": [], "song_name": [], "song_link": []})
tqdm.pandas()


def get_songs(row):
    response = requests.get(
        url=row.链接, headers=config.HEADERS, params={}, cookies=config.COOKIES
    )
    soup = bs(response.text, "lxml")
    # print(soup.prettify())
    # pbar = tqdm.get_lock().get_instances()[0]
    # pbar.set_description_str(f'processing {row.歌手}')

    song_names = [
        song.text for song in soup.find_all("a", href=re.compile(r"/song\?id=\d"))
    ]
    song_links = [
        r"https://music.163.com" + song["href"]
        for song in soup.find_all("a", href=re.compile(r"/song\?id=\d"))
    ]

    global df_songs
    df_songs = pd.concat(
        [
            df_songs,
            pd.DataFrame(
                {
                    "singer": [row.歌手 for _ in range(len(song_names))],
                    "song_name": song_names,
                    "song_link": song_links,
                }
            ),
        ],
        ignore_index=True,
    )
    # return df_songs_new
    # time.sleep(2.0)


# %%
df_singers.progress_apply(get_songs, axis=1)

# %%
df_songs.to_csv(rf"../data/{sex}歌曲.csv", header=True, index=False)
