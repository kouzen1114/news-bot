import feedparser
import pandas as pd
import os

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

keywords = ["税", "消費税", "増税", "課税", "税制"]

file_path = "newsDB.xlsx"
data = []

for url in urls:
    feed = feedparser.parse(url)

    for entry in feed.entries:
        title = entry.get("title", "")
        summary = entry.get("summary", "")

        if any(k in title or k in summary for k in keywords):

            category = entry.get("category", "")
            link = entry.get("link", "")
            published = entry.get("published", "")

            data.append([category, title, link, published])

# データなし対策
if len(data) == 0:
    print("該当ニュースなし")
    exit()

df_new = pd.DataFrame(data, columns=["カテゴリ", "タイトル", "URL", "更新日"])

if os.path.exists(file_path):
    df_old = pd.read_excel(file_path)
    df_all = pd.concat([df_old, df_new]).drop_duplicates(subset="URL")
else:
    df_all = df_new

df_all.to_excel(file_path, index=False)

print(f"取得件数: {len(df_new)}")
