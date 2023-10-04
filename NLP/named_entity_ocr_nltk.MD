# Named Entity Recognition with Pytesseract OCR and NLTK NER

## Step 1: Import libraries
```python
!apt-get install tesseract-ocr
import pytesseract
import requests
import io
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
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

## Step 4:
```python
tagged = pos_tag(word_tokenize(sent))
chunks = ne_chunk(tagged)
```

Part-of-speech Tagged:

![image](https://github.com/hughiephan/DPL/assets/16631121/c15286e9-2218-4bbe-9475-d477cc94cabd)

Named Entity Chunk:

![image](https://github.com/hughiephan/DPL/assets/16631121/a228482a-4208-4926-b97e-850a35e663df)

## Step 5: NER process
```python

for chunk in chunks:
    if type(chunk) == Tree:
        name = ''
        for chunk_leaf in chunk.leaves():
            name += chunk_leaf[0] + ' '
        print (chunk.label(), ':', name)
```
![image](https://github.com/hughiephan/DPL/assets/16631121/390f5831-94b6-43ad-baba-24f95aa2b4d4)

## Optional
```python
!pip install svgling
```

## References
- https://stackoverflow.com/questions/20827741/nltk-naivebayesclassifier-training-for-sentiment-analysis
