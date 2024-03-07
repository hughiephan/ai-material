# Item-based Recommend with Cosine Similarity

## Step 1: Import libraries

```python
import pandas as pd
import numpy as np
import ast
from sklearn.metrics.pairwise import cosine_similarity
```

## Step 2: Dataset

Download H&M Personalized Fashion Recommendations dataset from `https://www.kaggle.com/competitions/h-and-m-personalized-fashion-recommendations/data`

```python
transaction = pd.read_csv('../input/h-and-m-personalized-fashion-recommendations/transactions_train.csv', nrows=100)
article = pd.read_csv('../input/h-and-m-personalized-fashion-recommendations/article.csv')
```

## Step 3: Dataframe
![image](https://github.com/hughiephan/DPL/assets/16631121/91c1a4f0-0810-4225-aab3-51cbb3a860ca)

```python
article_id_to_name = dict(zip(article['article_id'], article['prod_name']))
transaction['prod_name'] = transaction['article_id'].map(article_id_to_name)
df = transaction[['customer_id','prod_name']]
```

Output of `article_id_to_name`

![image](https://github.com/hughiephan/DPL/assets/16631121/424e5115-e3cf-4ebd-a9bf-63b33ef29f6e)


## Step 4: Item to vectors
```python
def compute_item_vectors(items):
    all_items = set()
    for sublist in items:
        all_items.update(sublist)
    all_items = sorted(list(all_items))
    vectors = []
    for sublist in items:
        vector = [1 if item in sublist else 0 for item in all_items]
        vectors.append(vector)
    return np.array(vectors), all_items
```

## Step 5: Recommend
```python
def recommend(items, input_items, num_recommendations=5):
    input_items = ast.literal_eval(input_items)
    item_vectors, all_items = compute_item_vectors(items)
    item_to_index = {item: i for i, item in enumerate(all_items)}
    index_to_item = {i: item for item, i in item_to_index.items()}
    input_indices = [item_to_index[item] for item in input_items if item in item_to_index]
    if not input_indices:
        print("None of the input items found.")
        return []
    input_vectors = item_vectors[:, input_indices]
    aggregated_vector = np.sum(input_vectors, axis=1)
    similarities = cosine_similarity([aggregated_vector], item_vectors.T)[0]
    similar_indices = similarities.argsort()[::-1]  # Sort in descending order
    similar_items = [index_to_item[idx] for idx in similar_indices if idx not in input_indices]
    return similar_items[:num_recommendations]
```

## Step 6: Prediction

```python
input_items = ['Perrie trash']
grouped_items = df.groupby('customer_id')['prod_name'].apply(list).tolist()
recommended_items = recommend(grouped_items, input_items)
print(f"Recommended items for {input_items}: {recommended_items}")
```


