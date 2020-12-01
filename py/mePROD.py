from scipy import stats
from scipy.stats import trim_mean
import pandas as pd
import numpy as np


'''PREPROCESSING: Heavy AND Light peptides are used for summed intensity normalisation'''
class PD_input:
    def __init__(self, input):
        self.input_file = input
    def IT_adjustment(self):
        input = self.input_file
        print("IT adjustment")
        channels = [col for col in input.columns if 'Abundance:' in col]
        IT=[col for col in input.columns if 'Ion Inject Time' in col]
        inject_times=input[IT[0]]
        input[channels]=input[channels].divide(inject_times,axis=0)
        input[channels]=input[channels].multiply(1000)
        print("Done")
        self.input_file = input
        

    def extract_heavy (self):
        input = self.input_file
        print("Extraction of labelled peptides")
        modi=list([col for col in input.columns if 'Modification' in col])
        modi=modi[0]
        
        Heavy_peptides=input[input[modi].str.contains('TMTK8|Label|TMTproK8',na=False)]

        print("Extraction Done","Extracted Peptides:", len(Heavy_peptides))
        self.input_file = Heavy_peptides



    def baseline_correction(self,threshold=5,i_baseline=0,method='TI',PD=True):#TODO Make available for together analyzed data
        input = self.input_file
        print("Baseline correction")
        channels=[col for col in input.columns if 'Abundance:' in col]
        MPA = list([col for col in input.columns if 'Master Protein Accession' in col])
        MPA = MPA[0]
        protein_groups=input.groupby(by=[MPA],sort=False)
        results={}
        for group in protein_groups.groups:
            temp_data=protein_groups.get_group(group)
            temp_data = temp_data[channels]
            baseline_channel=channels[i_baseline]
            baseline=temp_data[baseline_channel]



            temp_data[channels]=temp_data[channels].subtract(baseline,axis='index')
            temp_data['Mean']=temp_data[channels].mean(axis=1)
            
            
            temp_data[temp_data < 0]=0 # replace negative abundances with 0
            temp_data=temp_data.loc[temp_data['Mean'] > threshold] # set S/N threshold for each PSM
            if method == 'sum':
                
                temp_data=temp_data[channels].sum()
                
            elif method == 'mean':
                
                temp_data=temp_data[channels].mean()
            elif method == 'median':
                
                temp_data=temp_data[channels].median()
            else:
                
                temp_data=temp_data[channels].sum()

            results[group]=temp_data
        print("Baseline correction done")
        result_df=pd.DataFrame.from_dict(results, orient='index',columns=channels)
        self.input_file = result_df
        return result_df

    def TMM(self):
        input = self.input_file
        channels=[col for col in input.columns if 'Abundance:' in col]
        input=input.dropna(subset=channels)
        input_trim=input[input[channels] < input[channels].quantile(.95)]
        print("Normalization")
        input_trim[channels]=input_trim[channels].divide(input_trim[channels[0]],axis=0)
        tm=np.argmin(trim_mean(input_trim[channels],0.25))
        summed=np.array(trim_mean(input_trim[channels], 0.25))
        minimum=summed[tm]
        norm_factors=summed/minimum
        input[channels]=input[channels].divide(norm_factors, axis=1)
        self.input_file = input
        
    def chunks(self,l, n):
        """Yield successive n-sized chunks from l."""
        for i in range(0, len(l), n):
            yield l[i:i + n]




    def total_intensity_normalisation(self):
        input = self.input_file
        channels=[col for col in input.columns if 'Abundance:' in col]
        input=input.dropna(subset=channels)
        print("Normalization")
        minimum=np.argmin(input[channels].sum().values)
        summed=np.array(input[channels].sum().values)
        minimum=summed[minimum]
        norm_factors=summed/minimum
        input[channels]=input[channels].divide(norm_factors, axis=1)
        print("Normalization done")
        self.input_file = input

    def Median_normalisation(self):
        input = self.input_file
        channels=[col for col in input.columns if 'Abundance:' in col]
        input=input.dropna(subset=channels)
        print("Normalization")
        minimum=np.argmin(input[channels].median().values)
        summed=np.array(input[channels].median().values)
        minimum=summed[minimum]
        norm_factors=summed/minimum
        input[channels]=input[channels].divide(norm_factors, axis=1)
        print("Normalization done")
        self.input_file = input

    def sum_peptides_for_proteins(self):
        input = self.input_file
        print('Calculate Protein quantifications from PSM')
        channels = [col for col in input.columns if 'Abundance:' in col]
        MPA=list([col for col in input.columns if 'Master Protein Accession' in col])
        MPA=MPA[0]
        PSM_grouped=PSM.groupby(by=[MPA])
        result={}
        for group in PSM_grouped.groups:
            temp=PSM_grouped.get_group(group)
            sums=temp[channels].sum()
            result[group]=sums
        
        protein_df=pd.DataFrame.from_dict(result, orient='index',columns=channels)
        
        print("Combination done")
        return protein_df


    def log2(self):
        input = self.input_file
        channels=[col for col in input.columns if 'Abundance:' in col]
        input[channels]=np.log2(input[channels])
        print("Normalization done")
        self.input_file = input

