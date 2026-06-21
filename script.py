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

keywords = ["税"]

file_path = "newsDB.xlsx"
data = []

for url in urls:
    try:
        feed = feedparser.parse(url)

        for entry in feed.entries:
            title = entry.get("title", "")
            summary = entry.get("summary", "")

            if any(k in title or k in summary for k in keywords):
                category = entry.get("category", "")
                link = entry.get("link", "")
                published = entry.get("published", "")

                data.append([category, title, link, published])

    except Exception as e:
        print(f"ERROR in URL {url}: {e}")

# データなしでも落とさない
if len(data) == 0:
    print("該当ニュースなし")
    df_all = pd.DataFrame(columns=["カテゴリ", "タイトル", "URL", "更新日"])
else:
    df_new = pd.DataFrame(data, columns=["カテゴリ", "タイトル", "URL", "更新日"])

    if os.path.exists(file_path):
        try:
            df_old = pd.read_excel(file_path)
            df_all = pd.concat([df_old, df_new]).drop_duplicates(subset="URL")
        except:
            df_all = df_new
    else:
        df_all = df_new

# 必ず保存する（重要）
df_all.to_excel(file_path, index=False)

print(f"取得件数: {len(data)}")
