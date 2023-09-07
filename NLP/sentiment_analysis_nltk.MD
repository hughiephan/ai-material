# Sentiment Analysis with NLTK

## Step: Import Libraries
```python
import nltk
import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import movie_reviews
from sklearn.metrics import classification_report
```

## Step: Import and pre-process data
```python
nltk.download("movie_reviews")
nltk.download("vader_lexicon")
reviews = []
for category in movie_reviews.categories():
    for fileid in movie_reviews.fileids(category):
        review = movie_reviews.raw(fileid)
        sentiment = 'positive' if category == 'pos' else 'negative'
        reviews.append((review, sentiment))
```

## Step: Make a prediction on a review
```python
sia = SentimentIntensityAnalyzer()
sia.polarity_scores("This movie was amazing! I loved every minute of it.")
```

![image](https://github.com/hughiephan/DPL/assets/16631121/9f1f075f-2284-4e84-a179-9a93b4c17578)

## Step: Make prediction on all review dataset
```python
sentiments = []
for review, sentiment in reviews:
    sentiment_scores = sia.polarity_scores(review)
    compound_score = sentiment_scores['compound']
    if compound_score >= 0.05:
        predicted_sentiment = "positive"
    elif compound_score <= -0.05:
        predicted_sentiment = "negative"
    else:
        predicted_sentiment = "neutral"
    sentiments.append((review, sentiment, predicted_sentiment))
df = pd.DataFrame(sentiments, columns=['Review', 'Actual Sentiment', 'Predicted Sentiment'])
filtered_df = df[df['Predicted Sentiment'] != 'neutral']
actual_sentiments = filtered_df['Actual Sentiment'].tolist()
predicted_sentiments = filtered_df['Predicted Sentiment'].tolist()
report = classification_report(actual_sentiments, predicted_sentiments)
print(report)
```

![image](https://github.com/hughiephan/DPL/assets/16631121/b02997bc-f23f-4654-9418-c0043d6f4a85)

## References
- Medium Blog by Lukman Aliyu (Unveiling Sentiments in IMDb Movie Reviews with NLTK’s SentimentIntensityAnalyzer)
