# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import wordcloud
import config
import jieba
import swifter
from stopwords import stopwords

# %%
src_file = config.WORKSPACE + 'data/song_info.json'
series_song = pd.read_json(src_file, orient='records', lines=True)['comments']
dest_file = config.WORKSPACE + 'analysis/wordcloud-add-stopwords.jpg'

# %%
frequencies = {}
def get_all_comments(comments: list):
    comment_text = ';'.join([
        comment['content'] for comment in comments
    ])
    comment_text = comment_text.replace('\n', ';')
    global frequencies
    for token in jieba.cut(comment_text):
        if token not in frequencies.keys():
            frequencies[token] = 1
        else:
            frequencies[token] += 1
        

# %%
series_song.swifter.apply(get_all_comments)

# %%
stopwords = stopwords() | {'爱心', '流泪', '亲亲', '大笑', '首歌', '大哭', '星星'}
filtered_freq = {
    key: value for key, value in frequencies.items()
    if key not in stopwords and len(key) > 1
}

# %%
font_path = '/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc'
wc = wordcloud.WordCloud(
    font_path=font_path,
    background_color='white',
    # stopwords=['我', '的', '你', '是', '了', '[', ']', ',', '.', '。', ';']
    # stopwords=['爱心', '星星', '亲亲', '可爱', '色', '流泪'],
)
wc.generate_from_frequencies(filtered_freq)

wc.to_file(dest_file)

# %%



