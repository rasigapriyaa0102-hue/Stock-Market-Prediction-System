import requests

API_KEY = "YOUR_API_KEY"

def get_news(stock):

    url = f"https://newsapi.org/v2/everything?q={stock}&apiKey={API_KEY}&language=en"

    response = requests.get(url)
    data = response.json()

    articles = data.get("articles", [])

    news_list = []

    for article in articles[:10]:   # top 10 news
        title = article["title"]
        news_list.append(title)

    return news_list