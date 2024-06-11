import os
import shutil
from flask import Flask, render_template, request
import numpy as np
import tensorflow as tf
from keras.preprocessing import image

app = Flask(__name__)

def predict_label(img_path, model_path):
    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    
    dic = {0: 'Diseased', 1: 'Healthy'}
    
    i = image.load_img(img_path, target_size=(224, 224))
    i = image.img_to_array(i) / 255.0
    i = np.expand_dims(i, axis=0).astype(np.float32)
    
    interpreter.set_tensor(input_details[0]['index'], i)
    
    interpreter.invoke()
    
    output_data = interpreter.get_tensor(output_details[0]['index'])
    prediction = np.argmax(output_data)
    
    return dic[prediction]
    
@app.route("/", methods=['GET'])
def main():
    return render_template('start.html')

@app.route("/plant", methods=['GET'])
def choose_plant():
    return render_template("plant.html")

@app.route("/plant/tomato", methods=['GET'])
def predict_tomato():
    return render_template("predict_tomato.html")

@app.route("/plant/potato", methods=['GET'])
def predict_potato():
    return render_template("predict_potato.html")

@app.route("/plant/tomato/predict", methods=['GET', 'POST'])
def get_output_tomato():
    if request.method == 'POST':
        img = request.files['image']
        img_path = "static/data/tomato/" + img.filename
        img.save(img_path)

        p = predict_label(img_path, 'models/tomato_model.tflite')

        if p == 'Healthy':
            target_dir = "static/data/tomato/healthy/"
        else:
            target_dir = "static/data/tomato/diseased/"
        
        target_path = target_dir + img.filename

        if os.path.exists(target_path):
            os.remove(target_path)
        
        shutil.move(img_path, target_path)
        
        return render_template("predict_tomato.html", prediction=p, img_path=target_path)

@app.route("/plant/potato/predict", methods=['GET', 'POST'])
def get_output_potato():
    if request.method == 'POST':
        img = request.files['image']
        img_path = "static/data/potato/" + img.filename
        img.save(img_path)
        
        p = predict_label(img_path, 'models/potato_model.tflite')

        if p == 'Healthy':
            target_dir = "static/data/potato/healthy/"
        else:
            target_dir = "static/data/potato/diseased/"
        
        target_path = target_dir + img.filename

        if os.path.exists(target_path):
            os.remove(target_path)
        
        shutil.move(img_path, target_path)
        
        return render_template("predict_potato.html", prediction=p, img_path=target_path)

if __name__ == '__main__':
    app.run(debug=True)
