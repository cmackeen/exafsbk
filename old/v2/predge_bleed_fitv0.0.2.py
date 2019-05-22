import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
from scipy import optimize

sf = pd.read_csv("pb_wiglzff.dat", sep="\n",  engine='python')
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
p=[.00002,.05,.05,200,.00007]

wvpack = lambda x, *p: np.exp(p[0]*(-1.*(x-p[3])**2)-p[4]*x)*(p[1]*np.cos(p[2]*(x-p[3])))

po=[.00002,.05,.05,200,.00007]

xrang=np.linspace(0,2000,200000)


popt, pcov = optimize.curve_fit(f=wvpack, xdata=sf4['e']-13052,ydata=sf4['re'], p0=p)

wvpack_out = lambda x: np.exp(po[0]*(-1.*(x-po[3])**2)-po[4]*x)*(po[1]*np.cos(po[2]*(x-po[3])))
wvpack_pout = lambda x: np.exp(popt[0]*(-1.*(x-popt[3])**2)-popt[4]*x)*(popt[1]*np.cos(popt[2]*(x-popt[3])))

plt.plot(xrang, wvpack_pout(xrang))
plt.plot(sf4['e']-13052, sf4['re'])
plt.show()
'''
for est in np.linspace(-100,100,500):
	wiggl=[]
	for sc in np.linspace(.1,1,30):
		sc_temp_rdchi=[]
		
		wiggl[1]=sc*sf4['re']
		wiggl[0]=sf4['e']+est
		sc_temp_rdchi.append(spy.stats.chisquare())
'''
#sf['Ia'], sf['Ib']= sf['I2ab'].str.split('\s', 1).str