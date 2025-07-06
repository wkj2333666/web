# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import config
import swifter
from matplotlib import dates

# 设置全局中文字体
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = [
    'Noto Sans CJK SC',  # Google Noto 字体
    'Source Han Sans SC', # Adobe 思源黑体
    'WenQuanYi Micro Hei', # 文泉驿微米黑
    'DejaVu Sans',
    'Arial Unicode MS'
]
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题


# %%
src_file = config.WORKSPACE + 'data/song_info.json'
df_song = pd.read_json(src_file, orient='records', lines=True)
dest_file = config.WORKSPACE + 'analysis/date-rank.csv'

# %%
df_song

# %%
def get_date(row: pd.Series) -> pd.Series:
    date = row['comments'][-1]['time'] if row['comments'] else None
    
    # exclude format such as "两天前"
    if date is not None and not date.isascii():
        date = None
    
    # 2025
    if date is not None and len(date) < 8:
        date = '2025-' + date
    
    # only reserve year and month
    # 2024-01-01 -> 2024-01
    if date is not None:
        date = date[:7]
    
    row['date'] = date
    
    return row

# %%
date_count = df_song.swifter \
                .apply(get_date, axis=1) \
                [['song_name', 'date']] \
                .dropna(axis=0) \
                .sort_values(by='date', ascending=True) \
                .groupby('date').size()
date_count.to_csv(dest_file, index=True)
# %%
date_count.index = pd.to_datetime(date_count.index)

# %%
ax = date_count.plot(figsize=(12, 6), grid=True)

# set date format 
ax.xaxis.set_major_formatter(plt.FixedFormatter(date_count.index.year.unique()))
ax.xaxis.set_major_locator(plt.MaxNLocator(len(date_count.index.year.unique())))

# plt.xticks(rotation=45)
plt.xlabel('年份')
plt.ylabel('歌曲数')
plt.title('歌曲上传年月分布')
plt.tight_layout()
plt.show()
# %%



