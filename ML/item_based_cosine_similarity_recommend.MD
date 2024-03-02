```python
!pip install gradio
import pickle
import pandas as pd
import cv2, matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import gradio as gr
from os.path import exists
from sklearn.metrics.pairwise import cosine_similarity
```

```python
df = pd.read_csv('../input/h-and-m-personalized-fashion-recommendations/transactions_train.csv', nrows=100)
articles_df = pd.read_csv('../input/h-and-m-personalized-fashion-recommendations/articles.csv')
article_id_to_name = dict(zip(articles_df['article_id'], articles_df['prod_name']))
df['prod_name'] = df['article_id'].map(article_id_to_name)
df = df[['customer_id','prod_name']]
grouped_items = df.groupby('customer_id')['prod_name'].apply(list).tolist()
unique_prod_names = df['prod_name'].unique().tolist()
print(unique_prod_names)
```

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

def recommend(items, input_items, num_recommendations=5):
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

grouped_items = df.groupby('customer_id')['prod_name'].apply(list).tolist()
```

```python
input_items = ['Perrie trash']
recommended_items = recommend(grouped_items, input_items)
print(f"Recommended items for {input_items}: {recommended_items}")
```

## Save model

```python
with open("model.pkl", "wb") as file:
    pickle.dump((grouped_items, recommend), file)
```

## Step: Open model
```python
with open("model.pkl", "rb") as file:
    grouped_items, recommend = pickle.load(file)
```

## Frontend

```html
<style>
    html,
    body {
        height: 100%;
        width: 100%;
        margin: 0;
        padding: 0;

        background-color: #f7f7f7;
        font-family: "Source Sans Pro", "Helvetica", sans-serif;
        letter-spacing: 1.5px;
    }

    .paypal {
        position: relative;
        left: 50%;
        display: inline-block;
        max-width: 100%;
        width: auto;
        margin: 50px auto 25px;
        padding: 20px 0;
        clear: both;
        -webkit-transform: translateX(-50%);
        -ms-transform: translateX(-50%);
        -o-transform: translateX(-50%);
        transform: translateX(-50%);
    }

    .paypal__header {
        display: flex;
        -ms-align-items: flex-start;
        align-items: flex-start;

        padding: 30px 30px 45px;
        background: #fff;
        border-top-right-radius: 5px;
        border-top-left-radius: 5px;
    }

    .paypal__logo-wrapper {
        flex: 1 0 40%;
    }

    .paypal__logo {
        display: block;
        width: 75px;
        height: auto;
        margin-left: 15px;
    }

    .paypal__header-info {
        flex: 1 0 50%;
    }

    .paypal__date,
    .paypal__ref {
        display: block;
        font-size: 19px;
        color: #aaa;
        font-weight: 300;
    }

    .paypal__date {
        margin-bottom: 5px;
    }

    .paypal__subheader-wrapper {
        background: #fff;
        padding-bottom: 20px;
    }

    .paypal__subheader {
        padding: 0 45px 0 40px;
        border-left: 5px solid #d63333;
    }

    .paypal__username {
        margin: 0 0 10px 0;
        font-size: 22px;
        font-weight: 600;
    }

    .paypal__help-text {
        color: #aaa;
        font-weight: 300;
    }

    .paypal__cart {
        display: block;
        padding: 25px 30px 10px;
    }

    .paypal__cart-title {
        display: block;
        margin-top: 0;
        text-align: center;
    }

    .paypal__cart-list {
        margin: 0;
        padding: 0 15px;
        list-style: none;
    }

    .paypal__cart-item {
        display: block;
        padding-top: 20px;
        margin-bottom: 20px;
        border-top: 2px dashed #aaa;
        font-size: 18px;
    }

    .paypal__cart-item:first-child {
        border-top: 0;
    }

    .paypal__index {
        padding-right: 15px;
        color: #aaa;
        font-weight: 300;
    }

    .paypal__item-name {
        color: #aaa;
        font-weight: 300;
    }

    .paypal__item-price {
        float: right;
        letter-spacing: 1px;
    }

    .paypal__cart-total {
        font-size: 20px;
        text-transform: uppercase;
    }

    .paypal__footer {
        position: relative;
        padding: 30px 20px;
        border-top: 2px dashed #d63333;

        border-bottom-left-radius: 5px;
        border-bottom-right-radius: 5px;
    }

    .paypal__footer::before,
    .paypal__footer::after {
        content: '';
        position: absolute;
        top: 0;
        border: 4px solid transparent;
    }

    .paypal__footer::before {
        margin-top: -5px;
        left: 0;
        border-left: 7px solid #d63333;
    }

    .paypal__footer::after {
        margin-top: -5px;
        right: 0;
        border-right: 7px solid #d63333;
    }

    .paypal__barcode {
        display: block;
        margin: 0 auto;
        max-width: 300px;
        height: auto;
    }

    .paypal__subheader {
        opacity: 100;
    }

    .paypal__cart {
        background-color: #fff;
    }

    .paypal__footer {
        background-color: #fff;
    }

    .paypal__cart-title {
        opacity: 100;
    }

    .paypal__cart-item {
        opacity: 100;
    }

    .paypal__cart-item:nth-child(2) {
        animation-delay: 2.9s;
    }

    .paypal__cart-item:nth-child(3) {
        animation-delay: 3.05s;
    }

    .paypal__cart-item:nth-child(4) {
        animation-delay: 3.2s;
    }

    .borderless {
        border: none;
        outline: none;
        font-size: 18px;
        margin-left: -4px;
    }
