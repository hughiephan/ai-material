# Question Similarities with NLTK and Wordnet

For the questions “What is the most populous state in the USA?” and “Which state in the United States has the most people?”, their intents are identical so we want to mark them as `duplicated`.

But for the questions below, question 1 mentions a particular country India while question 2 asks a more general question. So we want to mark these as `different`. 
![image](https://github.com/hughiephan/DPL/assets/16631121/b42f6acd-4969-4d51-b62f-f50ffe710b0f)

## Step 1: Import libraries
```python
!pip install gradio
import pandas as pd
import nltk
import gradio as gr
nltk.download('wordnet')
from nltk.corpus import wordnet
from sklearn.metrics import classification_report
```

## Step 2: Unzip wordnet
If you work with Wordnet in a Notebook, sometimes it prompts `Resource corpora/wordnet not found` because the `nltk.download` command downloaded the corpora successfully but could not unzip it. So let's run the command below to help unzip it:

```python
!unzip -o /usr/share/nltk_data/corpora/wordnet.zip -d /usr/share/nltk_data/corpora/
```

Visualization of Wordnet Corpus for the word `temperature`
![image](https://github.com/hughiephan/DPL/assets/16631121/e0ddbe09-f4e3-4116-9563-25926ee4411d)

Example of hypernym: `Arm` is a kind of `Limb`, `Leg` is a kind of `Limb`. So in this case `Arm` and `Leg` are the hyponyms and `Limb` is the hypernym

Example of antonym (opposite words): `Hot` is the antonym of `Cold`

Example of synonym (similar words): `Cold` is the synonym of `Icy`

## Step 3: Import Dataset
We will be using the Quora Question-Pairs Dataset to identify duplicate questions https://www.kaggle.com/datasets/quora/question-pairs-dataset. Our simple algorithm (based on NLTK and Wordnet) will classify if the question pairs are duplicated on a small portion (100 question pairs x 2 = 200 questions) to speed up prediction time as it is costly to run.
```python
df_train = pd.read_csv('/kaggle/input/question-pairs-dataset/questions.csv')
df_train = df_train[0:100]
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

Visualization of our simple approach
![image](https://github.com/hughiephan/DPL/assets/16631121/62ee4001-52e4-4e77-921d-3553cf214a78)

Here is the formula for Wu-Palmer Similarity

![image](https://github.com/hughiephan/DPL/assets/16631121/ab5ceed1-189b-48d4-a8da-193a791c40b3)

For example, `LCS(Boat, Car)` is `Vehicle`, with a depth of 1 (calculated from the root of the tree). Then we have `depth(Boat)` is 2, and `depth(Car)` is 3. Substitute all into the Wu-Palmer formula, we will finally get the Wu-Palmer Similarity score 

![image](https://github.com/hughiephan/DPL/assets/16631121/f86afa60-711c-418d-b23b-1d7e90d937d3)


## Step 5: Show the model's accuracy

```python
true_labels = df_train["is_duplicate"]
predicted_labels = df_train["prediction"]
report = classification_report(true_labels, predicted_labels)
print(report)
```

Accuracy is 36% from 100 question pairs

![image](https://github.com/hughiephan/DPL/assets/16631121/588ed513-ea67-465e-ad05-c3a2a286ece6)

## Step 6: Build a Demo
Re-write our predict function a bit to accept two questions as input

```python
def predict(question1, question2):
    total_similarity = 0.0
    count = 0.0
    for word1 in question1:
        for word2 in question2:
            synset1 = wordnet.synsets(word1)
            synset2 = wordnet.synsets(word2)
            if synset1 and synset2:
                similarity_score = synset1[0].wup_similarity(synset2[0])
                if similarity_score:
                    total_similarity += similarity_score
                    count += 1
    average_similarity = total_similarity / (count + 0.0001)
    return 'Questions are different' if average_similarity > 0.4 else 'Questions are duplicated'

demo = gr.Interface(
    fn=predict,
    inputs=["text", "text"],
    outputs=["text"],
    title="Check questions different or duplicated",
)

demo.queue().launch(share=True)
```

Interface of our demo

![image](https://github.com/hughiephan/DPL/assets/16631121/a49e680e-5d3b-4212-8866-e816f8cb2e86)

## Exercise
Our simple approach accuracy is low. Can we improve the accuracy using `synonyms` and `antonyms`?
```python
for syn in wordnet.synsets("hello"):
	for l in syn.lemmas():
		synonyms.append(l.name())
		if l.antonyms():
            antonyms.append(l.antonyms()[0].name())
print(set(synonyms))
print(set(antonyms))
```

Apply pre_process techniques (stopwords, remove special characters,...)
```python
from nltk.corpus import stopwords
stop = set(stopwords.words('english'))
sentence = 'What is the most populous state in the USA?'
def pre_process(sentence):
    return [i for i in sentence.lower().split() if i not in stop]
```

## References
- Kaggle Notebook from SHUBH24 (Wordnet Similarity Matrix)
- Caldarola, Enrico G. & Picariello, Antonio & Rinaldi, Antonio. (2016). WordNet Exploration and Visualization in Neo4J. A Tag Cloud-Based Approach.
- Blogs RStudio (Classifying Duplicate Questions from Quora with Keras)
- Kavita Ganesan (Demystifying Nouns in Wordnet)
- https://stackoverflow.com/questions/18629469/what-is-least-common-subsumer-and-how-to-compute-it
- https://www.geeksforgeeks.org/nlp-wupalmer-wordnet-similarity/
