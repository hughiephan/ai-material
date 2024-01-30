# Fair Recommendation with LightFM

The model’s prediction for user u and item i is then given by the dot product of user and item representations, adjusted by user and item feature biases. If the model is recommending the same popular items to all users, we can try to set the item bias vectors to all zeros or apply inverse propensity weights to the features. Read more at: https://github.com/lyst/lightfm/issues/395

![image](https://github.com/hughiephan/DPL/assets/16631121/98fd531b-4fbf-430a-bf87-34c3c188754e)

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
```

## Step 3: Matrix
```python
product_id_to_name = df_products.set_index('product_id')['product_name'].to_dict()
order_product_matrix = coo_matrix((df_orders['reordered'], (df_orders['order_id'], df_orders['product_id']))).tocsr()
train_data, test_data = train_test_split(order_product_matrix, test_size=0.2, random_state=42)
```

## Step 4: Training
```python
model = LightFM(loss='warp')
model.fit(train_data, epochs=10)
```

## Step 5: Manual score
```python
item_biases, item_embeddings = model.get_item_representations()
user_biases, user_embeddings = model.get_user_representations()
manual_scores = ((user_embeddings @ item_embeddings.T + item_biases).T + user_biases).T
```

## Step 6: Make prediction
```python
top_n = 5
order_id = 1
top_items_for_order = np.argsort(manual_scores[order_id])[::-1][:top_n]
top_item_names = [product_id_to_name[item_id] for item_id in top_items_for_order]
print(f"Order {order_id} recommendation: {top_item_names}")
```

![image](https://github.com/hughiephan/DPL/assets/16631121/dc725dee-ba86-480a-b2a3-98663abcd681)

## Reference
- https://www.kaggle.com/code/niyamatalmass/lightfm-hybrid-recommendation-system
- https://www.stepbystepdatascience.com/hybrid-recommender-lightfm-python
- https://www.datarevenue.com/en-blog/building-a-production-ready-recommendation-system
