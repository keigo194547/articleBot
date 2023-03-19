import urllib, urllib.request
import feedparser
import os
import time
import random
import requests
from datetime import datetime, timedelta
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from datetime import datetime
import schedule,time,datetime

# テスト用の日時を設定する
test_date = schedule.every().day.at("10:00")

Slack_BOT_APIKey = "xoxb-3170042464704-4991891524720-hlb6bldEJkVUauc0BokooZrF"

arxiv_APIKey = 'http://export.arxiv.org/api/query'

Search_Queries = [ "cat:cs.CL","cat:cs.CV","cat:cs.LG","cat:cs.AI","cat:stat.ML"]

# 通知する曜日
NOTIFY_DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday"]

# 時間帯の設定（UTC時間）
POST_TIME = schedule.every().day.at("10:00")

# Slackクライアントの初期化
client = WebClient(token=Slack_BOT_APIKey)


# arXivから論文を取得する関数
def fetch_arxiv_papers(search_query):
    url = "http://export.arxiv.org/api/query"
    payload = {
        "search_query": search_query,
        "max_results": 1,
        "sortBy": "submittedDate",
        "sortOrder": "descending"
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    response = requests.get(url, params=payload, headers=headers)
    return response.content.decode("utf-8")

# Slackに通知する関数
def notify_slack(paper_title, paper_url):
    message = f"arXivから論文が届きました！\n{paper_title}\n{paper_url}"
    try:
        response = client.chat_postMessage(channel="#general", text=message)
        print("通知が送信されました:", response["ts"])
    except SlackApiError as e:
        print("通知の送信に失敗しました:", e)
        
# メイン処理
if __name__ == "__main__":
    
    
    # スクリプトを実行する
    if test_date:
        notify_slack(Search_Queries, Slack_BOT_APIKey)

    
    while True:
        # 現在の日時と曜日を取得
        now = date time.now()
        now_day = now.strftime("%A").lower()
        # 指定した曜日と一致する場合のみ処理を実行
        if now_day in NOTIFY_DAYS:
            # 指定した時間帯に処理を実行
            if now.hour in POST_TIME:
                # ランダムに検索クエリを選択
                search_query = random.choice(Search_Queries)
                # arXivから論文を取得
                papers_xml = fetch_arxiv_papers(search_query)
                paper_title = papers_xml.split("<title>")[1].split("</title>")[0]
                paper_url = papers_xml.split
                
                # Slackに通知
                notify_slack(paper_title, paper_url)
        # 次の処理までの時間を計算
        next_hour = (now + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
        sleep_seconds = (next_hour - now).total_seconds()
        print(f"{now}に処理を実行しました。次の処理まで{sleep_seconds}秒待機します。")
        time.sleep(sleep_seconds)        
