import urllib, urllib.request
import feedparser

searchCount = 3

def main():
    url = feedparser.parse(
        'http://export.arxiv.org/api/query?search_query=cat:stat.ML&max_results=3')
    data = url['entries']

    for num in range(searchCount):
        print(f'{num+1}番目の論文')
        author = data[num].author
        title = data[num].title
        abst = data[num].summary
        cat = data[num].category
        
        print(f'著者 : {author}')
        print(f'タイトル : {title}')
        print(f'アブスト：{abst}')
        print(f'カテゴリ：{cat}')


if __name__ == "__main__":
    main()