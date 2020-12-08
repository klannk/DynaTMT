from scipy import stats
from scipy.stats import trim_mean
import pandas as pd
import numpy as np



class PD_input:
    '''Class containing functions to analyze the default peptide/PSM output from ProteomeDiscoverer. All column names are assumed
    to be default PD output. If your column names do not match these assumed strings, you can modify them or use the plain_text_input
    class, that uses column order instead of names.
    '''
    def __init__(self, input):
        '''Initialises PD_input class with specified input file. The input file gets stored
        in the class variable self.input_file.
        '''
        self.input_file = input
        
    def IT_adjustment(self):
        '''This function adjusts the input DataFrame stored in the class variable self.input_file for Ion injection times.
        Abundance channels should contain "Abundance:" string and injection time uses "Ion Inject Time" as used by ProteomeDiscoverer
        default output. For other column headers please refer to plain_text_input class.
        '''
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
        '''This function takes the class variable self.input_file dataframe and extracts all heavy labelled peptides. Naming of the 
        Modifications: Arg10: should contain Label, TMTK8, TMTproK8. Strings for modifications can be edited below for customisation.
        writes filtered self.input_file back to class
        '''
        input = self.input_file
        print("Extraction of labelled peptides")
        modi=list([col for col in input.columns if 'Modification' in col])
        modi=modi[0]
        '''Change Modification String here'''
        Heavy_peptides=input[input[modi].str.contains('TMTK8|Label|TMTproK8',na=False)]

        print("Extraction Done","Extracted Peptides:", len(Heavy_peptides))
        return Heavy_peptides


    def extract_light (self):
        '''This function takes the class variable self.input_file dataframe and extracts all light labelled peptides. Naming of the 
        Modifications: Arg10: should contain Label, TMTK8, TMTproK8. Strings for modifications can be edited below for customisation.
        Returns light peptide DF
        '''
        input = self.input_file
        print("Extraction of labelled peptides")
        modi=list([col for col in input.columns if 'Modification' in col])
        modi=modi[0]
        
        
        light_peptides=input[~input[modi].str.contains('TMTK8|Label|TMTproK8',na=False)]

        print("Extraction Done","Extracted Peptides:", len(light_peptides))
        return light_peptides

    def baseline_correction(self,input,threshold=5,i_baseline=0,method='sum'):
        '''This function takes the self.input_file DataFrame and substracts the baseline/noise channel from all other samples. The index of the
        baseline column is defaulted to 0. Set i_baseline=X to change baseline column.
        Threshold: After baseline substraction the remaining average signal has to be above threshold to be included. Parameter is set with threshold=X.
        This prevents very low remaining signal peptides to produce artificially high fold changes. Has to be determined empirically.
        Method: The method parameter sets the method for protein wollup quantification. Default is 'sum', which will sum all peptides for
        the corresponding protein. Alternatives are 'median' or 'mean'. If no or invalid input is given it uses 'sum'.
        Modifies self.input_file variable and returns a pandas df.
        '''
        
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


    def statistics(self, input):
        '''This function provides summary statistics for quality control assessment from Proteome Discoverer Output.
        '''
        numeric_without_tmt_channels=[col for col in input.columns if not 'Abundance:' in col]
        print(input[numeric_without_tmt_channels].describe(include=[np.number]))
        return(input[numeric_without_tmt_channels].describe(include=[np.number]))

    def TMM(self):
        '''This function implements TMM normalisation (Robinson & Oshlack, 2010, Genome Biology). It modifies the self.input_file class
        variable.
        '''
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
        '''This function normalizes the self.input_file variable to the summed intensity of all TMT channels. It modifies the self.input_file
        to the updated DataFrame containing the normalized values.
        '''
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
        '''This function normalizes the self.input_file variable to the median of all individual TMT channels. It modifies the self.input_file
        to the updated DataFrame containing the normalized values.
        '''    
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

    def sum_peptides_for_proteins(self,input):
        '''This function takes a peptide/PSM level DataFrame stored in self.input_file and performs Protein quantification rollup based
        on the sum of all corresponding peptides.
        Returns a Protein level DataFrame and modifies self.input_file
        '''
        print('Calculate Protein quantifications from PSM')
        channels = [col for col in input.columns if 'Abundance:' in col]
        MPA=list([col for col in input.columns if 'Master Protein Accession' in col])
        MPA=MPA[0]
        PSM_grouped=input.groupby(by=[MPA])
        result={}
        for group in PSM_grouped.groups:
            temp=PSM_grouped.get_group(group)
            sums=temp[channels].sum()
            result[group]=sums
        
        protein_df=pd.DataFrame.from_dict(result, orient='index',columns=channels)
        print("Combination done")
        return protein_df[channels]


    def log2(self):
        '''Modifies self.input_file and log2 transforms all TMT intensities.
        '''
        input = self.input_file
        channels=[col for col in input.columns if 'Abundance:' in col]
        input[channels]=np.log2(input[channels])
        print("Normalization done")
        self.input_file = input

