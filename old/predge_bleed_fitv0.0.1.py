import numpy as numpy
import pandas as pd 
import matplotlib as plt

sf = pd.read_csv("pb_wiglzff.dat", sep="\n",  engine='python')
df = pd.read_csv("012b1_pregg.dat", sep="\n",  engine='python')

df['A'], df['B'] = df[df.columns[0]].str.split('  ', 1).str
sf['A'], sf['B'], sf['I0'], sf['I1'], sf['I2ab']= sf[sf.columns[0]].str.split('\s', 4).str
sf['Ia'], sf['Ib']= sf['I2ab'].str.split('\s', 1).str