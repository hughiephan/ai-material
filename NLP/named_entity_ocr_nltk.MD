# Named Entity Recognition with Pytesseract OCR and NLTK

![image](https://github.com/hughiephan/DPL/assets/16631121/c38d4f8d-3a9c-423d-a05c-a4b82c4dec12)

## Step 1: Import libraries
```python
!apt-get install tesseract-ocr
!pip install pytesseract
!pip install gradio
!pip install svgling
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

## Step 2: Import image
```python
response = requests.get('https://www.beginner-bookkeeping.com/images/Word_Receipt_Example.jpg')
img = Image.open(io.BytesIO(response.content))
```

Output of `img`:

![image](https://www.beginner-bookkeeping.com/images/Word_Receipt_Example.jpg)

## Step 3: OCR process
```python
text = pytesseract.image_to_string(img)
```

Output of `text`:

![image](https://github.com/hughiephan/DPL/assets/16631121/87894933-7f89-4691-b30f-831278e0bff6)

## Step 4: Named-entity tagging
```python
tagged = pos_tag(word_tokenize(text))
```

POS Tagging (Parts of Speech Tagging) is a process to mark up the words in text format for a particular part of a speech based on its definition and context. NLTK `pos_tag` is implemented using PerceptronTagger which uses the averaged, structured perceptron algorithm, you can read more about it here: https://explosion.ai/blog/part-of-speech-pos-tagger-in-python

Output of `tagged`:

![image](https://github.com/hughiephan/DPL/assets/16631121/c15286e9-2218-4bbe-9475-d477cc94cabd)

List of 35 POS Tags https://www.h2kinfosys.com/blog/part-of-speech-tagging-chunking-with-nltk, here's a few examples:
- `NN` is Noun, Singular. Examples: School, Table, Pen
- `NNP` is Proper Noun, Singular. Example: Monday, Chicago, Mark
- `CD` is Cardinal Digit. Example: One, Two, Three, Forty
- `IN` is Subordinating Conjunction or Preposition. Examples: Over, Behind, Into
- `JJ` is Adjective. Examples: Beautiful, Slow, New
- `VBN` is Verb, Past Participle. Examples: Taken, Given, Gone
- `VBD` is Verb, Past Tense. Examples: Jumped, Ate, Played 

## Step 4: Chunking
```python
chunks = ne_chunk(tagged)
```

Chunking in NLP is a process to take small pieces of information and group them into large units, `ne_chunk()` function takes a list of POS-tagged tokens and returns a tree of named entities

Output of the tree `chunks`:

![image](https://github.com/hughiephan/DPL/assets/16631121/a228482a-4208-4926-b97e-850a35e663df)

Example of a Tree from NLTK, you can read more here https://www.nltk.org/howto/tree.html :

![Untitled](https://github.com/hughiephan/DPL/assets/16631121/6bf09d37-a42b-4787-a056-865664979db3)

## Step 5: Result
```python
for chunk in chunks:
    name = ''
    if type(chunk) == Tree:
        for chunk_leaf in chunk.leaves():
            name += chunk_leaf[0] + ' '
        print(chunk.label(), ':', name)
```

Prediction result:

![image](https://github.com/hughiephan/DPL/assets/16631121/390f5831-94b6-43ad-baba-24f95aa2b4d4)

## Step 6: Build demo
If you want to build an interface with Gradio, it works best on Jupyter or Google Colab Notebook. Kaggle Notebook often gets timed out when running Gradio.

```python
def predict(img):
    text = pytesseract.image_to_string(img)
    tagged = pos_tag(word_tokenize(text))
    chunks = ne_chunk(tagged)
    result = []
    for chunk in chunks:
        name = ''
        if type(chunk) == Tree:
            for chunk_leaf in chunk.leaves():
                name += chunk_leaf[0] + ' '
            result.append([chunk.label(), name])
    return result

demo = gr.Interface(
    fn=predict,
    inputs=gr.inputs.Image(type="pil"),
    outputs=["text"],
    title="Named Entity Recognition with Pytesseract OCR and ",
)

demo.queue().launch(share=True, debug=True)
```

Interface of our demo:

![image](https://github.com/hughiephan/DPL/assets/16631121/147c5546-b4a9-483f-9224-053dc0d2baa5)

## References
- https://stackoverflow.com/questions/20827741/nltk-naivebayesclassifier-training-for-sentiment-analysis
- https://www.h2kinfosys.com/blog/part-of-speech-tagging-chunking-with-nltk
- https://www.nltk.org/howto/tree.html
- https://stackoverflow.com/questions/32016545/how-does-nltk-pos-tag-work
- https://explosion.ai/blog/part-of-speech-pos-tagger-in-python
