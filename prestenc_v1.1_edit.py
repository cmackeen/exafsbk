#edited from Cam's code
#by Jason Gruzdas jgruzdas@ucsc.edu, jasongruzdas@gmail.com 2/2018
#cut off headers of input files for before reduction, put headers back
#use os bash comands and outputs to 0**b*gg_pre_adjusted.dat
# "#J:" new functionality, or note Jason added
#3/18: run over batch of files
import matplotlib as mpl
mpl.use('Agg')
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

#-----------------------------------------------------------------------------------------------
# GLOBAL VARIABLES
file_name = ""
E_stenc = 0
E1 = 0

ned = 0
inputFlag = 0
plotFlag = 0

#-----------------------------------------------------------------------------------------------
print("Type main() to start.")

def main():
    #Flag 0 means no inputs for file_name, E_stenc, E1
    global inputFlag
    
    global file_name
    file_name = raw_input('Name of Batch file? ')
    
    global E_stenc
    E_stenc = float(input('Edge of interest for the STENCIL: '))
    
    global E1
    E1 = float(input('Edge of interest for the DATA: '))
    
    loop()

#-----------------------------------------------------------------------------------------------

def interface():
    global inputFlag
    # Check to see if user already has inputs in order to print the list of options once
    if not inputFlag:
	print("To see the plot, enter 'plot'.")
	
	inputFlag = 1

    global userInput
    userInput = input("Command: ")
    # Only when entering the 'end' command will "check_command" return false so that
    # the interface ends otherwise "check_command" returns true and will call
    # interface again so that they can enter other measurment commands
    if check_command(userInput):
	interface()




#-----------------------------------------------------------------------------------------------

###J: Variables:
#verbose?
verbose = bool(True)
# set number of rows of header (default 14):
header_length = 16
# length to cut data to
cut_length = 21
# delete temp header file and data file after cominbed?
cleanup = bool(True)

def loop():
#inport batch list:
#batchlist = pd.read_csv("stencdat.inp", sep="\s", header=None, engine='python')
    batchlist = pd.read_csv(file_name, sep="\s", header=None, engine='python')
#will loop with length of list:
    batchlist_length = len(batchlist)

#sf = pd.read_csv("pbwig_zeros.dat", sep="\n",  engine='python')


#J: old df for file w/o header:
#df = pd.read_csv("013_cut.dat", sep="\n",  engine='python')
#J: new df for file w/ header:
#df = pd.read_csv("013_cut-w-header.dat", skiprows=header_length, sep="\n", engine='python')

#J: for loop:

    for i in range(0, batchlist_length):
        #J: new-new df for file w/ header and in batch:
        #Br data to fit
        df = pd.read_csv(batchlist.iloc[i,0], skiprows=header_length, sep="\n", engine='python')
        #Pb simmulated wiggle
        sf= pd.read_csv(batchlist.iloc[i,1], sep="\n", header=18, engine='python')
        print('-_-_-_-_-_-_')
        print(batchlist.iloc[i,0])
        print(batchlist.iloc[i,1])
        print ('**********')
        #J: cut down to length:
        df = df[:cut_length]
        #J: df_header is header w/o data (minus 1 b/c 2nd line starts on 0 index)
        df_header = pd.read_csv(batchlist.iloc[i,0], nrows=(header_length-1), sep="\n", engine='python')

        #batchlist.iloc[0,0]
        #test = pd.read_csv(batchlist.iloc[0,0], skiprows=header_length, sep="\n", engine='python')

        df2 = df[df.columns[0]].str.split()
        df3=pd.DataFrame(index=[list(zip(*df2)[0])])
        df4=df3.reset_index()
        df4.columns=['e']
        df4['amp']=list(zip(*df2)[1])
        df4=df4.astype(float)

        plt.plot(df4['e'],df4['amp'], label=' data')
        plt.show()

        sf2 = sf[sf.columns[0]].str.split()
        sf3=pd.DataFrame(index=[list(zip(*sf2)[0])])
        sf4=sf3.reset_index()
        sf4.columns=['k']

    # ahd to edit 1->0 ????
        sf4['re']=list(zip(*sf2)[1])
        sf4=sf4.astype(float)
    #sf4['e']=(sf4['k']**2)*3.81+12052
        sf4['e']=(sf4['k']**2)*(1/.512393**2)+E_stenc

    #recently fixed to put '.512' in the numerator!
        sf4['re2']=(sf4['re']*(.512393**2/(2*sf4['k'])))
