# Fair Recommendation with LightFM

The model’s prediction for user u and item i is then given by the dot product of user and item representations, adjusted by user and item feature biases. If the model is recommending the same popular items to all users, we can try to set the item bias vectors to all zeros or apply inverse propensity weights to the features. Read more at: https://github.com/lyst/lightfm/issues/395

![image](https://github.com/hughiephan/DPL/assets/16631121/98fd531b-4fbf-430a-bf87-34c3c188754e)

## Step 1: Import libraries

```python
!pip install lightfm
import numpy as np
import pandas as pd
from lightfm import LightFM
from lightfm.evaluation import precision_at_k
from sklearn.model_selection import train_test_split
from scipy.sparse import coo_matrix, identity
```

## Step 2: 
Download `Instacart Market Basket Analysis` from https://www.kaggle.com/datasets/psparks/instacart-market-basket-analysis
```python
df_products = pd.read_csv('/kaggle/input/instacart-market-basket-analysis/products.csv')  # Assuming you have a separate file with product information
df_orders = pd.read_csv('/kaggle/input/instacart-market-basket-analysis/order_products__train.csv')
```

## Step 3: 
```python
product_id_to_name = df_products.set_index('product_id')['product_name'].to_dict()
order_product_matrix = coo_matrix((df_orders['reordered'], (df_orders['order_id'], df_orders['product_id']))).tocsr()
train_data, test_data = train_test_split(order_product_matrix, test_size=0.2, random_state=42)
user_identity = identity(train_data.shape[0])
item_identity = identity(train_data.shape[1])
```

## Step 4: Training
```python
model = LightFM(loss='warp')
model.fit(train_data, user_features=user_identity, item_features=item_identity, epochs=30, num_threads=2)
```

## Step 5: Evaluate
```python
precision = precision_at_k(model, test_data, user_features=user_identity, item_features=item_identity, k=5).mean()
print(f'Precision at k=5: {precision}')
```

## Step 6: Make prediction
```python
order_id = 1
known_positives = np.where(train_data[order_id].toarray() > 0)[0]
scores = model.predict(order_id, np.arange(train_data.shape[1]), user_features=user_identity, item_features=item_identity)
top_items = np.argsort(-scores)
print(f'\nTop 5 Recommendations for Order {order_id}:')
for i in top_items[:5]:
    if i not in known_positives:
        product_name = product_id_to_name.get(i, f'Unknown Product {i}')
        print(f'Product: {product_name}')
```

![image](https://github.com/hughiephan/DPL/assets/16631121/dc725dee-ba86-480a-b2a3-98663abcd681)

## Reference
- https://www.kaggle.com/code/niyamatalmass/lightfm-hybrid-recommendation-system
