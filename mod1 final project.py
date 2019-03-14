# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 10:11:41 2019

@author: james
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
plt.style.use('seaborn')
import statsmodels.api as sm
import statsmodels.formula.api as smf
#%matplotlib inline
#cd('D')
#cd('D:\Users\James\Dropbox (Personal)\CODING\_FLATIRON\Mod1_FinalProject\dsc-1-final-project-online-ds-ft-021119\')
df = pd.read_csv('kc_house_data.csv')   

# Write a function to print out series information to test for categorical 
def check_column(series):
    print(f"Column: df['{series.name}']':")
    print(f"dtype: {series.dtype}")
    print(f"isna: {series.isna().sum()} out of {len(series)} - {round(series.isna().sum()/len(series),3)}%")
    print(f'\nUnique non-na values:') #,df['waterfront'].unique())
    print(series.value_counts())
    

print(df.info())
df = df.drop('id',axis=1)


# Check for columns with null values (remember strings/objects are not counted here)
res = df.isna().sum()
print(res[res>0])

# Recast categories as strings for visualization purposes
df['zipcode'] = df['zipcode'].astype('str')
df['lat'] = df['lat'].astype('str')
df['long'] = df['long'].astype('str')
df['view'] = df['view'].astype('str')
df['waterfront'] = df['waterfront'].astype('str')
df['condition'] = df['condition'].astype('str')
df['grade'] = df['grade'].astype('str')



df['floors'] = df['floors'].astype('category')


## Recast df['date'] as datetime
df['date'] = pd.to_datetime(df['date'])
df['date'].nunique()

#JUST RECASt SQFT_BASEMENT AS FLOAT
df['sqft_basement'].replace('?','0.0',inplace=True)
df['sqft_basement']=df['sqft_basement'].astype('float')



df['log_price'] = np.log(df['price'])
df['log_sqftliving'] = np.log(df['sqft_living'])
df['log_sqftlot'] = np.log(df['sqft_lot'])