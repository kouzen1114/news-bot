import feedparser
import pandas as pd
import os

# RSS一覧（全カテゴリ）
urls = [
    "https://news.yahoo.co.jp/rss/categories/top-picks.xml",
    "https://news.yahoo.co.jp/rss/categories/domestic.xml",
    "https://news.yahoo.co.jp/rss/categories/world.xml",
    "https://news.yahoo.co.jp/rss/categories/business.xml",
    "https://news.yahoo.co.jp/rss/categories/it.xml",
    "https://news.yahoo.co.jp/rss/categories/science.xml",
    "https://news.yahoo.co.jp/rss/categories/local.xml",
    "https://news.yahoo.co.jp/rss/categories/entertainment.xml",
    "https://news.yahoo.co.jp/rss/categories/sports.xml"
]

# キーワード
keywords = ["税", "消費税", "増税", "課税", "税制"]

file_path = "newsDB.xlsx"
data = []

for url in urls:
    feed = feedparser.parse(url)

    for entry in feed.entries:
        title = entry.title

        if any(k in title for k in keywords):
            category = entry.get("category", "")
            link = entry.link
            published = entry.published

            data.append([category, title, link, published])

# DataFrame
df_new = pd.DataFrame(data, columns=["カテゴリ", "タイトル", "URL", "更新日"])

# 重複排除
if os.path.exists(file_path):
    df_old = pd.read_excel(file_path)
    df_all = pd.concat([df_old, df_new]).drop_duplicates(subset="URL")
else:
    df_all = df_new

# 保存
df_all.to_excel(file_path, index=False)

print(f"取得件数: {len(df_new)}")
