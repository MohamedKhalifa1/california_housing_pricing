import json
import pandas as pd
import pickle
import numpy as np
from flask import Flask ,  request , app ,jsonify , url_for , render_template

app = Flask(__name__)
scalar = pickle.load(open('std_scaler.pkl','rb'))
model = pickle.load(open('regressor_model.pkl','rb'))

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/predict_api',methods=['POST'])
def predict_api():
    data=request.json['data']
    print(data)
    print(np.array(list(data.values())).reshape(1,-1))
    new_data=scalar.transform(np.array(list(data.values())).reshape(1,-1))
    output=model.predict(new_data)
    print(output[0])
    return jsonify(output[0])

@app.route('/predict',methods=['POST'])
def predict():
    data=[float(x) for x in request.form.values()]
    final_input=scalar.transform(np.array(data).reshape(1,-1))
    print(np.array(data).reshape(1,-1))
    output = model.predict(np.array(data).reshape(1,-1))[0]
    return render_template("home.html",prediction_text="The House price prediction in California is {}".format(output))


if __name__=="__main__":
    app.run(debug=True)
   