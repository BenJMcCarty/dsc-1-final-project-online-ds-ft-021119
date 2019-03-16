# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 18:06:25 2019

@author: james
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
plt.style.use('seaborn')
import statsmodels.api as sm
import statsmodels.formula.api as smf
df_run = pd.read_csv('test_df.csv')   

# MULTIPLOT
from string import ascii_letters
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import statsmodels.api as sm
import statsmodels.formula.api as smf
import scipy.stats as stats
import statsmodels.stats.api as sms





def multiplot(df):

    sns.set(style="white")

    # Compute the correlation matrix
#     df_corr = df.drop('price',axis=1)
    corr = df.corr()

    # Generate a mask for the upper triangle
    mask = np.zeros_like(corr, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True

    # Set up the matplotlib figure
    f, ax = plt.subplots(figsize=(16, 16))

    # Generate a custom diverging colormap
    cmap = sns.diverging_palette(220, 10, as_cmap=True)

    # Draw the heatmap with the mask and correct aspect ratio
    sns.heatmap(corr, mask=mask, annot=True, cmap=cmap, center=0,
                
    square=True, linewidths=.5, cbar_kws={"shrink": .5}) #
    
    
    
    
# Plots histogram and scatter (vs price) side by side
def plot_hist_scat(df,target='price',stats=True):
    plt.style.use('bmh')
    results = [['column','K_square','p-val']]

    for column in df.describe():
    # for column in df:

        fig = plt.figure(figsize=(8,3) )#plt.figaspect(0.5))#(5,4))
        ax1 = fig.add_subplot(121)
        ax1.hist(df[column],density=True,label = column+' histogram',bins=20)
    #     ax1.kde()
        ax1.set(title=column.capitalize())
        ax1.legend()
    #     plt.show()
        ax2 = fig.add_subplot(122)
        ax2.scatter(x=df[column], y=df[target],label = column+' vs price',marker='.')
        ax2.set(title=column.capitalize())
        ax2.legend()

        fig.tight_layout()
        if stats==True:
            stat, p = normtest(df[column])
#             print(f'Normality test for {column}:K_square = {stat}, p-value = {p}')

            results.append([column,stat, p])
    return pd.DataFrame(results)




# PUTTING TOGETHER THE PREDICTORS TO RUN IN THE REGRESSION
## Last min dummy vars []'cat_grade','cat_zipcode','cat_view','cat_bins_sqft_above','cat_bins_sqft_basement']
dum_grades = pd.get_dummies(df_run['cat_grade'],prefix='gr').iloc[:,:-1]
dum_view = pd.get_dummies(df_run['cat_view'], prefix='view').iloc[:,:-1]
dum_sqft_above = pd.get_dummies(df_run['cat_bins_sqftabove'],prefix='sqftAb').iloc[:,:-1]
dum_sqft_base = pd.get_dummies(df_run['cat_bins_sqftbasement'],prefix='sqftBa').iloc[:,:-1]


# RUNNING K-FOLD VALIDATION WITH STATSMODELS OLS.
# X = df_run.drop(['price','logZ_price'],axis=1)
list_predictors = ['logZ_sqft_living','logZ_sqft_living15','bedrooms','bathrooms','floors']
X = df_run[list_predictors]
X = pd.concat([X,dum_grades,dum_view,dum_sqft_above,dum_sqft_base],axis=1) #dum_bedrooms
y = df_run['logZ_price']




list_predictors = [str(x) for x in X.columns]
# reg_params = ['intercept']
# reg_params.append(list_predictors)
list_predictors.append('intercept')
list_predictors





# DEFINING FUNCTION TO RUN K-FOLD VALIDATION
def k_fold_val(X,y,k=10,QQ=False):
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LinearRegression
    from sklearn import metrics 

    # Run 10-fold cross validation
    i=0
    results = [['set#','R_square_train','MSE_train','R_square_test','MSE_test']]
    residuals= [['y_train','y_test','train_residuals','test_residuals' ]]
                
    num_coeff = X.shape[1]
    
    list_predictors = [str(x) for x in X.columns]
    # reg_params = ['intercept']
    # reg_params.append(list_predictors)
    list_predictors.append('intercept') 
    reg_params = [list_predictors]
    while i <(k+1):
        X_train, X_test, y_train, y_test = train_test_split(X,y) #,stratify=[cat_col_names])


        linreg = LinearRegression()
        linreg.fit(X_train, y_train)


        y_hat_train = linreg.predict(X_train)
        y_hat_test = linreg.predict(X_test)

        train_residuals = y_hat_train - y_train
        test_residuals = y_hat_test - y_test
        
#             fig = sm.graphics.qqplot(train_residuals, dist=stats.norm, line='45', fit=True) 
#             fig=figure(figsize=(12,12)
#             plt.figure()
            

        
        train_mse = metrics.mean_squared_error(y_train, y_hat_train)
        test_mse = metrics.mean_squared_error(y_test, y_hat_test)

        R_sqare_train = metrics.r2_score(y_train,y_hat_train)
        R_square_test = metrics.r2_score(y_test,y_hat_test)

        residuals.append(['y_train','y_test','train_residuals','test_residuals' ])

        results.append([i,R_sqare_train,train_mse,R_square_test,test_mse])
        params_to_add = [x for x in linreg.coef_]
        params_to_add.append(linreg.intercept_)
        reg_params.append(params_to_add)

        i +=1
    if QQ ==True:

        fig, ax = sm.graphics.qqplot(test_residuals, dist=stats.norm, line='45', fit=True)
        ax.set_title('Test Residuals')
        plt.show()
        
        
        
    df_res=pd.DataFrame(results)
    df_reg_params = pd.DataFrame(reg_params)

    r2_test = np.array(df_res.iloc[1:,3]).mean()
    MSE_test = np.array(df_res.iloc[1:,4]).mean()
    
    print(f'For k={k}: mean r2 = {round(r2_test,3)}, mean MSE = {round(MSE_test,3)}')

    return df_res, df_reg_params, residuals





# Output 1:
df_res,df_params, residuals = k_fold_val(X,y,QQ=True)
df_res