from flask import Flask, render_template, url_for, flash, redirect
from flask import request
import numpy as np
import joblib
import os
from flask import send_from_directory
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
#from tensorflow.keras.applications.imagenet_utils import preprocess_input
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['SECRET_KEY'] = '17d12c21ee0842faaf7d013654f4c79d'
@app.route('/')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/cancer')
def cancer():
    return render_template('cancer.html')

@app.route('/diabetes')
def diabetes():
    return render_template('diabetes.html')

@app.route('/heart')
def heart():
    return render_template('heart.html')

@app.route('/kidney')
def kidney():
    return render_template('kidney.html')

@app.route('/liver')
def liver():
    return render_template('liver.html')

@app.route('/malaria')
def malaria():
    return render_template('malaria.html')

@app.route('/pneumonia')
def pneumonia():
    return render_template('pneumonia.html')

def ValuePredictor(to_predict_list, size):
    to_predict = np.array(to_predict_list).reshape(1,size)
    if(size==8):#Diabetes
        loaded_model = joblib.load("diabetes_model.pkl")
        result = loaded_model.predict(to_predict)
    elif(size==16):#Cancer
        loaded_model = joblib.load("cancer_model.pkl")
        result = loaded_model.predict(to_predict)
    elif(size==14):#Kidney
        loaded_model = joblib.load("kidney_model.pkl")
        result = loaded_model.predict(to_predict)
    elif(size==10):
        loaded_model = joblib.load("liver_model.pkl")
        result = loaded_model.predict(to_predict)
    elif(size==9):#Heart
        loaded_model = joblib.load("heart_model.pkl")
        result =loaded_model.predict(to_predict)
    return result[0]


@app.route('/result',methods = ["POST"])
def result():
    if request.method == 'POST':
        to_predict_list = request.form.to_dict()
        to_predict_list=list(to_predict_list.values())
        to_predict_list = list(map(float, to_predict_list))
        if(len(to_predict_list)==8):#Daiabtes
            result = ValuePredictor(to_predict_list,8)
        elif(len(to_predict_list)==16):#Cancer
            result = ValuePredictor(to_predict_list,16)
        elif(len(to_predict_list)==9):#Heart
            result = ValuePredictor(to_predict_list,9)
        elif(len(to_predict_list)==14):#Kidney
            result = ValuePredictor(to_predict_list,14)
        elif(len(to_predict_list)==10):#Liver
            result = ValuePredictor(to_predict_list,10)
    if(int(result)==1):
        prediction='RESULT IS POSITIVE ! PLEASE VISIT THE DOCTOR.'
    else:
        prediction='RESULT IS NEGATIVE ! YOU ARE HEALTHY.' 
    return(render_template("result.html", prediction_text=prediction))


model = load_model('model_malaria.h5')

def model_predict(img_path, model):
    img = image.load_img(img_path, target_size=(64, 64))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    preds = model.predict(x)
    if preds[0][0] == 0:
        preds = "Parasitized"
    else:
        preds = "Uninfected" 
    return preds

@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        try:
            f = request.files['file']
            # Save the file to ./uploads
            basepath = os.path.dirname(__file__)
            file_path = os.path.join(
                    basepath, 'uploads', secure_filename(f.filename))
            f.save(file_path)
            # Make prediction
            preds = model_predict(file_path, model)
            #result=preds
            return render_template('predict.html', image_file_name = f.filename, preds = preds)
        except:
            flash("Please select the image first !!", "danger")      
            return redirect(url_for("malaria"))
    return None

@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory('uploads', filename)


model2 = load_model('model_pneumonia.h5')

def model2_predict(img_path, model2):
    img = image.load_img(img_path, target_size=(64,64))
    # Preprocessing the image
    x2 = image.img_to_array(img)

    x2 = np.expand_dims(x2, axis=0)
    preds = model2.predict(x2)
    if preds[0][0] == 1:
        preds = "Normal"
    else:
        preds = "Pneumonia" 
    return preds

@app.route('/predict2', methods=['GET', 'POST'])
def upload2():
    if request.method == 'POST':
        try:
            # Get the file from post request
            f = request.files['file']
            # Save the file to ./uploads
            basepath = os.path.dirname(__file__)
            file_path = os.path.join(
                    basepath, 'uploads2', secure_filename(f.filename))
            f.save(file_path)
            # Make prediction
            preds = model2_predict(file_path, model2)
            #result=preds
            return render_template('predict2.html', image_file_name = f.filename, preds = preds)
        except:
            flash("Please select the image first !!", "danger")      
            return redirect(url_for("pneumonia"))
    return None

@app.route('/uploads2/<filename>')
def send_file2(filename):
    return send_from_directory('uploads2', filename)


if __name__=="__main__":
    #app.run(host='0.0.0.0' ,port=8080, debug=True)
    app.run(debug=True)
#if __name__=="__main__":
#    app.run(host='0.0.0.0', port=8080)