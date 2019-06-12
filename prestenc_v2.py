#! /usr/bin/env python2.7

#edited from Cam's code
#cut off headers of input files for before reduction, put headers back
#use os bash comands and outputs to 0**b*gg_pre_adjusted.dat
# "#J:" new functionality, or note Jason added
#batch'd by Jason Gruzdas jgruzdas@ucsc.edu, jasongruzdas@gmail.com 2/2018
#3/18: run over batch of files


import matplotlib as mpl

mpl.use('TkAgg')
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
from scipy import optimize
from scipy import special
from scipy import interpolate

from matplotlib.backends.backend_pdf import PdfPages
#pp = PdfPages('multipage.pdf')

#J: import os comands to combine header file and final_out
import os
import argparse



def main():
    parser=argparse.ArgumentParser(description="Takes input 2 column (tab sep) list, expicitly titled 'stencdat.inp'. Left column is data files to be corrected, Right column is simulated ks 'stencil' files. Cheers  ")
    parser.add_argument("-es",help="Energy of the stencil's edge [eV] (the lower energy edge tat bleeds into edge of interest)" ,dest="e_stenc", type=float, required=True)
    parser.add_argument("-e1",help="Edge of interest [eV] (Default=auto from max edge slope" ,dest="e1", type=float, default=37)
    parser.set_defaults(func=run)
    args=parser.parse_args()
    args.func(args)


#-----------------------------------------------------------------------------------------------



# set number of rows of header (default 14):
header_length = 14
# length to cut data to
cut_length = 25
cut1_length = 125
# delete temp header file and data file after cominbed?
cleanup = bool(True)

def run(args):

    E_stenc = args.e_stenc # these match the "dest": dest="input"
    E1 = args.e1 # from dest="output"
    file_name='stencdat.inp'
    #E1=22121.5
    #e_stenc=21761.5

    #inport batch list:
    batchlist = pd.read_csv(file_name, sep="\t", header=None, engine='python')
    #will loop with length of list:
    batchlist_length = len(batchlist)

    for i in range(0, batchlist_length):
        #J: new-new df for file w/ header and in batch:
        #Br data to fit
        df = pd.read_csv(batchlist[0][i], skiprows=header_length, sep="\n", engine='python')
        #Pb simmulated wiggle
        sf= pd.read_csv(batchlist[1][i], sep="\n", header=18, engine='python')
        print('-_-_-_-_-_-_')
        print(batchlist[0][i])
        print(batchlist[1][i])
        print ('**********')
        #J: cut down to length:
        df = df[:cut1_length]

        #J: df_header is header w/o data (minus 1 b/c 2nd line starts on 0 index)
        df_header = pd.read_csv(batchlist[0][i], nrows=(header_length-1), sep="\n", engine='python')

        #batchlist.iloc[0,0]
        #test = pd.read_csv(batchlist.iloc[0,0], skiprows=header_length, sep="\n", engine='python')

        df2 = df[df.columns[0]].str.split()
        df3=pd.DataFrame(index=[list(zip(*df2)[0])])
        df4=df3.reset_index()
        df4.columns=['e']
        df4['amp']=list(zip(*df2)[1])
        df4=df4.astype(float)
        df4['diff']=df4['amp'].diff()
        if E1 == 37:
            E1=df4['e'][df4['diff'].idxmax()]
        df4 = df4[:cut_length]
        
        print(E1)
        
        print('==========')

        

        sf2 = sf[sf.columns[0]].str.split()
        sf3=pd.DataFrame(index=[list(zip(*sf2)[0])])
        sf4=sf3.reset_index()
        sf4.columns=['k']

        sf4['re']=list(zip(*sf2)[1])
        sf4=sf4.astype(float)
        sf4['e']=(sf4['k']**2)*(1/.512393**2)+E_stenc
        
        #option to used amplitude scaled by jacobian of k->e variable convention
        sf4['re2']=(sf4['re']*(.512393**2/(2*sf4['k'])))
        
        # This will try to automatically set the plot limits
        value = min(sf4['e'], key=lambda x:abs(x-E1))
        #Change sf4['e'] into a list to use .index()
        myList = sf4['e'].tolist()
        value_index = myList.index(value)#Gives index value in df['amp'] that matches index 
        ylim_list = [sf4['re'][jj] for jj in range(value_index-150, value_index+151)]
#------------------------------------------------------------

        #plt.plot(sf4['e'],sf4['re'], label='raw stencil')
        plt.xlim(E1-300, E1+200)
        plt.ylim(1.2*min(ylim_list), 1.2*max(ylim_list))
        sf4['e'][0]=0
        sf4['re'][0]=0
        smooth_wv=interpolate.interp1d(sf4['e'],sf4['re'],kind='cubic')
 
        pp=[30,.02]

    

        p=[.2,0.0]
        slide_pump=lambda x, *p: p[0]*p[0]*smooth_wv(x+p[1])
        popt, pcov = optimize.curve_fit(f=slide_pump, xdata=df4['e'], ydata=df4['amp'], p0=p,maxfev=99000)
        
        print(str(popt[0]) + '     amplitude factor to fit stencil to pre-edge')

        print(str(popt[1]) + '    stencil energy shift in eV (negative is right shift, positive is left)')

        xrang=np.linspace(E_stenc-200, E1+200, 2000)
        slide_pout=lambda x, *p: popt[0]*smooth_wv(x+popt[1])
    

        plt.plot(xrang, slide_pout(xrang),ms=3., label='stenc_fit',linewidth=3.0) 
       


        

        df4['dif']=slide_pout(df4['e'])-df4['amp']

        #J: added skiprow of header to this line:
        findf= pd.read_csv(batchlist[0][i], skiprows=header_length, sep="\n",  engine='python')
        findf2 = findf[findf.columns[0]].str.split()
        findf3=pd.DataFrame(index=[list(zip(*findf2)[0])])
        findf4=findf3.reset_index()
        findf4.columns=['e']
        findf4['amp']=list(zip(*findf2)[1])
        findf4=findf4.astype(float)
        
        plt.plot(findf4['e'],findf4['amp'],label='data in', linewidth=3.0)
        
        findf4['dif']=findf4['amp']-slide_pout(findf4['e'])
        plt.plot(findf4['e'],findf4['dif'],label='data out', linewidth=3.0)
        final_out =pd.DataFrame(columns=['e','amp'])
        final_out['e']=findf4['e']
        final_out['amp']=findf4['dif']
        plt.legend(loc=4)

        plt.show()
        final_out['zeds']=[0. for c in range(len(findf4['dif']))]
     #J: this line has been edited to outout to 'final_data', and not print column
        final_out.to_csv('final_data', sep=" ", index=False, index_label=False, header=False)

    #J: save header to temp file:
        df_header.to_csv('final_header', sep="\n", index=False, index_label=False)

    #J: combine files and delete temp files:
        cmd="cat final_header final_data > "+(batchlist[0][i])[0:9]+"_adjusted"
    #os.system("cat final_header final_data > 013_adjusted-w-header")
        os.system(cmd)
        print batchlist.iloc[i,0]," --> ",(batchlist.iloc[i,0])[0:9]+"_adjusted"
        os.system("rm final_header final_data")
    
        

if __name__=="__main__":
    main()


