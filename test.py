from flask import Flask, request, redirect, render_template,session
import py.mePROD as process
import pandas as pd 
import numpy as np
import os
import time
# from flask_cors import CORS
app = Flask(__name__)
# CORS(app)
app.secret_key = '123'

@app.route("/", methods=["GET"])
def index():
  # return redirect("/static/index.html", code=302)
    return render_template('params.jinja')



@app.route("/api/params", methods=["POST"])
def http_resp():
    data = request.json
    session['itype'] = data['input_type']
    session['normal_method']=data['normal_method']

  
    return{'sucess':'yes'}
    
  
@app.route("/api/process", methods=["POST"])
def processor():
    file_val = request.files['file']
    data=pd.read_csv(file_val,sep='\t',header=0)
    
    print("Input Type:",session['itype'])
    print("Normalization Method:",session['normal_method'])
    normed_data = process.IT_adjustment(data)
    if session['normal_method'] == 'TI':
        normed_data = process.total_intensity_normalisation(normed_data)
    elif session['normal_method'] == 'MD':
        normed_data = process.Median_normalisation(normed_data)
    elif session['normal_method'] == 'TMM':
        normed_data = process.TMM(normed_data)
    else:
        print('No Normalization performed')
        
    extracted_data = process.extract_heavy(normed_data)
    baselined = process.baseline_correction(extracted_data)
    timestr = time.strftime("%Y%m%d-%H%M%S")
    baselined.to_csv("./Results/"+timestr+".txt",sep='\t')
    return(baselined.to_json())


# @app.route("/runs/", methods=["GET", "POST"])
# def runs():
#   # Returns a list of all runs to select from
#   pass



if __name__  == '__main__':
    
    app.run()