class plain_text_input:
    def __init__(self, input, it_adj=True):
        self.input_file = input
        self.input_columns = list(input.columns)
        if it_adj == True:
            self.abundances = self.input_columns[3:]
            self.mpa = self.input_columns[0]
            self.it_col = self.input_columns[1]
            self.modifications = self.input_columns[2]
        else:
            self.abundances = self.input_columns[2:]
            self.modifications = self.input_columns[1]
            self.mpa = self.input_columns[0]
            

    def IT_adjustment(self):
        input = self.input_file
        print("IT adjustment")
        channels = self.abundances
        IT=self.it_col
        inject_times=input[IT]
        input[channels]=input[channels].divide(inject_times,axis=0)
        input[channels]=input[channels].multiply(1000)
        print("Done")
        self.input_file = input
        

    def extract_heavy (self):
        input = self.input_file
        print("Extraction of labelled peptides")
        modi=self.modifications
        
        
        Heavy_peptides=input[input[modi].str.contains('TMTK8|Label|TMTproK8',na=False)]

        print("Extraction Done","Extracted Peptides:", len(Heavy_peptides))
        self.input_file = Heavy_peptides



    def baseline_correction(self,threshold=5,i_baseline=0,method='TI'):#TODO Make available for together analyzed data
        input = self.input_file
        print("Baseline correction")
        channels=self.abundances
        MPA = self.mpa
        
        protein_groups=input.groupby(by=[MPA],sort=False)
        results={}
        for group in protein_groups.groups:
            temp_data=protein_groups.get_group(group)
            temp_data = temp_data[channels]
            baseline_channel=channels[i_baseline]
            baseline=temp_data[baseline_channel]



            temp_data[channels]=temp_data[channels].subtract(baseline,axis='index')
            temp_data['Mean']=temp_data[channels].mean(axis=1)
            
            
            temp_data[temp_data < 0]=0 # replace negative abundances with 0
            temp_data=temp_data.loc[temp_data['Mean'] > threshold] # set S/N threshold for each PSM
            if method == 'sum':
                
                temp_data=temp_data[channels].sum()
                
            elif method == 'mean':
                
                temp_data=temp_data[channels].mean()
            elif method == 'median':
                
                temp_data=temp_data[channels].median()
            else:
                
                temp_data=temp_data[channels].sum()

            results[group]=temp_data
        print("Baseline correction done")
        result_df=pd.DataFrame.from_dict(results, orient='index',columns=channels)
        self.input_file = result_df
        return result_df

    def TMM(self):
        input = self.input_file
        channels=self.abundances
        input=input.dropna(subset=channels)
        input_trim=input[input[channels] < input[channels].quantile(.95)]
        print("Normalization")
        input_trim[channels]=input_trim[channels].divide(input_trim[channels[0]],axis=0)
        tm=np.argmin(trim_mean(input_trim[channels],0.25))
        summed=np.array(trim_mean(input_trim[channels], 0.25))
        minimum=summed[tm]
        norm_factors=summed/minimum
        input[channels]=input[channels].divide(norm_factors, axis=1)
        self.input_file = input
        
    
    def total_intensity_normalisation(self):
        input = self.input_file
        channels=self.abundances
        input=input.dropna(subset=channels)
        print("Normalization")
        minimum=np.argmin(input[channels].sum().values)
        summed=np.array(input[channels].sum().values)
        minimum=summed[minimum]
        norm_factors=summed/minimum
        input[channels]=input[channels].divide(norm_factors, axis=1)
        print("Normalization done")
        self.input_file = input

    def Median_normalisation(self):
        input = self.input_file
        channels=self.abundances
        input=input.dropna(subset=channels)
        print("Normalization")
        minimum=np.argmin(input[channels].median().values)
        summed=np.array(input[channels].median().values)
        minimum=summed[minimum]
        norm_factors=summed/minimum
        input[channels]=input[channels].divide(norm_factors, axis=1)
        print("Normalization done")
        self.input_file = input
