# Sentiment Analysis with NLTK

Sentiment analysis is the process of analyzing text to determine if the emotional tone of the message is positive, negative, or neutral.

![image](https://github.com/hughiephan/DPL/assets/16631121/c1dd9a7b-6b82-4ae6-bb68-b26ffcf6e58b)

## Step 1: Import NLTK library, dataset and lexicon
```python
import nltk
nltk.download("movie_reviews")
nltk.download("vader_lexicon")
from nltk.corpus import movie_reviews
```

The movie_reviews dataset have 2000 text files, each of them is a review of a movie.

![image](https://github.com/hughiephan/DPL/assets/16631121/e8486247-fe86-495b-a158-80fa01ac8df8)

In the `vader_lexicon` we have the sentiment ratings from 10 independent human raters, with [–4] Extremely Negative to [4] Extremely Positive and [0] for Neutral. If the standard deviation exceed 2.5 means that the word is highly disagree between the 10 human raters. For example, the word "beautiful" is postive with 2.9, and "castatrophic" is negative with -2.2

![image](https://github.com/hughiephan/DPL/assets/16631121/4494fb77-8dad-4642-951f-774469ae37dd)

## Step 2: Import other libraries
```python
import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer
from sklearn.metrics import classification_report
```

`SentimentIntensityAnalyzer` (Vader) is an NLTK module for sentiment analysis using rule-based approach (another name is Lexicon-based approach). The words will be labeled as positive, negative or neutral with a compound score. 

![image](https://github.com/hughiephan/DPL/assets/16631121/29bda251-7dbf-4666-b204-c60384ba2305)

And `classification_report` from `sklearn.metrics` will used to measure the quality of predictions from our SentimentIntensityAnalyzer.

## Step 3: Pre-process Dataset
```python
reviews = []
for category in movie_reviews.categories():
    for fileid in movie_reviews.fileids(category):
        review = movie_reviews.raw(fileid)
        sentiment = 'positive' if category == 'pos' else 'negative'
        reviews.append((review, sentiment))
```

There are two categories `pos` for postive, and `neg` for negative. We loop through every review in both the postive and negative categories, and transform them in two a tuple of review and sentiment.

## Step 4: Make a prediction on one review
```python
sia = SentimentIntensityAnalyzer()
sia.polarity_scores("This movie was amazing! I loved every minute of it.")
```

![image](https://github.com/hughiephan/DPL/assets/16631121/9f1f075f-2284-4e84-a179-9a93b4c17578)

## Step 5: Make predictions on all reviews
The compound_score sum up the sentiment scores of each word in the sentence.

![image](https://github.com/hughiephan/DPL/assets/16631121/6d7022c1-3c01-404b-94fd-10cd0505f3be)

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
```

## Step 6: Check the report of SentimentIntensityAnalyzer on all reviews
```python
df = pd.DataFrame(sentiments, columns=['Review', 'Actual Sentiment', 'Predicted Sentiment'])
filtered_df = df[df['Predicted Sentiment'] != 'neutral']
actual_sentiments = filtered_df['Actual Sentiment'].tolist()
predicted_sentiments = filtered_df['Predicted Sentiment'].tolist()
report = classification_report(actual_sentiments, predicted_sentiments)
```

![image](https://github.com/hughiephan/DPL/assets/16631121/b02997bc-f23f-4654-9418-c0043d6f4a85)

## References
- Medium Blog by Lukman Aliyu (Unveiling Sentiments in IMDb Movie Reviews...)
- https://www.analyticsvidhya.com/blog/2022/10/sentiment-analysis-using-vader
- https://www.nltk.org/howto/sentiment.html
- https://github.com/cjhutto/vaderSentiment
- MonkeyLearn
 
