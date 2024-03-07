# Item-based Recommend with Cosine Similarity

![image](https://github.com/hughiephan/DPL/assets/16631121/0f33463d-5877-4e3d-929e-003aceda0781)

Item-based recommendation explores the relationship between the pair of items (the user who bought Y, also bought Z). Then the similarity between item pairs can be found in different ways. One of the most common methods is to use cosine similarity. 

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

The Transaction dataframe initially includes only the customer ID and article ID, but to enhance clarity, we aim to display the product name alongside. Thus, we utilize a mapping technique, associating each transaction's article ID with its corresponding product name from a dictionary containing article IDs and their respective product names. Then, the resulting dataframe contains solely the customer ID and product names.
```python
article_id_to_name = dict(zip(article['article_id'], article['prod_name']))
transaction['prod_name'] = transaction['article_id'].map(article_id_to_name)
df = transaction[['customer_id','prod_name']]
```

Output of `article_id_to_name`

![image](https://github.com/hughiephan/DPL/assets/16631121/424e5115-e3cf-4ebd-a9bf-63b33ef29f6e)

Output of `df`

![image](https://github.com/hughiephan/DPL/assets/16631121/e3ed43a0-3067-4b5a-b4bb-465a8973e742)

## Step 4: Group items

We use `df.groupby` to categorize products that are commonly purchased together by individual customers. 

```python
group_items = df.groupby('customer_id')['prod_name'].apply(list).tolist()
```

![image](https://github.com/hughiephan/DPL/assets/16631121/e64dee94-9850-4bcb-a25f-3fdae15947df)

So basically, we will have Group 1: [Atlanta Push Body Harlow', 'Rae Push (Melbourne) 2p], Group 2: ['Inca Jumper', 'W YODA KNIT OL OFFER', 'W YODA KNIT OL OFFER', 'W YODA KNIT OL OFFER', 'Inca jumper'], and so on.

## Step 5: All unique items

Generate a set of all unique items, this will prove valuable when we construct new item vectors for existing dataset or a new query.

```python
all_items = set(df['prod_name'].unique())
```

![image](https://github.com/hughiephan/DPL/assets/16631121/7a985a82-4c1a-4946-8ced-da87343332d2)

## Step 6: Item to vectors

If the item is present then we assign a `1`, otherwise, a `0` is assigned. This process resuts in a series of vectors consisting of 0s and 1s.

```python
item_vectors = []
for sublist in group_items:
    vector = [1 if item in sublist else 0 for item in all_items]
    item_vectors.append(vector)    
item_vectors = np.array(item_vectors)
```

![image](https://github.com/hughiephan/DPL/assets/16631121/b7a3ebb7-0dba-4730-80ee-fab2226c5dd8)

## Step 7: Dictionary

Indices are beneficial when determining the appropriate placement to put a `1` (if the item exists). With these 2 functions, we can translate vectors into product names and vice versa.

```python
item_to_index = {item: i for i, item in enumerate(all_items)}
index_to_item = {i: item for item, i in item_to_index.items()}
```

Output of `item_to_index`

![image](https://github.com/hughiephan/DPL/assets/16631121/e5dc71a5-2f1c-451c-87f6-151ad68fb605)

Output of `index_to_item`

![image](https://github.com/hughiephan/DPL/assets/16631121/3e36b70e-d0c6-45b4-8459-d5c217feebe8)

## Step 8: Recommend

We first check if the input items exist in the dictionary `item_to_index`. If any input items are found, we proceed to extract their corresponding vectors from a matrix `item_vectors`. These vectors are aggregated into a single vector, and then the cosine similarity between this aggregated vector and all other item vectors is calculated. The resulting similarities are sorted in descending order to identify the most similar items. Finally, we filter out the input items from the list of similar items and selects the top five recommendations.

```python
input_items = ['Perrie trash', 'Glans tunic']
input_indices = [item_to_index[item] for item in input_items if item in item_to_index]
if not input_indices:
    print("None of the input items found.")
else:
    input_vectors = item_vectors[:, input_indices]
    aggregated_vector = np.sum(input_vectors, axis=1)
    similarities = cosine_similarity([aggregated_vector], item_vectors.T)[0]
    similar_indices = similarities.argsort()[::-1]  # Sort in descending order
    similar_items = [index_to_item[idx] for idx in similar_indices if idx not in input_indices]
    recommended_items = similar_items[:5]
    print(f"Recommended items for {input_items}: {recommended_items}")
```

Output of `input_vectors`

![image](https://github.com/hughiephan/DPL/assets/16631121/abae85d5-90b0-4dd1-9a34-0a8f424ea707)

Output of `aggregated_vector`

![image](https://github.com/hughiephan/DPL/assets/16631121/61aa8bec-c7d3-4b35-82bd-07d630e31769)

Final recommendation:

![image](https://github.com/hughiephan/DPL/assets/16631121/648e9488-72fc-4fed-9d3d-460a917ceeed)
