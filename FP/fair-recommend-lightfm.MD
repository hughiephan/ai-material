# Popularity Bias with LightFM

The model’s prediction for user u and item i is then given by the dot product of user and item representations, adjusted by user and item feature biases. If the model is recommending the same popular items to all users, the easiest solution is to set the item bias vectors to all zeros.

## Step 1: Import libraries

```python
!pip install lightfm
import numpy as np
import pandas as pd
from lightfm import LightFM
from sklearn.model_selection import train_test_split
from scipy.sparse import coo_matrix
```

## Step 2: Dataset
Download `Instacart Market Basket Analysis` from https://www.kaggle.com/datasets/psparks/instacart-market-basket-analysis
```python
df_products = pd.read_csv('/kaggle/input/instacart-market-basket-analysis/products.csv')
df_orders = pd.read_csv('/kaggle/input/instacart-market-basket-analysis/order_products__train.csv', nrows=1000)
order_product_matrix = coo_matrix((df_orders['reordered'], (df_orders['order_id'], df_orders['product_id']))).tocsr()
train_data, test_data = train_test_split(order_product_matrix, test_size=0.2)
```

## Step 3: Helper function
```python
product_id_to_name = df_products.set_index('product_id')['product_name'].to_dict()
```

## Step 4: Training
```python
model = LightFM(loss='warp')
model.fit(train_data, epochs=10)
```

## Step 5: Score

![image](https://github.com/hughiephan/DPL/assets/16631121/98fd531b-4fbf-430a-bf87-34c3c188754e)

```python
product_biases, product_embeddings = model.get_item_representations()
order_biases, order_embeddings = model.get_user_representations()
scores = ((order_embeddings @ product_embeddings.T + product_biases).T + order_biases).T
scores_without_popularity_bias = ((order_embeddings @ product_embeddings.T).T + order_biases).T
```

## Step 6: Make recommendations
```python
order_id = 1
print(f'\nTop 5 Recommendations for Order {order_id}:')
for i in np.argsort(scores[order_id])[::-1][:5]:
    product_name = product_id_to_name.get(i, f'Unknown Product {i}')
    print(f'Product: {product_name}')

print(f'\nTop 5 Recommendations for Order {order_id} (without popularity bias):')
for i in np.argsort(scores_without_bias[order_id])[::-1][:5]:
    product_name = product_id_to_name.get(i, f'Unknown Product {i}')
    print(f'Product: {product_name}')
```

![image](https://github.com/hughiephan/DPL/assets/16631121/41502cee-3717-413e-8efa-76d6c5b3a371)

## Reference
- https://www.kaggle.com/code/niyamatalmass/lightfm-hybrid-recommendation-system
- https://www.stepbystepdatascience.com/hybrid-recommender-lightfm-python
- https://www.datarevenue.com/en-blog/building-a-production-ready-recommendation-system
- https://github.com/lyst/lightfm/issues/395
