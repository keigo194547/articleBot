import urllib, urllib.request
import time
import random
import requests
from datetime import datetime, timedelta
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from datetime import datetime
import schedule,time,datetime
from xml.etree import ElementTree
import schedule
from time import sleep


search_queries = [ "cat:cs.CL","cat:cs.CV","cat:cs.LG","cat:cs.AI","cat:stat.ML"]
week_day = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
animeList = ["メイドインアビス", "SAO", "ラブライブ"]


template = """
    Title: {}
    Authors: {}
    Summary: {}
    """

# arXivで検索形式を指定
def get_arXiv_paper(getArticleValue):
    url = "http://export.arxiv.org/api/query"
    payload = {
        "search_query": getArticleValue,
        "max_results": 3,
        "sortBy": "submittedDate",
        "sortOrder": "descending"
    }   
    response = requests.get(url, params=payload)
    return response.content.decode("utf-8")

# 任意の時間で実行する関数
def task():
    # 変数の初期化
    response = None
    root = None
    entries = []
    
    # 曜日確認
    today = datetime.date.today()
    today_index = today.weekday()
    today = week_day[today_index]
    print(today)
    
    # 曜日の選択
    if today in ["Saturday","Sunday"]:
        anime = random.choice(animeList)
    # 検索する内容指定
    else:
        search_index = search_queries[today_index]
        response = get_arXiv_paper(search_index)
        root = ElementTree.fromstring(response)
        entries = root.findall("{http://www.w3.org/2005/Atom}entry")
    
    # Slackへ通知
    client = WebClient(token=Slack_BOT_APIKey)
    
    if today in ["Saturday", "Sunday"]:
        text_content = f"「{anime}は良いぞ」おじさんです"
        try:
            day_content = client.chat_postMessage(
                channel="#テスト",
                text=text_content
            )
            print(text_content)
        except SlackApiError as e:
            print("Error sending message: {}".format(e))
    else:
        text_content = f"本日は{search_index}の内容です"
        try:
            day_content = client.chat_postMessage(
                channel="#テスト",
                text=text_content
            )
            print(text_content)
        except SlackApiError as e:
            print("Error sending message: {}".format(e))
        
        # 検索する論文の内容をサーチ
        for i in range(3):
            entry = random.choice(entries)
            title = entry.find("{http://www.w3.org/2005/Atom}title").text
            authors = [author.find("{http://www.w3.org/2005/Atom}name").text for author in entry.findall("{http://www.w3.org/2005/Atom}author")]
            summary = entry.find("{http://www.w3.org/2005/Atom}summary").text
            message = template.format(title, ", ".join(authors), summary)
            try:
                response = client.chat_postMessage(
                    channel="#テスト",
                    text=message
                )
                print("Message sent: ", message)
            except SlackApiError as e:
                print("Error sending message: {}".format(e))
        

if __name__ == "__main__":
    
    Slack_BOT_APIKey = 'SlackAPI'
    
    # スケジュールにtask()関数を登録する
    schedule.every().day.at("7:00").do(task)
    
    # スケジュールの実行
    while True:
        schedule.run_pending()
        time.sleep(1)