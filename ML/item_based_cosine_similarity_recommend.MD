# Item-based Recommend with Cosine Similarity

![image](https://github.com/hughiephan/DPL/assets/16631121/496e4cb6-6245-422c-92ca-87934b14757c)

## Step 1: Import libraries

```python
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
```

## Step 2: Dataset

Download H&M Personalized Fashion Recommendations dataset from `https://www.kaggle.com/competitions/h-and-m-personalized-fashion-recommendations/data`

```python
transaction = pd.read_csv('../input/h-and-m-personalized-fashion-recommendations/transactions_train.csv', nrows=100)
article = pd.read_csv('../input/h-and-m-personalized-fashion-recommendations/articles.csv')
```

## Step 3: Dataframe

```python
article_id_to_name = dict(zip(article['article_id'], article['prod_name']))
transaction['prod_name'] = transaction['article_id'].map(article_id_to_name)
df = transaction[['customer_id','prod_name']]
```

Output of `article_id_to_name`

![image](https://github.com/hughiephan/DPL/assets/16631121/424e5115-e3cf-4ebd-a9bf-63b33ef29f6e)

## Step 4: Group items

```python
group_items = df.groupby('customer_id')['prod_name'].apply(list).tolist()
```

Group 1: [Atlanta Push Body Harlow', 'Rae Push (Melbourne) 2p], Group 2: ['Inca Jumper', 'W YODA KNIT OL OFFER', 'W YODA KNIT OL OFFER', 'W YODA KNIT OL OFFER', 'Inca jumper'],...

![image](https://github.com/hughiephan/DPL/assets/16631121/e64dee94-9850-4bcb-a25f-3fdae15947df)

## Step 5: All unique items

```python
all_items = set(df['prod_name'].unique())
```

![image](https://github.com/hughiephan/DPL/assets/16631121/7a985a82-4c1a-4946-8ced-da87343332d2)

## Step 6: Item to vectors
```python
item_vectors = []
for sublist in group_items:
    vector = [1 if item in sublist else 0 for item in all_items]
    item_vectors.append(vector)    
item_vectors = np.array(item_vectors)
```

![image](https://github.com/hughiephan/DPL/assets/16631121/b7a3ebb7-0dba-4730-80ee-fab2226c5dd8)

## Step 7: Recommend
```python
item_to_index = {item: i for i, item in enumerate(all_items)}
index_to_item = {i: item for item, i in item_to_index.items()}
input_items = ['Perrie trash']
input_indices = [item_to_index[item] for item in input_items if item in item_to_index]
if not input_indices:
    print("None of the input items found.")
else:
    num_recommendations = 5
    input_vectors = item_vectors[:, input_indices]
    aggregated_vector = np.sum(input_vectors, axis=1)
    similarities = cosine_similarity([aggregated_vector], item_vectors.T)[0]
    similar_indices = similarities.argsort()[::-1]  # Sort in descending order
    similar_items = [index_to_item[idx] for idx in similar_indices if idx not in input_indices]
    recommended_items = similar_items[:num_recommendations]
    print(f"Recommended items for {input_items}: {recommended_items}")
```
