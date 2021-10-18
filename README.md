<h1>Documentation</h1>


[![DOI](https://zenodo.org/badge/317233670.svg)](https://zenodo.org/badge/latestdoi/317233670)


    <p align="justify">The <b>DynaTMT tool</b> can be used to analyze <b>m</b>ultiplexed <b>e</b>nhanced <b>pro</b>tein <b>d</b>ynamic mass spectrometry (mePROD) data. mePROD uses pulse SILAC combined with Tandem Mass Tag (TMT) labelling to profile newly synthesized proteins. Through a booster channel, that contains a fully heavy labelled digest, the identification rate of labelled peptides is greatly enhanced, compared to other pSILAC experiments. Through the multiplexing capacity of TMT reagents it is possible during the workflow to use the boost signal as a carrier that improves survey scan intensities, but does not interfere with quantification of the pulsed samples. This workflow makes labelling times of minutes (down to 15min in the original publication) possible.
    Additionally, mePROD utilizes a baseline channel, comprised of a non-SILAC labelled digest that serves as a proxy for isolation interference and greatly improves quantification dynamic range. Quantification values of a heavy labelled peptide in that baseline channel are derived from co-fragmented heavy peptides and will be subtracted from the other quantifications. 
    For more information on mePROD, please refer to the original publication <a href="https://doi.org/10.1016/j.molcel.2019.11.010">Klann et al. 2020</a>.
    <br>
    <br><i>
    It can also be used to analyze any combination experiment of SILAC with TMT, if used in the pSILAC mode (see Navigation Bar). The Documentation holds true
    for both workflows, just the baseline related calcualtions are missing in pSILAC compared to mePROD.
    </i></p>
    <h2>Input Files</h2>
    <p align="justify">
        DynaTMT by default uses ProteomeDiscoverer Peptide or PSM file outputs in tab-delimited text. Relevant column headers are automatically extracted from the input file and processed accordingly.
    <br><b>Important Note:</b> DynaTMT assumes heavy labelled modifications to be named according to ProteomeDiscoverer or the custom TMT/SILAC lysine modification, respectively. The custom TMT/Lysine modification is necessary, since search engines are not compatible with two modifications on the same residue at the same time. Thus the heavy lysine as used during SILAC collides with the TMT modification at the lysine. To overcome this problem it is necessary to create a new chemical modification combining the two modification masses. Please name these modification as follows:
    <ul><li>
    Label:13C(6)15N(4) – Heavy Arginine (PD default modification, DynaTMT searches for Label string in modifications)</li>
    <li>TMTK8 – (Modification at lysines, +237.177 average modification mass)</li>
    <li>TMTproK8 -  (Modification at lysines, +312.255 average modification mass)
    </li></ul>
    Alternatively, it is possible to input a any other text file containing Protein Accession or Identifiers in the first column, Ion Injection times in the second column (optional) and Peptide/PSM Modifications in the third column. All following columns are assumed to be TMT intensities, no matter the column names. For plain text files naming of the columns is irrelevant, as long as no duplicate column names are used.
    </p>
    <h2>Normalization</h2>
    <p align="justify">DynaTMT normalizes the samples for their loading, based on both light and heavy peptides. It is assumed that the total protein level does not change between the conditions. The sample loading can be normalized using three different methods:
        <ul><li>
        Total intensity – Sum of all intensities in a channel</li>
        <li>Median – Median intensity of the channels is used to calculate normalization factors</li>
        <li>TMM – Trimmed mean of M values normalization (<a href=”https://doi.org/10.1186/gb-2010-11-3-r25”>publication</a>)
        </li></ul>
    </p>
    <h2>Ion injection time adjustment</h2>
    <p align="justify">During TMT experiments the resulting TMT intensity does not directly reflect the precursor abundance. Lower abundant peptides are injected longer to reach the same number of ions (the AGC target) in the orbitrap. Thus, especially in pSILAC experiments the normalization by just summing TMT abundances creates a bias in the quantifications (for more information please refer to <a href=” https://doi.org/10.1021/acs.analchem.0c01749”>this publication</a>). To account for these differences it is possible to adjust the TMT intensities by their ion injection time. 
        If you want to adjust your data, please make sure to export the Ion injection times for your PSM file. 
    </p>
    <h2>Baseline Index</h2>
    <p align="justify"> This field allows you to specify a custom index for your used baseline channel. Per default it uses the first channel. Please note that the array starts at 0. This means your first channel has the index 0.
    </p>
    <h2>Results</h2>
    <p align="justify"> The results are stored as tab delimited text files in the Results folder of the app. They are named according to the date and the time when the analysis was run.</p>
    <h2>Visualization</h2>
    <p>From the dropdown menu in the visualizations tab all results stored in the results folder can be accessed and boxplots of extracted TMT abundances are drawn. In case of standard ProteomeDiscoverer Input, additional statistics like charge state, average reporter ion intensity or Isolation Interference are extracted and plotted for both heavy and light peptides. The plots are interactive and show relevant statistics and can be easily saved directly from the interface.</p>
