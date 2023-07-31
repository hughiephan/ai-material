# ChatBot for Review IMDB Comments

A Web Chatbot to review IMDB Comments

## Prerequisites
- Python3 https://phoenixnap.com/kb/how-to-install-python-3-windows
- Pip

![ReviewBot](https://github.com/hughiephan/DPL/assets/16631121/68e7a8bf-5e7f-4ae2-b220-0444a92cbe72)

## Step 1: Build and train our model
We use `tfds` to load imdb reviews and their sentiment labels (positive = 1 or negative = 0). Then apply `Tokenizer.fit_on_texts` to create the word index (e.x 'cat':0, 'dog': 1, 'coffee': 2,...). After that, we pad the sequence to be the same size 120. Then we train the embedding layer (vectorize) along with RNN layer and output a prediction for the review.

```
import pickle
import warnings 
warnings.filterwarnings('ignore')
import numpy as np
import tensorflow as tf
import tensorflow_datasets as tfds
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

imdb = tfds.load("imdb_reviews", as_supervised=True) # Get a tuple (features, label)
train_data, test_data = imdb['train'], imdb['test']
training_sentences = []
training_labels = []
testing_sentences = []
testing_labels = []
for s,l in train_data:
    training_sentences.append(str(s.numpy()))
    training_labels.append(l.numpy())
for s,l in test_data:
    testing_sentences.append(str(s.numpy()))
    testing_labels.append(l.numpy())
training_labels_final = np.array(training_labels)
testing_labels_final = np.array(testing_labels)
tokenizer = Tokenizer(num_words = 10000, oov_token="")
tokenizer.fit_on_texts(training_sentences)
sequences = tokenizer.texts_to_sequences(training_sentences)
padded = pad_sequences(sequences, maxlen=120, truncating='post') # A maximum length of 120 words will be used for each piece of text,  trunc_type is set to be ‘post’ means the text will be truncated at the end
testing_sequences = tokenizer.texts_to_sequences(testing_sentences)
testing_padded = pad_sequences(testing_sequences, maxlen=120)
vocab_size = 10000 # 10000 unique words will be used for this model
embedding_dim= 16 # A vector of size 16 will be representing each word
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(vocab_size, embedding_dim, input_length=120),
    tf.keras.layers.SimpleRNN(32),
    tf.keras.layers.Dense(10, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])
model.summary()
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
history = model.fit(padded, training_labels_final, epochs=5, validation_data = (testing_padded, testing_labels_final))
```

## Step 2: Save the model and Tokenizer to local storage
Keras saves models in .h5 format as it can easily store the weights and model configuration in a single file. We also use `pickle` library to save the word index (built based on the training dataset) to local storage, `tokenizer` is important for tranforming the user's input into sequence, which can then be fed into RNN model. 

If you use `Kaggle Notebook`, press on the Download button in the output section to download these 2 files to your computer.

```
model.save('model.h5')
with open('tokenizer.pickle', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
```

![image](https://github.com/hughiephan/DPL/assets/16631121/4cc75cb3-73e2-45d8-9071-30080241ba1e)

## Step 3: Setup folder structure
Create a new folder `ReviewBot` with these empty files:
- app.py
- index.html
- requirements.txt

Also, we need to add the model and tokenizer in the `ReviewBot` folder so our backend could access them:
- model.h5 (downloaded from previous step)
- tokenizer.pickle (downloaded from previous step)

Finally, `ReviewBot` folder should look like this:

![image](https://github.com/hughiephan/DPL/assets/16631121/4e73c81f-7778-40a1-a470-fe83fd083ab8)

## Step 4: Code Backend

Now let's add the code to our backend `app.py` file. 

```
import pickle
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

app = Flask(__name__, template_folder='./')
CORS(app)

# Loading our model and tokenizer into our backend. Now our backend can use these to make prediction.
model = load_model('model.h5', compile=False)
with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

# When you go to localhost:5000 using a web browswer, it will render index.html's content
@app.route('/') 
def index(): 
    return render_template('index.html')

# The Frontend will make API call to this localhost:5000/predict?text=TheMovieIsTerrible, and backend will return "The review is negative"
@app.route('/predict', methods=['GET'])
def predict():
    text = request.args.get('text', '')
    sequence = tokenizer.texts_to_sequences([text])
    padded = pad_sequences(sequence, maxlen=120)
    prediction = model.predict(padded)
    if prediction[0][0] >= 0.5:
         return "The review is positive."
    else:
        return "The review is negative."
```

Add the following content to `requirements.txt` file. `pickle-mixin` provides a way to deserialize our `Tokenizer` and make it runnable in our backend. `flask` is our backend server, we use it along with `flask-cors` to allow Cross Origin Resource Sharing. When we work with API, we often need to have `flask-cors` enabled to let Frontend access the Backend.  

```
pickle-mixin
flask
flask-cors
tensorflow
```

## Step 5: Install Backend

Open command line, and run this command. The command will look at the `requirements.txt` and install the four libraries `pickle-mixin`, `flask`, `flask-cors`, `tensorflow`

```
pip install -r requirements.txt
```

![image](https://github.com/hughiephan/DPL/assets/16631121/71430a8e-7d9a-4978-a78a-aea2df0b6cc0)

## Step 6: Start Backend

Open a command line and run below command:
```
flask run
```

Now your backend server is running on `localhost:5000` and ready to give prediction. You can type `localhost:5000` on a web URL and see a blank page (After we add the frontend, we will see some content). Finally, we need `tensorflow` because we built our model based `tensorflow` and we will need to use some of it's libraries like `load_model` and `pad_sequence`.

![image](https://github.com/hughiephan/DPL/assets/16631121/d05272bd-801a-4d58-8ae6-d164cd69864c)

## Step 7: Code Frontend

HTML is the language for documents to be displayed in a web browser. 

Add the following code to `index.html` file:

```html
<html>

<!-- This is our CSS. You can read more about CSS here: https://blog.hubspot.com/website/css-tutorial -->
<style>
    @import url("https://fonts.googleapis.com/css2?family=Montserrat&display=swap");
    :root {
        --accent-color: #a876aa;
        --background-color: #eeeeee;
    }
    body {
        font-family: "Montserrat", sans-serif;
        background-color: var(--background-color);
        display: flex;
        align-items: center;
        justify-content: center;
        height: 100vh;
        margin: 0;
    }
    .container {
        display: flex;
        flex-direction: column;
        background-color: #ffffff;
        border-radius: 30px;
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1), 0 6px 6px rgba(0, 0, 0, 0.1);
        height: 800px;
        width: 600px;
        max-height: 90%;
    }
    .header {
        display: flex;
        align-items: center;
        margin: 20px;
        color: var(--accent-color);
    }
    .header .avatar {
        background-color: var(--accent-color);
        align-self: center;
        padding: 5px;
        width: 50px;
        border-radius: 50%;
    }
    .header h3 {
        margin-left: 20px;
        margin-right: auto;
    }
    .chat {
        background-color: #fff;
        height: 100%;
        overflow: auto;
        padding: 10px;
    }
    .message {
        font-size: 16px;
        line-height: 25px;
        width: fit-content;
        max-width: 450px;
        margin: 20px 10px;
        padding: 20px;
        border-radius: 30px;
    }
    .message.review {
        background-color: var(--accent-color);
        color: #fff;
        border-top-left-radius: 0px;
        padding-left: 30px;
    }
    .message.text {
        background-color: #eee;
        border-top-right-radius: 0px;
        margin-left: auto;
        padding-right: 30px;
    }
    input[type="text"] {
        background-color: #eee;
        color: var(--accent-color);
        font-family: inherit;
        border: 0;
        border-radius: 50px;
        padding: 14px 40px;
        margin: 20px;
        font-size: 16px;
        cursor: pointer;
        outline: none;
    }
</style>

<!-- This is our HTML content -->
<body>
    <div class="container">
    <div class="header"> 
        <img src="https://cdn-icons-png.flaticon.com/512/2233/2233922.png" alt="" class="avatar">
        <h3>Chatbot for Reviewing IMDB Comments</h3>
    </div>
    <div id="chat" class="chat"> </div>
    <input type="text" id="inputText" placeholder="Please enter a review">
    </div>
</body>

<!-- This is our javascript, we use this to manipulate the HTML content -->
<script>
    const chat = document.getElementById("chat");  // Find the element with id = chat 
    const reviewBtn = document.getElementById("reviewBtn"); // Find the element with id = reviewBtn 
    const inputText = document.getElementById('inputText'); // Find the element with id = inputText 
    inputText.addEventListener('keypress', async (event) => {   
        if (event.key === 'Enter') {  // Run this action when user type something into inputText 
            const inputValue = inputText.value;  // We get the text value typed by the user 
            const data = 'http://localhost:5000/predict?text=' + encodeURIComponent(inputText.value) // And send the user text to our backend
            result = await fetch(data).then(response => response.text()) // Let's wait for backend to return a response. The result will be 'The review is postive' or ' The review is negative'

            // Now we will update what the user has typed, and the result from backend, and add it to the HTML body so the user can see both their text and review result.
            const message = document.createElement("div");   
            const review = document.createElement("div");
            message.classList.add("message", "text");
            review.classList.add("message", "review");
            review.innerHTML = result;
            message.innerHTML = inputText.value;
            chat.appendChild(message);
            chat.appendChild(review);
        }
    });
</script>
</html>
```

## Step 8: Start Frontend
To start ReviewBot, double click on `index.html` or go to `localhost:5000` on any web browswer.

![image](https://github.com/hughiephan/DPL/assets/16631121/fb66d617-08d9-4f35-81ae-f26ebc436b92)

## Step 9 (Optional): Deploy ReviewBot to Render.com
https://dev.to/sm0ke/deploy-flask-to-render-5f39

# Debugging
If issue happens, try the following solutions
```
Problem: Encountered error while trying to install package pickle-mixin. 
Answer: Try pickle5
```
