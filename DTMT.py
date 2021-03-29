from flask import Flask, request, redirect, render_template,session, Response
from DynaTMT.DynaTMT import PD_input,plain_text_input
import json
import pandas as pd 
import numpy as np
import os
import time

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
    return {'sucess':'yes'}
    
@app.route("/api/params_TPP", methods=["POST"])
def http_resp_TPP():
    data = request.json
    session['itype'] = data['input_type']
    session['normal_method']=data['normal_method']
    if data['it_adj'] == 'Yes':
        session['it_adjustment']=True
    else:
        session['it_adjustment']=False
    
    return {'sucess':'yes'}
    


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
            
        heavy = process_PD.extract_heavy()
        light = process_PD.extract_light()
        
        stats_heavy = process_PD.statistics(heavy)
        stats_light = process_PD.statistics(light)
        
        baselined=process_PD.baseline_correction_peptide_return(heavy,i_baseline=session['baseline_index'])
        timestr=time.strftime("%Y%m%d-%H%M%S")
        os.mkdir("./Results/"+timestr+"/")
        baselined.to_csv("./Results/"+timestr+"/processed_result_peptides.txt",sep='\t')
        
        baselined = process_PD.sum_peptides_for_proteins(baselined)
        baselined.to_csv("./Results/"+timestr+"/processed_result.txt",sep='\t')
        stats_light.to_csv("./Results/"+timestr+"/statistics_light.txt",sep='\t')
        stats_heavy.to_csv("./Results/"+timestr+"/statistics_heavy.txt",sep='\t')

        baselined.to_csv("./Temp/Result.csv")
        return(json.dumps({}))
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
        heavy = process_MQ.extract_heavy()


        baselined=process_MQ.baseline_correction_peptide_return(heavy,i_baseline=session['baseline_index'])
        timestr=time.strftime("%Y%m%d-%H%M%S")
        os.mkdir("./Results/"+timestr+"/")
        baselined.to_csv("./Results/"+timestr+"/processed_result_peptides.txt",sep='\t')
        baselined = process_MQ.sum_peptides_for_proteins(baselined)
        baselined.to_csv("./Results/"+timestr+"/processed_result.txt",sep='\t')
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
            
        heavy = process_PD.extract_heavy()
        light = process_PD.extract_light()
        
        stats_heavy = process_PD.statistics(heavy)
        stats_light = process_PD.statistics(light)
        
        
        
        light=process_PD.sum_peptides_for_proteins(light)
        light.index.name= 'Accession'
        heavy=process_PD.sum_peptides_for_proteins(heavy)
        heavy.index.name= 'Accession'
        timestr=time.strftime("%Y%m%d-%H%M%S")
        os.mkdir("./Results/"+timestr+"/")
        
        stats_light.to_csv("./Results/"+timestr+"/statistics_light.txt",sep='\t')
        stats_heavy.to_csv("./Results/"+timestr+"/statistics_heavy.txt",sep='\t')



        heavy.to_csv("./Results/"+timestr+"/Result_heavy.txt",sep='\t')
        light.to_csv("./Results/"+timestr+"/Result_light.txt",sep='\t')
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
        light.index.name= 'Accession'
        heavy=process_MQ.sum_peptides_for_proteins(heavy)
        heavy.index.name= 'Accession'
        timestr=time.strftime("%Y%m%d-%H%M%S")
        os.mkdir("./Results/"+timestr+"/")

        heavy.to_csv("./Results/"+timestr+"/Result_heavy.txt",sep='\t')
        light.to_csv("./Results/"+timestr+"/Result_light.txt",sep='\t')
        heavy.to_csv("./Temp/Heavy_Result.csv")
        light.to_csv("./Temp/Light_Result.csv")
        return(heavy.to_json(),light.to_json())

    else:
        print('Input Type Error')
        return('Input Type Error')



@app.route("/api/results", methods=["GET"])
def results_index():

    return render_template('Results.jinja')

@app.route("/all_results", methods=["GET"])
def all_results():
    return render_template('all_results_page.jinja')

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


@app.route("/api/populate_select",methods=["GET"])
def get_folders():
    folders=[name for name in os.listdir("./Results")]
    print(folders)
    return json.dumps(folders)

@app.route("/api/get_defined_result",methods=["POST"])
def return_results():
    data = request.json
    folder = data['result']
    folder = os.path.join("./Results/",folder)
    ftype = data['type']
    if ftype == 'mePROD':
        dataframe = pd.read_csv(folder+"/processed_result.txt",sep='\t')
        try:
            stats_light = pd.read_csv(folder +"/statistics_light.txt",sep='\t')
            stats_heavy = pd.read_csv(folder +"/statistics_heavy.txt",sep='\t')
            data_as_json = {
                'Data':dataframe.to_numpy().tolist(),
                'stats_light':stats_light.to_numpy().tolist(),
                'stats_heavy':stats_heavy.to_numpy().tolist(),
                'stats_columns':list(stats_light.columns),
                'stats':'yes',
                'stats_index':list(stats_light.iloc[:,0])
            }
            resp = Response()
            resp.set_data(json.dumps(data_as_json))
            
            return resp
        except:
            data_as_json = {
                'Data':dataframe.to_numpy().tolist(),
                'stats':'no'
            }
            resp = Response()
            resp.set_data(json.dumps(data_as_json))
            return resp

    elif ftype == 'pSILAC':
        dataframe_light = pd.read_csv(folder+"/Result_light.txt",sep='\t')
        dataframe_heavy = pd.read_csv(folder+"/Result_heavy.txt",sep='\t')
        try:
            stats_light = pd.read_csv(folder +"/statistics_light.txt",sep='\t')
            stats_heavy = pd.read_csv(folder +"/statistics_heavy.txt",sep='\t')
            data_as_json = {
                'Data_Light':dataframe_light.to_numpy().tolist(),
                'Data_heavy':dataframe_heavy.to_numpy().tolist(),
                'stats_light':stats_light.to_numpy().tolist(),
                'stats_heavy':stats_heavy.to_numpy().tolist(),
                'stats_columns':list(stats_light.columns),
                'stats':'yes',
                'stats_index':list(stats_light.iloc[:,0])
            }
            return Response(json.dumps(data_as_json),mimetype='text/json')
       
        except:
            data_as_json = {
                'Data':dataframe.to_numpy().tolist(),
                'stats':'no'
            }
            resp = Response()
            resp.set_data(json.dumps(data_as_json))
            return resp
    else:
        return('ERROR')
    
@app.route("/api/result_type",methods=["GET","POST"])
def get_result_type():
    data = request.json
    folder = data['result']
    folder = os.path.join("./Results/",folder)
    list_of_files = os.listdir(folder)
    print(list_of_files)
    if 'processed_result.txt' in list_of_files:
        print('meprod')
        return json.dumps({'type':'mePROD'})
    elif 'Result_heavy.txt' in list_of_files:
        print('pSILAC')
        return json.dumps({'type':'pSILAC'})
        
    else:
        return json.dumps({'return':'fail'})


if __name__  == '__main__':
    path = os.path.dirname(os.path.realpath(__file__))    
    if not os.path.exists(os.path.join(path,"./Results")):
        os.mkdir(os.path.join(path,"./Results"))
    if not os.path.exists(os.path.join(path,"./Temp")):
        os.mkdir(os.path.join(path,"./Temp"))
    import webbrowser
    webbrowser.open("http://127.0.0.1:5000")
    app.run()