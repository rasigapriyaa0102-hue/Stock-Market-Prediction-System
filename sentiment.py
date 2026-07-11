from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def get_sentiment_score(news_list):
    scores = [analyzer.polarity_scores(news)["compound"] for news in news_list]
    return sum(scores) / len(scores) if scores else 0