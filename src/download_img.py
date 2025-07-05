import pandas as pd
import requests
import config
from tqdm import tqdm


restore_path = config.WORKSPACE + "data/song_img/"
src_file = config.WORKSPACE + "data/song_info.json"
df = pd.read_json(src_file, lines=True)


def download_img(row: pd.Series):
    response = requests.get(
        url=row.img_url, cookies=config.COOKIES, headers=config.HEADERS, params={}
    )

    with open(f"{restore_path}{row.song_id}.jpg", mode="wb") as restore_file:
        restore_file.write(response.content)


tqdm.pandas()
df.progress_apply(download_img, axis=1)
