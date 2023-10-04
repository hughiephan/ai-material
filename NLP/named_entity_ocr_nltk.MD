# Named Entity Recognition with Pytesseract OCR and NLTK NER

![image](https://github.com/hughiephan/DPL/assets/16631121/c38d4f8d-3a9c-423d-a05c-a4b82c4dec12)

## Step 1: Import libraries
```python
!apt-get install tesseract-ocr
!pip install pytesseract
!pip install gradio
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
def load_img(url):
    response = requests.get(url)
    img = Image.open(io.BytesIO(response.content))
```

Output of `load_img('https://www.beginner-bookkeeping.com/images/Word_Receipt_Example.jpg')`:

![image](https://www.beginner-bookkeeping.com/images/Word_Receipt_Example.jpg)

## Step 3: OCR process
```python
def ocr(img):
    return pytesseract.image_to_string(img)
```

Output of `ocr` function:

![image](https://github.com/hughiephan/DPL/assets/16631121/87894933-7f89-4691-b30f-831278e0bff6)

## Step 4:
```python
def named_entity_chunk(text):
    tagged = pos_tag(word_tokenize(text))
    chunks = ne_chunk(tagged)
    return chunks
```

Output of `pos_tag(word_tokenize(text)`:

![image](https://github.com/hughiephan/DPL/assets/16631121/c15286e9-2218-4bbe-9475-d477cc94cabd)

Output of `ne_chunk(tagged)`:

![image](https://github.com/hughiephan/DPL/assets/16631121/a228482a-4208-4926-b97e-850a35e663df)

## Step 5: Put everything together
```python
def predict(img):
    text = load_img(img)
    chunks = ocr(text)
    result = []
    for chunk in chunks:
        name = ''
        if type(chunk) == Tree:
            for chunk_leaf in chunk.leaves():
                name += chunk_leaf[0] + ' '
            result.append([chunk.label(), name])
    return result
```

## Step 6: Make prediction
```python
img = load_img('https://www.beginner-bookkeeping.com/images/Word_Receipt_Example.jpg')
predict(img)
```

![image](https://github.com/hughiephan/DPL/assets/16631121/390f5831-94b6-43ad-baba-24f95aa2b4d4)

## Step 7: Build demo
```python
demo = gr.Interface(
    fn=predict,
    inputs=gr.inputs.Image(type="pil"),
    outputs=["text"],
    title="Named Entity Recognition with Pytesseract OCR and ",
)

demo.queue().launch(share=True, debug=True)
```

![image](https://github.com/hughiephan/DPL/assets/16631121/147c5546-b4a9-483f-9224-053dc0d2baa5)

## Optional
```python
!pip install svgling
```

## References
- https://stackoverflow.com/questions/20827741/nltk-naivebayesclassifier-training-for-sentiment-analysis
