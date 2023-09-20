# Question Similarities with NLTK and Wordnet

For the questions “What is the most populous state in the USA?” and “Which state in the United States has the most people?”, their intents are identical so we want to mark them as duplicates.

![image](https://github.com/hughiephan/DPL/assets/16631121/7102673c-3e1f-41dc-a7d1-b0f4f7d29b58)

## Step 1: Import libraries
```python
import pandas as pd
import nltk
nltk.download('wordnet')
from nltk.corpus import wordnet
from sklearn.metrics import classification_report
```

## Step 2: Unzip wordnet
If you work with Wordnet in a Notebook, sometimes it prompts `Resource corpora/wordnet not found` because the `nltk.download` command downloaded the corpora successfully but could not unzip it. So let's run the command below to help unzip it:

```python
!unzip -o /usr/share/nltk_data/corpora/wordnet.zip -d /usr/share/nltk_data/corpora/
```

![image](https://github.com/hughiephan/DPL/assets/16631121/e0ddbe09-f4e3-4116-9563-25926ee4411d)

## Step 3: Import Dataset
We will be using the Quora Question-Pairs Dataset to identify duplicate questions https://www.kaggle.com/datasets/quora/question-pairs-dataset . Our simple algorithm (based on NLTK and Wordnet) will classify if the question pairs are duplicated on a small portion (100 question pairs x 2 = 200 questions) to speed up prediction time as it is costly to run.
```python
df_train = pd.read_csv('/kaggle/input/question-pairs-dataset/questions.csv')
df_train = df_train[0:101]
```

![image](https://github.com/hughiephan/DPL/assets/16631121/503d7e27-6b41-452b-87aa-6f0efd631e5d)

## Step 4: Predict 
Our naive algorithm loops through all the words in question 1 and question 2, then uses Wu Palmer Similarity to get the similarity scores between the two words. We combine all `similarity_score` into the `total_similarity` and then divide with `count` to get the `average_similarity`. We set a custom threshold of 0.4, if `average_similarity` crosses this threshold, we say that the two questions are similar, otherwise states they are duplicated.

```python
def predict(row):
    q1 = [i for i in row["question1"].lower().split()]
    q2 = [i for i in row["question2"].lower().split()]
    total_similarity = 0.0
    count = 0.0
    for word1 in q1:
        for word2 in q2:
            synset1 = wordnet.synsets(word1)
            synset2 = wordnet.synsets(word2)
            if synset1 and synset2:
                similarity_score = synset1[0].wup_similarity(synset2[0])
                if similarity_score:
                    total_similarity += similarity_score
                    count += 1
    average_similarity = total_similarity / (count + 0.0001)
    return 0 if average_similarity > 0.4 else 1
df_train["prediction"] = df_train.apply(predict, axis=1)
```

![image](https://github.com/hughiephan/DPL/assets/16631121/62ee4001-52e4-4e77-921d-3553cf214a78)

## Step 5: Show the model's accuracy
```python
true_labels = df_train["is_duplicate"]
predicted_labels = df_train["prediction"]
report = classification_report(true_labels, predicted_labels)
print(report)
```

## Step 6: 

## References
- Kaggle Notebook from SHUBH24 (Wordnet Similarity Matrix)
- Caldarola, Enrico G. & Picariello, Antonio & Rinaldi, Antonio. (2016). WordNet Exploration and Visualization in Neo4J. A Tag Cloud-Based Approach.
- Blogs RStudio (Classifying Duplicate Questions from Quora with Keras)
