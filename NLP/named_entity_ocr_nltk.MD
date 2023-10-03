# Named Entity Recognition with Pytesseract OCR and NLTK NER

## Step 1: Import libraries
```python
import pytesseract
import requests
import io
import nltk
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
from PIL import Image
```

## Step 2: Import Image
```python
response = requests.get('https://www.beginner-bookkeeping.com/images/Word_Receipt_Example.jpg')
img = Image.open(io.BytesIO(response.content))
```

![image](https://www.beginner-bookkeeping.com/images/Word_Receipt_Example.jpg)

## Step 3: OCR process
```python
sent = pytesseract.image_to_string(img)
```

![image](https://github.com/hughiephan/DPL/assets/16631121/87894933-7f89-4691-b30f-831278e0bff6)

## Step 4: NER process
```python
nltk_results = ne_chunk(pos_tag(word_tokenize(sent)))
for nltk_result in nltk_results:
    if type(nltk_result) == Tree:
        name = ''
        for nltk_result_leaf in nltk_result.leaves():
            name += nltk_result_leaf[0] + ' '
        print (nltk_result.label(), ':', name)
```

After Part-of-speech tagged:
![image](https://github.com/hughiephan/DPL/assets/16631121/c15286e9-2218-4bbe-9475-d477cc94cabd)

![image](https://github.com/hughiephan/DPL/assets/16631121/390f5831-94b6-43ad-baba-24f95aa2b4d4)

## References
- https://stackoverflow.com/questions/20827741/nltk-naivebayesclassifier-training-for-sentiment-analysis
