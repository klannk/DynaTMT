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

@app.route("/TPP", methods=["GET"])
def index_TPP():
  # return redirect("/static/index.html", code=302)
    return render_template('TPP_params.jinja')


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
    
@app.route("/api/params_TPP", methods=["POST"])
def http_resp_TPP():
    data = request.json
    session['itype'] = data['input_type']
    session['normal_method']=data['normal_method']
    if data['it_adj'] == 'Yes':
        session['it_adjustment']=True
    else:
        session['it_adjustment']=False
    
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
        if session['it_adjustment'] == True:

            process_PD.IT_adjustment()
        else:
            pass
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
        baselined.to_csv("./Temp/Result.csv")
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
        baselined.to_csv("./Temp/Result.csv")
        return(baselined.to_json())

    else:
        print('Input Type Error')
        return('Input Type Error')


@app.route("/api/process_TPP", methods=["POST"])
def processor_TPP():
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
        if session['it_adjustment'] == True:

            process_PD.IT_adjustment()
        else:
            pass
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
            
        
        light = process_PD.extract_light()
        process_PD.extract_heavy()
        heavy = process_PD.input_file

        light=process_PD.sum_peptides_for_proteins(light)
        heavy=process_PD.sum_peptides_for_proteins(heavy)
        timestr=time.strftime("%Y%m%d-%H%M%S")
        heavy.to_csv("./Results/"+timestr+"_heavy.txt",sep='\t')
        light.to_csv("./Results/"+timestr+"_light.txt",sep='\t')
        heavy.to_csv("./Temp/Heavy_Result.csv")
        light.to_csv("./Temp/Light_Result.csv")
        
        print('DONE')
        
        return(heavy.to_json())
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
        light = process_MQ.extract_light()
        process_MQ.extract_heavy()
        heavy = process_MQ.input_file

        light=process_MQ.sum_peptides_for_proteins(light)
        heavy=process_MQ.sum_peptides_for_proteins(heavy)
        timestr=time.strftime("%Y%m%d-%H%M%S")
        heavy.to_csv("./Results/"+timestr+"_heavy.txt",sep='\t')
        light.to_csv("./Results/"+timestr+"_light.txt",sep='\t')
        heavy.to_csv("./Temp/Heavy_Result.csv")
        light.to_csv("./Temp/Light_Result.csv")
        return(heavy.to_json(),light.to_json())

    else:
        print('Input Type Error')
        return('Input Type Error')

@app.route("/api/results", methods=["GET"])
def results_index():

    return render_template('Results.jinja')

@app.route("/api/results_TPP", methods=["GET"])
def results_index_TPP():

    return render_template('Results_TPP.jinja')


@app.route("/api/get_latest",methods=["GET"])
def get_latest_result():
    data = pd.read_csv("./Temp/Result.csv")
    return(data.to_csv())

@app.route("/api/get_latest_TPP_light",methods=["GET"])
def get_latest_result_TPP():
    data = pd.read_csv("./Temp/Light_Result.csv")
    return(data.to_csv())

@app.route("/api/get_latest_TPP_heavy",methods=["GET"])
def get_latest_result_TPPh():
    data = pd.read_csv("./Temp/Heavy_Result.csv")
    return(data.to_csv())


if __name__  == '__main__':
    if not os.path.exists("./Results"):
        os.mkdir("./Results")
    if not os.path.exists("./Temp"):
        os.mkdir("./Temp")
    import webbrowser
    webbrowser.open("http://127.0.0.1:5000")
    app.run()