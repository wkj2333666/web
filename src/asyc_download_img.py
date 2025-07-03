import pandas as pd
import config
from tqdm import tqdm
import asyncio
import aiohttp
import aiofiles


restore_path = config.WORKSPACE + 'data/async_song_img/'
src_file = config.WORKSPACE + 'data/song_info.json'
df = pd.read_json(src_file, lines=True)


async def download_img(session, semaphore, row, pbar):
    async with semaphore:
        async with session.get(
            url=row.img_url,
            cookies=config.COOKIES,
            headers=config.HEADERS,
        ) as response:
            content = await response.read()
            async with aiofiles.open(f'{restore_path}{row.song_id}.jpg', mode='wb') as a_file:
                await a_file.write(content)
    
    pbar.update(1)
        
            
async def main():
    concurrency = 20
    semaphore = asyncio.Semaphore(concurrency)
    pbar = tqdm(total=len(df), desc='Downloading')
    
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[
            download_img(session, semaphore, row, pbar)
            for _, row in df.iterrows()
        ])
    
    pbar.close()


asyncio.run(main())