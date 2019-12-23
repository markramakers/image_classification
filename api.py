from flask import Flask, send_from_directory, request, render_template, jsonify
from pathlib import Path
import tensorflow as tf
from PIL import Image
import numpy as np

model_path = Path("models/mnist_v1.h5")

model = tf.keras.models.load_model(model_path)
model.summary()

app = Flask(__name__)


@app.route('/home')
def root():
    file_path = 'predict.html'
    return render_template(file_path)


@app.route('/templates/<path:path>')
def send_js(path):
    return send_from_directory('templates', path)


@app.route('/predict', methods = ['POST'])
def predict():
    print(request.files)
    file = request.files['file']
    print(file)

    img = Image.open(request.files['file'].stream).convert("L")
    img = img.resize((28, 28))
    im2arr = np.array(img)
    im2arr = im2arr.reshape(1, 28, 28)
    y_pred = model.predict(im2arr)
    print("Prediction", y_pred)
    predictions = {
        label: float(y_pred[0][label])
        for label in range(0, 10)
    }
    print(predictions)
    return jsonify(predictions)


if __name__ == '__main__':
    app.run(debug=True)
