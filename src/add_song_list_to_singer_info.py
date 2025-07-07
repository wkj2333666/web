# %%
import pandas as pd
import config
import requests
import re
import lxml
from tqdm import tqdm
from bs4 import BeautifulSoup as bs

# %%
src_file = config.WORKSPACE + "data/singer_info.json"
df = pd.read_json(src_file, orient="records", lines=True)

# %%
def add_songs(row: pd.Series) -> pd.Series:
    response = requests.get(
        url=config.SINGER_ORG_URL,
        headers=config.HEADERS,
        cookies=config.COOKIES,
        params={
            "id": row.singer_id,
        },
    )
    soup = bs(response.text, "lxml")
    id_pattern = re.compile(r"\d+$")
    songs_id = [
        int(id_pattern.search(song["href"]).group(0))
        for song in soup.find_all("a", href=re.compile(r"/song\?id=\d"))
    ]
    row["songs_id"] = songs_id
    return row


# %%
tqdm.pandas()
df = df.progress_apply(add_songs, axis=1)

# %%
df.to_json(src_file, orient="records", lines=True, mode="w", force_ascii=False)

# %%
