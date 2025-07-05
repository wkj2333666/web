# %%
import pandas as pd
import config
import requests
import re
import lxml
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
import swifter

# %%
src_singer = config.WORKSPACE + "data/singer_info.json"
src_song = config.WORKSPACE + "data/song_info.json"
df_singer = pd.read_json(src_singer, lines=True, orient="records")
df_song = pd.read_json(src_song, lines=True, orient="records")


# %%
def change_singer_to_dict(row: pd.Series) -> pd.Series:
    try:
        singers = []
        for singer_name in row.singers:
            new_singer_dict = {}
            new_singer_dict["singer_name"] = singer_name
            new_singer_dict["singer_id"] = (
                df_singer.loc[df_singer["singer_name"] == singer_name].iloc[0].singer_id
            )
            singers.append(new_singer_dict)
        row.singers = singers
        return row
    except IndexError:
        # set dismatched row as nan!
        print(singer_name)


# %%
def change_song_to_dict(row_singer: pd.Series) -> pd.Series:
    songs = []
    for song_id in row_singer.songs_id:
        try:
            new_song_dict = {}
            new_song_dict["song_id"] = song_id
            new_song_dict["song_name"] = (
                df_song.loc[df_song["song_id"] == song_id].iloc[0].song_name
            )
            songs.append(new_song_dict)
        except IndexError:
            # ignore dismatched song_id
            pass
    row_singer["songs"] = songs
    return row_singer


# %%
df_singer = df_singer.swifter.apply(change_song_to_dict, axis=1)

# %%
df_singer.drop(["songs_id"], axis=1, inplace=True)

# %%
df_singer.to_json(src_singer, orient="records", lines=True, force_ascii=False, mode="w")

# %%
df_song = df_song.swifter.apply(change_singer_to_dict, axis=1)

# %%
df_song.to_json(src_song, orient="records", lines=True, force_ascii=False, mode="w")
