import feedparser
import pandas as pd
import os

# RSS URL
url = "https://news.yahoo.co.jp/rss/categories/business.xml"

# ファイル
file_path = "newsDB.xlsx"

# RSS取得
feed = feedparser.parse(url)

data = []

for entry in feed.entries:
    title = entry.title

    if "税" in title:
        category = entry.get("category", "")
        link = entry.link
        published = entry.published

        data.append([category, title, link, published])

# DataFrame化
df_new = pd.DataFrame(data, columns=["カテゴリ", "タイトル", "URL", "更新日"])

# 既存ファイルとの結合
if os.path.exists(file_path):
    df_old = pd.read_excel(file_path)
    df_all = pd.concat([df_old, df_new]).drop_duplicates(subset="URL")
else:
    df_all = df_new

# 保存
df_all.to_excel(file_path, index=False)
