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
import asyncio
import aiohttp
import aiofiles

# 加密函数
from pyncm.utils.crypto import WeapiEncrypt

# %%
df_songs = pd.read_csv(config.WORKSPACE + "data/raw_songs.csv")
restore_file = config.WORKSPACE + "data/async_song_info.json"


# %%
async def get_song_info(session: aiohttp.ClientSession,
                  semaphore: asyncio.Semaphore,
                  row: pd.Series,
                  pbar: tqdm) -> pd.Series:
    
    retry = 3
    async with semaphore:
        isSuccess = False
        for _ in range(retry):
            try:
                async with session.get(
                    url=config.SONG_ORG_URL,
                    headers=config.HEADERS,
                    cookies=config.COOKIES,
                    params={"id": row.song_id},
                ) as response:
                    response_text = await response.text()
                    soup = bs(response_text, "lxml")
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
                    real_lyric = re.sub(r"\[[\d\:\.]+\]", "", raw_lyric, count=0, flags=0)

                    row["img_url"] = song_img_url
                    row["lyric"] = real_lyric

                # get comments
                data = {
                    "threadId": f"R_SO_4_{row.song_id}",
                }
                enc_data = WeapiEncrypt(data)
                async with session.post(
                    url=config.COMMENT_URT,
                    data=enc_data,
                    headers=config.HEADERS,
                    cookies=config.COOKIES,
                ) as comment_response:
                    comment_json = await comment_response.json()
                    comments = [
                        {"name": i["user"]["nickname"], "content": i["content"], "time": i["timeStr"]}
                        for i in comment_json["data"]["comments"]
                    ]

                    row["comments"] = comments
                
                # success
                isSuccess = True
                break
            
            except aiohttp.client_exceptions.ClientPayloadError:
                pass
        
        if not isSuccess:
            raise RuntimeError(f'Exceeds max retry limit: {retry}.')

    pbar.set_postfix({'free': semaphore._value})
    pbar.update(1)

    return row


# %%
# tqdm.pandas()
# df_songs.progress_apply(get_song_info, axis=1)

# df_songs.to_csv(restore_file, header=True, index=False)
chunk_size = 100
total_rows = len(df_songs)
restart_from_pause = 0


async def main():
    concurrency = 20
    semaphore = asyncio.Semaphore(concurrency)
    
    for start in tqdm(range(restart_from_pause, total_rows, chunk_size), desc="Chunks"):
        end = min(start + chunk_size, total_rows)

        sub_pbar = tqdm(total=end - start, desc="Processing", leave=False)
        
        async with aiohttp.ClientSession() as session:
            result_list = await asyncio.gather(
                *[get_song_info(session, semaphore, row, sub_pbar) for _, row in df_songs.iloc[start: end].iterrows()]
            )
            
            result_df = pd.DataFrame(result_list)
            result_df.to_json(restore_file, orient="records", lines=True, mode='a', force_ascii=False)
            df_songs.iloc[start: end] = result_df


asyncio.run(main())