#------------------------------------------------------------
# This will try to automatically set the plot limits
        value = min(sf4['e'], key=lambda x:abs(x-E1))
        #Change sf4['e'] into a list to use .index()
        myList = sf4['e'].tolist()
        value_index = myList.index(value)#Gives index value in df['amp'] that matches index 
        ylim_list = [sf4['re'][i] for i in range(value_index-150, value_index+151)]
#------------------------------------------------------------

        plt.plot(sf4['e'],sf4['re'], label='raw stencil')
	plt.xlim(E1-400, E1+400)
	plt.ylim(min(ylim_list), max(ylim_list))
        plt.show()
        sf4['e'][0]=0
        sf4['re2'][0]=0
        smooth_wv=interpolate.interp1d(sf4['e'],sf4['re2'],kind='cubic')
    #E1 is the edge of interest for the DATA
    #p=[1.,0.]
    
        pp=[30,.02]

    

        p=[30,3.0]
        slide_pump=lambda x, *p: p[0]*smooth_wv(x+p[1])
        popt, pcov = optimize.curve_fit(f=slide_pump, xdata=df4['e'], ydata=df4['amp'], p0=p,maxfev=9000)
        print(popt)

        xrang=np.linspace(E_stenc-200, E1, 2000)
        slide_pout=lambda x, *p: popt[0]*smooth_wv(x+popt[1])
    
    
    #plt.plot(smooth_wv.x, smooth_wv(smooth_wv.x), label='stencil interp')
    #plt.plot(sf4['e'][::6], sf4['re2'][::6], 'o', alpha=0.4, label='stencil_data')
        plt.plot(xrang, slide_pout(xrang),ms=3., label='stenc_fit') 
        plt.legend(loc=4)
       


        '''
    
        plt.xlim([13200,13900])
        plt.ylim([-.03, .03])
        plt.xlabel('Energy (eV)')
        plt.ylabel('abs.')
        plt.title('Pre_edge Br data fit with simulated Pb high k background')
        plt.legend(loc=4)
        '''
        plt.show()

        df4['dif']=slide_pout(df4['e'])-df4['amp']

    #J: added skiprow of header to this line:
        findf= pd.read_csv(batchlist.iloc[i,0], skiprows=header_length, sep="\n",  engine='python')
        findf2 = findf[findf.columns[0]].str.split()
        findf3=pd.DataFrame(index=[list(zip(*findf2)[0])])
        findf4=findf3.reset_index()
        findf4.columns=['e']
        findf4['amp']=list(zip(*findf2)[1])
        findf4=findf4.astype(float)
        '''
        plt.plot(findf4['e'],findf4['amp'])
        plt.xlim([12200,14900])
        plt.plot(sf4['e']-popt[1],popt[0]*sf4['re2'],ms=3)
        plt.plot(xrang, slide_pout(xrang),ms=3.)
        plt.ylim([-.3, .3])
        plt.plot(findf4['e'],findf4['dif'])
        plt.show()
        '''
        findf4['dif']=findf4['amp']-slide_pout(findf4['e'])

        final_out =pd.DataFrame(columns=['e','amp'])
        final_out['e']=findf4['e']
        final_out['amp']=findf4['dif']
        final_out['zeds']=[0. for c in range(len(findf4['dif']))]
    #J: this line has been edited to outout to 'final_data', and not print column
        final_out.to_csv('final_data', sep=" ", index=False, index_label=False, header=False)

    #J: save header to temp file:
        df_header.to_csv('final_header', sep="\n", index=False, index_label=False)

    #J: combine files and delete temp files:
        cmd="cat final_header final_data > "+(batchlist.iloc[i,0])[0:11]+"_adjusted"
    #os.system("cat final_header final_data > 013_adjusted-w-header")
        os.system(cmd)
        if verbose: print batchlist.iloc[i,0]," --> ",(batchlist.iloc[i,0])[0:11]+"_adjusted"
        if cleanup: os.system("rm final_header final_data")

#-----------------------------------------------------------------------------------------------
