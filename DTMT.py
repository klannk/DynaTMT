from flask import Flask, request, redirect, render_template,session
from py.mePROD import PD_input,plain_text_input

import pandas as pd 
import numpy as np
import os
import time
# from flask_cors import CORS
app = Flask(__name__)
app.secret_key = '123'



@app.route("/", methods=["GET"])
def index():
  # return redirect("/static/index.html", code=302)
    return render_template('params.jinja')

@app.route("/help")
def documentation():
    return render_template('documentation.jinja')


@app.route("/api/params", methods=["POST"])
def http_resp():
    data = request.json
    session['itype'] = data['input_type']
    session['normal_method']=data['normal_method']
    if data['it_adj'] == 'Yes':
        session['it_adjustment']=True
    else:
        session['it_adjustment']=False
    try:
        session['baseline_index']=int(data['base_index'])
    except ValueError:
        session['baseline_index']=0
        print("DEFAULTED BASELINE")
    return{'sucess':'yes'}
    
  
@app.route("/api/process", methods=["POST"])
def processor():
    file_val = request.files['file']
    data=pd.read_csv(file_val,sep='\t',header=0)
    if session['it_adjustment'] == True:
        process_MQ=plain_text_input(data, it_adj=True)
            
    else:
        process_MQ=plain_text_input(data, it_adj=False)
    process_PD = PD_input(data)
    print("Input Type:",session['itype'])
    print("Normalization Method:",session['normal_method'])
    if session['itype'] == "PD":
        print('STARTING PD PROCESSING')
        process_PD.IT_adjustment()
        if session['normal_method'] == 'TI':
            print('Total intensity normalisation')
            process_PD.total_intensity_normalisation()
            
        elif session['normal_method'] == 'MD':
            print('Median normalisation')
            process_PD.Median_normalisation()
        elif session['normal_method'] == 'TMM':
            print('TMM normalisation')
            process_PD.TMM()
        else:
            print('No Normalization performed')
            
        process_PD.extract_heavy()
        baselined=process_PD.baseline_correction(i_baseline=session['baseline_index'])
        timestr=time.strftime("%Y%m%d-%H%M%S")
        baselined.to_csv("./Results/"+timestr+".txt",sep='\t')
        baselined.to_json("./Temp/Result.json")
        return(baselined.to_json())
    elif session['itype'] == "MQ":
        
        print('STARTING PLAIN TEXT PROCESSING')
        if  session['it_adjustment'] == True:
            process_MQ.IT_adjustment()
        else:
            pass

        if session['normal_method'] == 'TI':
            print('Total intensity normalisation')
            process_MQ.total_intensity_normalisation()
            
        elif session['normal_method'] == 'MD':
            print('Median normalisation')
            process_MQ.Median_normalisation()
        elif session['normal_method'] == 'TMM':
            print('TMM normalisation')
            process_MQ.TMM()
        else:
            print('No Normalization performed')
        process_MQ.extract_heavy()
        baselined=process_MQ.baseline_correction(i_baseline=session['baseline_index'])
        timestr=time.strftime("%Y%m%d-%H%M%S")
        baselined.to_csv("./Results/"+timestr+".txt",sep='\t')
        baselined.to_json("./Temp/Result.json")
        return(baselined.to_json())

    else:
        print('Input Type Error')
        return('Input Type Error')

@app.route("/api/results", methods=["GET"])
def results_index():

    return render_template('Results.jinja')

@app.route("/api/get_latest",methods=["GET"])
def get_latest_result():
    data = pd.read_json("./Temp/Result.json")
    return(data.to_csv())
# @app.route("/runs/", methods=["GET", "POST"])
# def runs():
#   # Returns a list of all runs to select from
#   pass


if __name__  == '__main__':
    import webbrowser
    webbrowser.open("http://127.0.0.1:5000")
    app.run()