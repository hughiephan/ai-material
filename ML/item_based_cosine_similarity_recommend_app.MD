## Item-based Cosine Similarity Recommendation

## Step 1: Create Huggingface Space

From this URL `https://huggingface.co/new-space` create a new Huggingface Space that we will deploy our backend along with our model. Input the space name as `item-based-cosine-similarity-recommend`, with the Gradio SDK, Free CPU Hardware, and set it in Public mode. The owner will automatically be your username.

![image](https://github.com/hughiephan/DPL/assets/16631121/7f4fd9d6-2da1-44fa-b001-b61961f0c5de)

## Step 1: Requirements.txt

```
scikit-learn
```

## Step 1: Deploy backend 
```python
import pickle
import gradio as gr
import numpy as np
import ast
from sklearn.metrics.pairwise import cosine_similarity

with open("model.pkl", "rb") as file:
    grouped_items = pickle.load(file)

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


def recommend_interface(input_items):
    recommended_items = recommend(grouped_items, input_items)
    return recommended_items

iface = gr.Interface(fn=recommend_interface, 
                     inputs=gr.Textbox(lines=5, label="Input items separated by comma"), 
                     outputs="text",
                     title="Fashion Item Recommendation",
                     description="Enter a list of fashion items separated by comma to get recommendations.")
iface.launch()
```

## Step 1: Get a list of all items
```python
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
transaction = pd.read_csv('../input/h-and-m-personalized-fashion-recommendations/transactions_train.csv', nrows=100)
article = pd.read_csv('../input/h-and-m-personalized-fashion-recommendations/articles.csv')
article_id_to_name = dict(zip(article['article_id'], article['prod_name']))
transaction['prod_name'] = transaction['article_id'].map(article_id_to_name)
df = transaction[['customer_id','prod_name']]
group_items = df.groupby('customer_id')['prod_name'].apply(list).tolist()
all_items = set(df['prod_name'].unique())
print('Group items', group_items)
print('All items', all_items)
```

![image](https://github.com/hughiephan/DPL/assets/16631121/2e5039f2-fb53-4661-a761-79765495845a)

## Step 2: Create a frontend application

![image](https://github.com/hughiephan/DPL/assets/16631121/af5981cd-b156-4abb-803c-0d098743d848)

Create an `index.html` file on your computer and copy the below code into the file to create a frontend application using HTML, CSS, and Javascript. In the `itemList`, remember to populate the list of items which we have printed out in the previous step.

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
    .app {
        position: relative;
        left: 50%;
        display: inline-block;
        max-width: 100%;
        width: 400px;
        margin: 50px auto 25px;
        padding: 20px 0;
        -webkit-transform: translateX(-50%);
        -ms-transform: translateX(-50%);
        -o-transform: translateX(-50%);
        transform: translateX(-50%);
    }
    .header {
        display: flex;
        -ms-align-items: flex-start;
        align-items: flex-start;
        padding: 30px 30px 45px;
        background: #fff;
    }
    .logo-wrapper {
        flex: 1 0 10%;
    }
    .logo {
        display: block;
        width: 75px;
        height: auto;
        margin-left: 15px;
    }
    .header-info {
        flex: 1 0 50%;
    }
    .brand,
    .clothes {
        display: block;
        font-size: 19px;
        color: #aaa;
        font-weight: 300;
    }
    .subheader-wrapper {
        background: #fff;
        padding-bottom: 20px;
    }
    .subheader {
        padding: 0 45px 0 40px;
        border-left: 5px solid #d63333;
    }
    .subheader-title {
        margin: 0 0 10px 0;
        font-size: 22px;
        font-weight: 600;
    }
    .cart {
        display: block;
        padding: 25px 30px 10px;
    }
    .cart-title {
        display: block;
        margin-top: 0;
        text-align: center;
    }
    .cart-list {
        margin: 0;
        padding: 0 15px;
        list-style: none;
    }
    .cart-item {
        display: block;
        padding-top: 20px;
        margin-bottom: 20px;
        border-top: 2px dashed #aaa;
        font-size: 18px;
    }
    .cart-item:first-child {
        border-top: 0;
    }
    .index {
        padding-right: 15px;
        color: #aaa;
        font-weight: 300;
    }
    .item-name {
        color: #aaa;
        font-weight: 300;
    }
    .footer {
        position: relative;
        padding: 30px 20px;
        border-top: 2px dashed #d63333;
        border-bottom-left-radius: 5px;
        border-bottom-right-radius: 5px;
    }
    .cart {
        background-color: #fff;
    }
    .footer {
        background-color: #fff;
    }
    .borderless {
        border: none;
        outline: none;
        font-size: 18px;
        margin-left: -4px;
    }
</style>

<html>
<link href="https://fonts.googleapis.com/css?family=Source+Sans+Pro:300,400,600" rel="stylesheet">
<div class="app">
    <div class="header">
        <div class="logo-wrapper">
            <img class="logo" src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/H%26M-Logo.svg/1280px-H%26M-Logo.svg.png">
        </div>
        <div class="header-info">
            <span class="brand">H&M Fasion</span>
            <span class="clothes">Clothes</span>
        </div>
    </div>
    <div class="subheader-wrapper">
        <div class="subheader">
            <h1 class="subheader-title">Recommendation System</h1>
            <span class="subheader-description">Using Item-based Cosine Similarities</span>
        </div>
    </div>
    <div class="cart">
        <h2 class="cart-title">Cart:</h2>
        <ul class="cart-list">
            <li class="cart-item">
                <span class="index">1</span>
                <span class="item-name">Inca Jumper</span>
            </li>
            <li class="cart-item">
                <span class="index">2</span>
                <span class="item-name">Felicia Tank</span>
            </li>
            <li class="cart-item">
                <span class="index">3</span>
                <select class="select borderless" id="itemSelect">
                </select>
            </li>
            <li class="cart-item">
            </li>
        </ul>
    </div>
    <div class="footer">
        Pick an item for recommendation
    </div>
</div>
</html>

<script type="module">
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
    var selectElement = document.getElementById('itemSelect');
    itemsList.forEach(function (item) {
        var option = document.createElement('option');
        option.value = item;
        option.textContent = item;
        selectElement.appendChild(option);
    });
    selectElement.addEventListener('change', async function () {
        var selectedItem = selectElement.value;
        var item1 = document.querySelector('.cart-item:nth-child(1) .item-name').textContent;
        var item2 = document.querySelector('.cart-item:nth-child(2) .item-name').textContent;
        var itemsArray = [item1, item2, selectedItem];
        const app = await client("https://hughiephan-item-based-cosine-similarity-recommend.hf.space");
        const result = await app.predict("/predict", [
            itemsArray,
        ]);
        const arrayResult = JSON.parse(result.data[0].replace(/'/g, '"'));
        var parsedDataContainer = document.createElement('div');
        parsedDataContainer.innerHTML = arrayResult.join(', ');
        var footerElement = document.querySelector('.footer');
        footerElement.innerHTML = 'Recommend item: ';
        footerElement.appendChild(parsedDataContainer);
    });
</script>
```
