# %%
import re
import requests
import lxml
import pandas as pd
from bs4 import BeautifulSoup as bs
import config

# %%
netease_singers_url = r'https://music.163.com/discover/artist/cat?id=1002'

netease_singers_response = requests.get(url=netease_singers_url,
                                        params={},
                                        headers=config.HEADERS,
                                        cookies=config.COOKIES,
                                        allow_redirects=True)
# netease_singers_response.encoding = 'utf-8'
netease_singers_male = netease_singers_response.text
netease_singers_male

# %%
netease_singers_male_soup = bs(netease_singers_male, 'lxml')
print(netease_singers_male_soup.prettify())

# %%
singers_male = netease_singers_male_soup.find_all('a',
                                                  href=re.compile(r'artist\?id'),
                                                  class_='nm nm-icn f-thide s-fc0')
singers_male

# %%
singers_male[0]

# %%
singers_male_names = [singer_name.text for singer_name in singers_male]
# singers_male_names.remove('')
singers_male_names

# %%
singers_male_links = [singer_link['href'].strip() for singer_link in singers_male]
singers_male_links

# %%
len(singers_male_links) == len(singers_male_names)

# %%
df_singers_male = pd.DataFrame({
    'singer': pd.Series(singers_male_names),
    'singer_link': (r'https://music.163.com' + pd.Series(singers_male_links))
})

# %%
df_singers_male.to_csv('../data/女歌手.csv', sep=',', header=True, index=False)

# %%



