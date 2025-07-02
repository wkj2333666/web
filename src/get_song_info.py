# %%
import re
import requests
from bs4 import BeautifulSoup as bs
from tqdm import tqdm
import numpy as np
import pandas as pd
import lxml
import time
import config

# 加密函数
from pyncm.utils.crypto import WeapiEncrypt

# %%
df_songs = pd.read_csv("../data/raw_songs.csv")
restore_file = "../data/song_info.csv"


# %%
def get_song_info(row):
    response = requests.get(
        url=config.SONG_ORG_URL,
        headers=config.HEADERS,
        cookies=config.COOKIES,
        params={"id": row.song_id},
    )
    soup = bs(response.text, "lxml")
    song_img_url = soup.find("img", class_="j-img")["data-src"]

    # get lyrics, using EncryptFunction from pyncm
    data = {
        "id": row.song_id,
        "lv": -1,
        "tv": -1,
        "csrf_token": config.COOKIES["__csrf"],
    }
    enc_data = WeapiEncrypt(data)
    lyric_response = requests.post(
        url=config.LYRIC_URL,
        headers=config.HEADERS,
        cookies=config.COOKIES,
        data=enc_data,
    )
    raw_lyric = lyric_response.json()["lrc"]["lyric"]
    real_lyric = re.sub(r"\[\d\d\:\d\d\.\d\d\d\]", "", raw_lyric, count=0, flags=0)

    # get comments
    data = {
        "threadId": f"R_SO_4_{row.song_id}",
    }
    enc_data = WeapiEncrypt(data)
    comment_response = requests.post(
        url=config.COMMENT_URT,
        data=enc_data,
        headers=config.HEADERS,
        cookies=config.COOKIES,
    )
    comments = [
        {"name": i["user"]["nickname"], "content": i["content"], "time": i["timeStr"]}
        for i in comment_response.json()["data"]["comments"]
    ]

    row["img_url"] = song_img_url
    row["lyric"] = real_lyric
    row["comments"] = comments

    global df_songs
    if row.index % 100 == 0:
        df_songs.to_csv(restore_file, header=True, index=False)


# %%
tqdm.pandas()
df_songs.progress_apply(get_song_info, axis=1)

df_songs.to_csv(restore_file, header=True, index=False)
