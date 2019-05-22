import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
from scipy import optimize
from scipy import special
from scipy import interpolate


sf = pd.read_csv("pbwig_zeros.dat", sep="\n",  engine='python')
df = pd.read_csv("013b1gg_pre.dat", sep="\n",  engine='python')

df2 = df[df.columns[0]].str.split()
df3=pd.DataFrame(index=[list(zip(*df2)[0])])
df4=df3.reset_index()
df4.columns=['e']
df4['amp']=list(zip(*df2)[1])
df4=df4.astype(float)
#plt.plot(df4['e'],df4['amp'])
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
#plt.plot(sf4['e'],sf4['re'])
#plt.show()
sf4['e'][0]=0
sf4['re'][0]=0
smooth_wv=interpolate.interp1d(sf4['e'],sf4['re'],kind='cubic', fill_value="extrapolate")
plt.plot(smooth_wv.x+200, smooth_wv(smooth_wv.x))
plt.plot(sf4['e'][::6], sf4['re'][::6], 'o', alpha=0.4)
plt.show()

'''
p=[.1,50]
wiggl = lambda x, *p: np.exp(p[0]*(-1*x**2))*(p[1]*np.



popt, pcov = optimize.curve_fit(f=wvpack, xdata=sf4['e']-13052,ydata=sf4['re'], p0=p)
wvpack_out = lambda x: np.exp(popt[0]*(-1*x**2))*(popt[1]*np.cos(popt[2]*x))

'''

#sf['Ia'], sf['Ib']= sf['I2ab'].str.split('\s', 1).str
