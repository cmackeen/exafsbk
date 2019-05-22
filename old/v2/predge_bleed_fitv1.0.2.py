import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
from scipy import optimize
from scipy import special
from scipy import interpolate

from matplotlib.backends.backend_pdf import PdfPages
#pp = PdfPages('multipage.pdf')

sf = pd.read_csv("pbwig_zeros.dat", sep="\n",  engine='python')
df = pd.read_csv("013_cut.dat", sep="\n",  engine='python')

df2 = df[df.columns[0]].str.split()
df3=pd.DataFrame(index=[list(zip(*df2)[0])])
df4=df3.reset_index()
df4.columns=['e']
df4['amp']=list(zip(*df2)[1])
df4=df4.astype(float)
plt.plot(df4['e'],df4['amp'])
#plt.xlim([13050,13480])
#plt.ylim([-.06,.06])
#plt.show()

sf2 = sf[sf.columns[0]].str.split()
sf3=pd.DataFrame(index=[list(zip(*sf2)[0])])
sf4=sf3.reset_index()
sf4.columns=['k']
sf4['re']=list(zip(*sf2)[1])
sf4=sf4.astype(float)
#sf4['e']=(sf4['k']**2)*3.81+12052
sf4['e']=(sf4['k']**2)*3.81+13052
sf4['re2']=(sf4['re']*(1/(8*sf4['k'])))
#plt.plot(sf4['e'],sf4['re'])
#plt.show()
sf4['e'][0]=0
sf4['re2'][0]=0
smooth_wv=interpolate.interp1d(sf4['e'],sf4['re2'],kind='cubic')
#plt.plot(smooth_wv.x, smooth_wv(smooth_wv.x))
#plt.plot(sf4['e'][::6], sf4['re'][::6], 'o', alpha=0.4)
#plt.show()

p=[1.,0.]
slide_pump=lambda x, *p: p[0]*smooth_wv(x+p[1])

popt, pcov = optimize.curve_fit(f=slide_pump, xdata=df4['e'], ydata=df4['amp'], p0=p,maxfev=2800)
xrang=np.linspace(11000, 15000, 2000)
slide_pout=lambda x, *p: popt[0]*smooth_wv(x+popt[1])
plt.plot(xrang, slide_pout(xrang),ms=3.)
plt.xlim([13200,13900])
plt.ylim([-.03, .03])
plt.xlabel('Energy (eV)')
plt.ylabel('abs.')
plt.title('Pre_edge Br data fit with simulated Pb high k background')
plt.legend(loc=4)


df4['dif']=slide_pout(df4['e'])-df4['amp']
plt.plot(df4['e'],df4['dif'])
pp=plt.show()


findf= pd.read_csv("013b1gg_pre.dat", sep="\n",  engine='python')
findf2 = findf[findf.columns[0]].str.split()
findf3=pd.DataFrame(index=[list(zip(*findf2)[0])])
findf4=findf3.reset_index()
findf4.columns=['e']
findf4['amp']=list(zip(*findf2)[1])
findf4=findf4.astype(float)
plt.plot(findf4['e'],findf4['amp'])
plt.xlim([12200,14900])
plt.plot(sf4['e']-popt[1],popt[0]*sf4['re2'],ms=3)
plt.plot(xrang, slide_pout(xrang),ms=3.)
plt.ylim([-.3, .3])
findf4['dif']=findf4['amp']-slide_pout(findf4['e'])
plt.plot(findf4['e'],findf4['dif'])
plt.show()

final_out =pd.DataFrame(columns=['e','amp'])
final_out['e']=findf4['e']
final_out['amp']=findf4['dif']
final_out.to_csv('013_adjusted', sep=" ", index=False, index_label=False)