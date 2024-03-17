## Item-based Cosine Similarity Recommendation


## Step 1: Get a list of all items and a list of group items

In a Notebook, run the following code with this dataset `https://www.kaggle.com/competitions/h-and-m-personalized-fashion-recommendations/data` to create a list of group items and a list of all items.

```python
import pandas as pd
transaction = pd.read_csv('../input/h-and-m-personalized-fashion-recommendations/transactions_train.csv', nrows=100)
article = pd.read_csv('../input/h-and-m-personalized-fashion-recommendations/articles.csv')
article_id_to_name = dict(zip(article['article_id'], article['prod_name']))
transaction['prod_name'] = transaction['article_id'].map(article_id_to_name)
df = transaction[['customer_id','prod_name']]
group_items = df.groupby('customer_id')['prod_name'].apply(list).tolist()
all_items = list(set(df['prod_name'].unique()))
print('Group items: \n', group_items)
print('All items: \n', all_items)
```

Output of `group_items`: 
```python
 [['Atlanta Push Body Harlow', 'Rae Push (Melbourne) 2p'], ['Inca Jumper', 'W YODA KNIT OL OFFER', 'W YODA KNIT OL OFFER', 'W YODA KNIT OL OFFER', 'Inca jumper'], ['Gyda!', 'Thomas paperbag wide', 'Fiona Wide', 'Gyda!', 'Gyda!'], ['Drew Cardigan', 'Lauper Sweater'], ['SIRPA', 'SIRPA', 'Felicia Tank', 'EDC ROMAN BLOUSE', 'EDC ROMAN BLOUSE', 'RICHIE PELATED SKIRT', 'RICHIE PELATED SKIRT', 'RICHIE PELATED SKIRT', 'RICHIE PELATED SKIRT', 'HOPPER 9.99', 'Bientot graphic tee', 'Bientot graphic tee', 'W YODA KNIT OL OFFER', 'W YODA KNIT OL OFFER', 'Linni tee', 'Linni tee', 'EDC LAURA LACE TOP', 'EDC LAURA LACE TOP', 'Wendy jersey top', 'Wendy jersey top', 'CSP Smock Top', 'CSP Smock Top', 'Linni tee', 'Linni tee', 'Jenner waist belt', 'Jenner waist belt', 'Svea Cropped Tank', 'Svea Cropped Tank', 'Fall graphic tee', 'Fall graphic tee'], ['Skinny L.W Bargain (1)'], ['Stork fancy', 'CSP Hackney tank'], ['Mini Trainer 5p Socks', 'Space 5 pkt tregging'], ['Håkan half zip CC', 'Dawn trousrer', 'TVP Henry trouser', 'Tempest TVP'], ['SC - MAJOR boot low'], ['Keyring fluff', 'Greta Shortie (Daisy Mid) 3p', 'Greta Shortie (Daisy Mid) 3p'], ['HM+ Glans tunic', 'HM+ Glans tunic', 'Glans SS', 'ED Tulip'], ['Valentino', 'A-band unicorn PU', 'HM+ Katie skatedress', '2P LS GIRLY PJ', 'Kai tunic', 'Cosy tunic', 'Lolly', 'Valentino', 'ED Madison Skinny HW', 'SORRENTO trousers', 'Glans tunic'], ['Rebecca or Delphine shirt', 'Swift Dress'], ['Janet SL-set (W)', 'Janet SL-set (W)', 'India PJ (W)', 'India PJ (W)'], ['Cindererlla'], ['Lola Lace-Up'], ['Cat Tee', 'Irma SL-set print (J)', 'Polly pencil case', 'Bracelet Tom'], ['Charlotte Brazilian Aza.Low 2p', 'Liza Superpush (Andes) 2pk', 'Henry polo. (1)', 'Mary fancy LS', 'Charlotte Brazilian Aza.Low 2p'], ['Nora Cardigan', 'Dolly hood', 'Jess oversize LS'], ['Latte slacks (1)'], ['FOG tanktop', 'MIST muscle tank', 'Boulevard TOP PRODUCT'], ['DOMINIC'], ['lennart dress'], ['Slurp long tregging'], ['Perrie trash']]
```

