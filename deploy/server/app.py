import os
import numpy as np
from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

app = Flask(__name__)

model = load_model('model.h5')
with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

@app.route('/')
def hello_world():
    return 'Hi from Flask!'

@app.route('/predict', methods=['GET'])
def predict():
    try:
        text = request.args.get('text', '')
        input_sequence = tokenizer.texts_to_sequences([sentence])
        input_padded = pad_sequences(input_sequence, maxlen=120)
        prediction = model.predict(padded_sequence)
        if prediction[0][0] >= 0.5:
            return "The review is positive."
        else:
            return "The review is negative."
    except Exception as e:
        return jsonify({'error': str(e)}), 400