</style>

<html>

<head>
    <meta charset="utf-8">
    <title>Recommendation System</title>
    <link href="https://fonts.googleapis.com/css?family=Source+Sans+Pro:300,400,600" rel="stylesheet">
</head>

<body>

    <div class="paypal">

        <div class="paypal__header">
            <div class="paypal__logo-wrapper">
                <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/H%26M-Logo.svg/1280px-H%26M-Logo.svg.png"
                    alt="Paypal" class="paypal__logo">
            </div>

            <div class="paypal__header-info">
                <span class="paypal__date">H&M Fasion</span>
                <span class="paypal__ref">Clothes</span>
            </div>
        </div>

        <div class="paypal__subheader-wrapper">
            <div class="paypal__subheader">
                <h1 class="paypal__username">Recommendation System</h1>
                <span class="paypal__help-text">Using Item-based Cosine Similarities</span>
            </div>
        </div>

        <div class="paypal__cart">
            <h2 class="paypal__cart-title">Cart:</h2>

            <ul class="paypal__cart-list">
                <li class="paypal__cart-item">
                    <span class="paypal__index">1</span>
                    <span class="paypal__item-name">Inca Jumper</span>
                </li>

                <li class="paypal__cart-item">
                    <span class="paypal__index">2</span>
                    <span class="paypal__item-name">Felicia Tank</span>
                </li>

                <li class="paypal__cart-item">
                    <span class="paypal__index">3</span>
                    <select class="paypal__select borderless" id="itemSelect">
                    </select>
                </li>

                <li class="paypal__cart-item">
                </li>
            </ul>
        </div>

        <div class="paypal__footer">
            Recommend item
        </div>
    </div>

</body>

</html>

<script>
    import { client } from "https://cdn.jsdelivr.net/npm/@gradio/client@0.12.0/dist/index.min.js";

    var itemsList = [
        'Atlanta Push Body Harlow', 'Rae Push (Melbourne) 2p', 'Inca Jumper', 'W YODA KNIT OL OFFER', 'Inca jumper',
        'Gyda!', 'Thomas paperbag wide', 'Fiona Wide', 'Drew Cardigan', 'Lauper Sweater', 'SIRPA', 'Felicia Tank',
        'EDC ROMAN BLOUSE', 'RICHIE PELATED SKIRT', 'HOPPER 9.99', 'Bientot graphic tee', 'Linni tee', 'EDC LAURA LACE TOP',
        'Wendy jersey top', 'CSP Smock Top', 'Jenner waist belt', 'Svea Cropped Tank', 'Fall graphic tee',
        'Skinny L.W Bargain (1)', 'Stork fancy', 'CSP Hackney tank', 'Mini Trainer 5p Socks', 'Space 5 pkt tregging',
        'Håkan half zip CC', 'Dawn trousrer', 'TVP Henry trouser', 'Tempest TVP', 'SC - MAJOR boot low', 'Keyring fluff',
        'Greta Shortie (Daisy Mid) 3p', 'HM+ Glans tunic', 'Glans SS', 'ED Tulip', 'Valentino', 'A-band unicorn PU',
        'HM+ Katie skatedress', '2P LS GIRLY PJ', 'Kai tunic', 'Cosy tunic', 'Lolly', 'ED Madison Skinny HW', 'SORRENTO trousers',
        'Glans tunic', 'Rebecca or Delphine shirt', 'Swift Dress', 'Janet SL-set (W)', 'India PJ (W)', 'Cindererlla',
        'Lola Lace-Up', 'Cat Tee', 'Irma SL-set print (J)', 'Polly pencil case', 'Bracelet Tom', 'Charlotte Brazilian Aza.Low 2p',
        'Liza Superpush (Andes) 2pk', 'Henry polo. (1)', 'Mary fancy LS', 'Nora Cardigan', 'Dolly hood', 'Jess oversize LS',
        'Latte slacks (1)', 'FOG tanktop', 'MIST muscle tank', 'Boulevard TOP PRODUCT', 'DOMINIC', 'lennart dress',
        'Slurp long tregging', 'Perrie trash'
    ];

    // Get the select element
    var selectElement = document.getElementById('itemSelect');

    // Add options to the select element
    itemsList.forEach(function (item) {
        var option = document.createElement('option');
        option.value = item;
        option.textContent = item;
        selectElement.appendChild(option);
    });

    selectElement.addEventListener('change', async function () {
        var selectedItem = selectElement.value;
        var item1 = document.querySelector('.paypal__cart-item:nth-child(1) .paypal__item-name').textContent;
        var item2 = document.querySelector('.paypal__cart-item:nth-child(2) .paypal__item-name').textContent;
        var itemsArray = [item1, item2, selectedItem];

        const app = await client("https://hughiephan-rnn-reviewbot.hf.space");
        const result = await app.predict("/predict", [
            itemsArray,
        ]);
    });
</script>
```

![image](https://github.com/hughiephan/DPL/assets/16631121/c524c0dc-006e-4c84-989c-d83562b6b982)

## Step: app.py
```
import pickle

with open("model.pkl", "rb") as file:
    grouped_items, recommend = pickle.load(file)

def recommend_interface(input_items):
    recommended_items = recommend(grouped_items, input_items)
    return recommended_items

iface = gr.Interface(fn=recommend_interface, 
                     inputs=gr.inputs.Textbox(lines=5, label="Input items separated by comma"), 
                     outputs="text",
                     title="Fashion Item Recommendation",
                     description="Enter a list of fashion items separated by comma to get recommendations.")
iface.launch()
```