Output of `all_items`: 
```python
 ['ED Tulip', 'Felicia Tank', 'Bracelet Tom', 'DOMINIC', 'Bientot graphic tee', 'Inca jumper', 'Wendy jersey top', 'CSP Hackney tank', 'Glans tunic', 'SIRPA', 'Stork fancy', 'Cat Tee', 'Boulevard TOP PRODUCT', 'Lolly', 'Jess oversize LS', 'FOG tanktop', 'Slurp long tregging', 'Space 5 pkt tregging', 'HOPPER 9.99', 'Linni tee', 'Fiona Wide', 'Skinny L.W Bargain (1)', 'Lola Lace-Up', 'W YODA KNIT OL OFFER', 'RICHIE PELATED SKIRT', 'Lauper Sweater', 'Thomas paperbag wide', '2P LS GIRLY PJ', 'HM+ Katie skatedress', 'EDC LAURA LACE TOP', 'Valentino', 'Nora Cardigan', 'Cosy tunic', 'Polly pencil case', 'Irma SL-set print (J)', 'Dolly hood', 'Keyring fluff', 'ED Madison Skinny HW', 'Håkan half zip CC', 'Mary fancy LS', 'MIST muscle tank', 'Kai tunic', 'Latte slacks (1)', 'HM+ Glans tunic', 'Swift Dress', 'Janet SL-set (W)', 'Drew Cardigan', 'India PJ (W)', 'Glans SS', 'SC - MAJOR boot low', 'Greta Shortie (Daisy Mid) 3p', 'Jenner waist belt', 'Atlanta Push Body Harlow', 'Svea Cropped Tank', 'Inca Jumper', 'lennart dress', 'EDC ROMAN BLOUSE', 'SORRENTO trousers', 'Liza Superpush (Andes) 2pk', 'Mini Trainer 5p Socks', 'Rae Push (Melbourne) 2p', 'Perrie trash', 'Dawn trousrer', 'TVP Henry trouser', 'Gyda!', 'Tempest TVP', 'A-band unicorn PU', 'Cindererlla', 'Charlotte Brazilian Aza.Low 2p', 'CSP Smock Top', 'Fall graphic tee', 'Rebecca or Delphine shirt', 'Henry polo. (1)']
```

## Step 2: Create Huggingface Space

From this URL `https://huggingface.co/new-space` create a new Huggingface Space that we will deploy our backend along with our model. Input the space name as `item-based-cosine-similarity-recommend`, with the Gradio SDK, Free CPU Hardware, and set it in Public mode. The owner will automatically be your username.

![image](https://github.com/hughiephan/DPL/assets/16631121/7f4fd9d6-2da1-44fa-b001-b61961f0c5de)

## Step 3: Create new items

![image](https://github.com/hughiephan/DPL/assets/16631121/e0a9d880-2ea1-4e59-90c9-0250495271b3)

To start creating items containing our application's logic, click on `Files` -> `Add file` -> `Create new file`. We will need to create 2 files, `requirements.txt` to install libraries and `app.py` to store the logic and handle API requests.

## Step 4: Create requirements.txt

![image](https://github.com/hughiephan/DPL/assets/16631121/af24a864-c614-4773-8e20-aea885161017)

```
scikit-learn
```

## Step 5: Create app.py

![image](https://github.com/hughiephan/DPL/assets/16631121/06d35634-3db7-405f-a7be-45b40b04b9f8)

Create a new file `app.py`. We then populate the `grouped_items` and `all_items` from the previous step into the following code and keep everything else the same.

```python
import gradio as gr
import numpy as np
import ast
from sklearn.metrics.pairwise import cosine_similarity

grouped_items = <----Add contents of group_items from previous step here
all_items = <-----Add contents of all_items from previous step here

def recommend(group_items, all_items, input_items):
    input_items = ast.literal_eval(input_items) 
    item_vectors = []
    for sublist in group_items:
        vector = [1 if item in sublist else 0 for item in all_items]
        item_vectors.append(vector)    
    item_to_index = {item: i for i, item in enumerate(all_items)}
    index_to_item = {i: item for item, i in item_to_index.items()}
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

def recommend_interface(input_items):
    recommended_items = recommend(grouped_items, all_items, input_items)
    return recommended_items

interface = gr.Interface(fn=recommend, 
                     inputs=gr.Textbox(label="Input items separated by comma"), 
                     outputs="text",
                     title="Fashion Item Recommendation",
                     description="Enter a list of fashion items separated by a comma to get recommendations.")
interface.launch()
```

## Step 6: Create a frontend application

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
    var all_items = [
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
    all_items.forEach(function (item) {
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
