import pandas as pd

try:
    from nltk.sentiment import SentimentIntensityAnalyzer
    nltk.data.find('vader_lexicon.zip')
except:
    import nltk
    nltk.download('vader_lexicon')

from nltk.sentiment import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()

def get_sentiment(text):
    score = sia.polarity_scores(text)['compound']
    if score <= -0.6:
        return "Negative"
    elif -0.6 < score <= -0.2:
        return "Slightly Negative"
    elif -0.2 < score <= 0.2:
        return "Neutral"
    elif 0.2 < score <= 0.6:
        return "Slightly Positive"
    else:
        return "Positive"


def sentiment(data):
    College_Infrastructure_sentiment = []
    Academics_sentiment = []
    Placements_sentiment = []
    Campus_Life_sentiment = []
    Anything_Else_sentiment = []
    text1 = data['College_Infrastructure']
    text2 = data['Academics']
    text3 = data['Placements']
    text4 = data['Campus_Life']
    text5 = data['Anything_Else']
    for i in text1:
        sentiment = get_sentiment(i)
        College_Infrastructure_sentiment.append([i,sentiment])
    for i in text2:
        sentiment = get_sentiment(i)
        Academics_sentiment.append([i,sentiment])
    for i in text3:
        sentiment = get_sentiment(i)
        Placements_sentiment.append([i,sentiment])
    for i in text4:
        sentiment = get_sentiment(i)
        Campus_Life_sentiment.append([i,sentiment])
    for i in text5:
        sentiment = get_sentiment(i)
        Anything_Else_sentiment.append([i,sentiment])

    College_Infrastructure_sentiment_df = pd.DataFrame(College_Infrastructure_sentiment,columns=['Text','Sentiment'])
    Academics_sentiment_df = pd.DataFrame(Academics_sentiment,columns=['Text','Sentiment'])
    Placements_sentiment_df = pd.DataFrame(Placements_sentiment,columns=['Text','Sentiment'])
    Campus_Life_sentiment_df = pd.DataFrame(Campus_Life_sentiment,columns=['Text','Sentiment'])
    Anything_Else_sentiment_df = pd.DataFrame(Anything_Else_sentiment,columns=['Text','Sentiment'])

    return College_Infrastructure_sentiment_df, Academics_sentiment_df, Placements_sentiment_df, Campus_Life_sentiment_df, Anything_Else_sentiment_df
