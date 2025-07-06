# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
import config
import swifter
from matplotlib.font_manager import FontProperties

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
src_file = config.WORKSPACE + 'data/song_search.json'
dest_file = config.WORKSPACE + 'analysis/cover_most.csv'
df_song = pd.read_json(src_file, orient='records', lines=True)

# %%
pattern = re.compile(r'(.+)[（\(].*[）\)]')
def remove_name_suffix(row: pd.Series) -> pd.Series:
    match = re.match(pattern, row.song_name)
    if match is not None:
        row.song_name = match.group(1).strip()
    
    return row

# %%
df_song = df_song.swifter.apply(remove_name_suffix, axis=1)

# %%
df_cover = df_song.groupby(by='song_name').size().sort_values(ascending=False)

# %%
df_cover.to_csv(dest_file, header=False, index=True, encoding='utf-8')

# %%
df_cover = df_cover[df_cover > 5]

# %%
fig = plt.figure()
ax = fig.add_axes([0.1, 0.2, 0.8, 0.7])
ax.set_title('上传次数最多的歌')
bar = ax.bar(df_cover.index, df_cover.values, width=0.5)
ax.bar_label(bar)
plt.xticks(rotation=45, ha='right')
plt.show()

# %%