class plain_text_input:
    '''This class contains functions to analyze pSILAC data based on a plain text input file. The column names can be freely chosen, as
    long as all column names are unique. The different column identities are extracted by the column order:
    - Accession
    - Injection time (optional, is set in class init)
    - Modification
    - all following columns are assumed to contain TMT abundances
     '''
    def __init__(self, input, it_adj=True):
        '''Initialises class and extracts relevant columns.The different column identities are extracted by the column order:
        - Accession
        - Injection time (optional, set by it_adj parameter)
        - Modification
        - all following columns are assumed to contain TMT abundances 
         
        '''
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
        '''This function adjusts the input DataFrame stored in the class variable self.input_file for Ion injection times.
        
        '''
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
        '''This function takes the class variable self.input_file dataframe and extracts all heavy labelled peptides. Naming of the 
        Modifications: Arg10: should contain Label, TMTK8, TMTproK8. Strings for modifications can be edited below for customisation.
        writes filtered self.input_file back to class
        '''
        input = self.input_file
        print("Extraction of labelled peptides")
        modi=self.modifications
        
        
        Heavy_peptides=input[input[modi].str.contains('TMTK8|Label|TMTproK8',na=False)]

        print("Extraction Done","Extracted Peptides:", len(Heavy_peptides))
        self.input_file = Heavy_peptides


    def extract_light (self):
        '''This function takes the class variable self.input_file dataframe and extracts all light labelled peptides. Naming of the 
        Modifications: Arg10: should contain Label, TMTK8, TMTproK8. Strings for modifications can be edited below for customisation.
        Returns light peptide DF
        '''
        input = self.input_file
        print("Extraction of labelled peptides")
        modi=self.modifications
        
        
        light_peptides=input[~input[modi].str.contains('TMTK8|Label|TMTproK8',na=False)]

        print("Extraction Done","Extracted Peptides:", len(light_peptides))
        self.input_file = light_peptides
        return light_peptides

    def baseline_correction(self,threshold=5,i_baseline=0,method='TI'):
        '''This function takes the self.input_file DataFrame and substracts the baseline/noise channel from all other samples. The index of the
        baseline column is defaulted to 0. Set i_baseline=X to change baseline column.
        Threshold: After baseline substraction the remaining average signal has to be above threshold to be included. Parameter is set with threshold=X.
        This prevents very low remaining signal peptides to produce artificially high fold changes. Has to be determined empirically.
        Method: The method parameter sets the method for protein wollup quantification. Default is 'sum', which will sum all peptides for
        the corresponding protein. Alternatives are 'median' or 'mean'. If no or invalid input is given it uses 'sum'.
        Modifies self.input_file variable and returns a pandas df.
        '''
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
        '''This function implements TMM normalisation (Robinson & Oshlack, 2010, Genome Biology). It modifies the self.input_file class
        variable.
        '''
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
        '''This function normalizes the self.input_file variable to the summed intensity of all TMT channels. It modifies the self.input_file
        to the updated DataFrame containing the normalized values.
        '''
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
        '''This function normalizes the self.input_file variable to the median of all individual TMT channels. It modifies the self.input_file
        to the updated DataFrame containing the normalized values.
        '''    
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
    def sum_peptides_for_proteins(self,input):
        '''This function takes a peptide/PSM level DataFrame stored in self.input_file and performs Protein quantification rollup based
        on the sum of all corresponding peptides.
        Returns a Protein level DataFrame and modifies self.input_file
        '''
        
        print('Calculate Protein quantifications from PSM')
        channels = self.abundances
        MPA=self.mpa
        PSM_grouped=input.groupby(by=[MPA])
        result={}
        for group in PSM_grouped.groups:
            temp=PSM_grouped.get_group(group)
            sums=temp[channels].sum()
            result[group]=sums
        
        protein_df=pd.DataFrame.from_dict(result, orient='index',columns=channels)
        
        print("Combination done")
        return protein_df[channels]