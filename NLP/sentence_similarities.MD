# Sentence Similarities with NLTK and Wordnet



## Step: Import NLTK library, Wordnet Dataset
```python
import pandas as pd
import nltk
nltk.download('wordnet')
nltk.download('stopwords')
from nltk.corpus import wordnet, stopwords
from sklearn.metrics import classification_report
```

## Step: Unzip wordnet
If you work with Wordnet in a Notebook, sometimes it prompts `Resource corpora/wordnet not found` because the `nltk.download` command downloaded the corpora successfully but could not unzip it. So let's run the command below to unzip:

```python
!unzip -o /usr/share/nltk_data/corpora/wordnet.zip -d /usr/share/nltk_data/corpora/
```
![image](https://github.com/hughiephan/DPL/assets/16631121/4cf5b187-77d1-4aba-a4f9-62992442f357)

![image](https://github.com/hughiephan/DPL/assets/16631121/e0ddbe09-f4e3-4116-9563-25926ee4411d)

## Step: Calculate the similarities between questions
We will be using the Quora Question-Pairs Dataset to identify duplicate questions https://www.kaggle.com/datasets/quora/question-pairs-dataset
```python
df_train = pd.read_csv('/kaggle/input/question-pairs-dataset/questions.csv')
df_train = df_train[0:100]
```

![image](https://github.com/hughiephan/DPL/assets/16631121/503d7e27-6b41-452b-87aa-6f0efd631e5d)

## Step: Predict 
```
def calculate_similarity(row):
    stop = set(stopwords.words('english'))
    terms1 = [i for i in row["question1"].lower().split() if i not in stop]
    terms2 = [i for i in row["question2"].lower().split() if i not in stop]
    total_similarity = 0.0
    count = 0
    for word1 in terms1:
        for word2 in terms2:
            synset1 = wordnet.synsets(word1)
            synset2 = wordnet.synsets(word2)
            if synset1 and synset2:
                similarity = synset1[0].wup_similarity(synset2[0])
                if similarity:
                    total_similarity += similarity
                    count += 1
    average_similarity = total_similarity / count if count > 0 else 0.0
    if average_similarity > 0.4:
        return 0
    else:
        return 1
df_train["prediction"] = df_train.apply(calculate_similarity, axis=1)
```

## Step: Show the model's accuracy
```python
true_labels = df_train["is_duplicate"]
predicted_labels = df_train["prediction"]
report = classification_report(true_labels, predicted_labels)
print(report)
```

## References
- Kaggle Notebook from SHUBH24 (Wordnet Similarity Matrix)
- Caldarola, Enrico G. & Picariello, Antonio & Rinaldi, Antonio. (2016). WordNet Exploration and Visualization in Neo4J. A Tag Cloud-Based Approach.

