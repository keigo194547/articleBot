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
from xml.etree import ElementTree


search_queries = [ "cat:cs.CL","cat:cs.CV","cat:cs.LG","cat:cs.AI","cat:stat.ML"]

template = """
    Title: {}
    Authors: {}
    Summary: {}
    """


def get_arXive_paper(getArticleValue):
    url = "http://export.arxiv.org/api/query"
    payload = {
        "search_query": getArticleValue,
        "max_results": 3,
        "sortBy": "submittedDate",
        "sortOrder": "descending"
    }
    
    response = requests.get(url, params=payload)
    return response.content.decode("utf-8")

if __name__ == "__main__":
    
    
    Slack_BOT_APIKey = 'yourAPI'
    
    search_queries = search_queries[1]
    response = get_arXive_paper(search_queries)
    root = ElementTree.fromstring(response)
    entries = root.findall("{http://www.w3.org/2005/Atom}entry")
    
    for i in range(3):
        entry = random.choice(entries)
        title = entry.find("{http://www.w3.org/2005/Atom}title").text
        authors = [author.find("{http://www.w3.org/2005/Atom}name").text for author in entry.findall("{http://www.w3.org/2005/Atom}author")]
        summary = entry.find("{http://www.w3.org/2005/Atom}summary").text
        message = template.format(title, ", ".join(authors), summary)
        
        client = WebClient(token=Slack_BOT_APIKey)
        try:
            response = client.chat_postMessage(
                channel="#テスト",
                text=message
            )
            print("Message sent: ", message)
        except SlackApiError as e:
            print("Error sending message: {}".format(e))

