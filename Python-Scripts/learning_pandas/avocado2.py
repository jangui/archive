#!/usr/bin/env python3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error

df = pd.read_csv('avocado.csv')

#exploring our data
print(df.head())
print(df.columns)
print(df.dtypes)
print(df.describe(include='all'))

df2 = df[['AveragePrice']]+1
#dealing with missing values
#option 1: replace missing vals with mean, mean or other revelant replacement
mean = df['AveragePrice'].mean()
df['AveragePrice'].replace(np.nan, mean, inplace=True)
#option 2; drop missing vals
df.dropna(subset=['AveragePrice'], axis=0, inplace = True) #drop all rows without val
df.reset_index(drop=True, inplace=True) #reset index after dropping rows

#formatting data
#assume we wanted price in cents not dollars
print(df2.head())
df2['AveragePrice'] = df2['AveragePrice'] * 100
df2.rename(columns={'AveragePrice':'AvgPriceCents'}, inplace=True)
#change data type
df2['AvgPriceCents'] = df2['AvgPriceCents'].astype('int')
print(df2.head())
print(df2.dtypes)

#data normalization / feature scaling
#z score normalization
df2['AvgPriceCents'] = (df2['AvgPriceCents'] - df2['AvgPriceCents'].mean() ) / df2['AvgPriceCents'].std()
print(df2.head())

#binning data
bins = np.linspace(min(df['AveragePrice']), max(df['AveragePrice']), 4)
groups = ['Low Price', 'Mid Price', 'High Price']
df['price_binned'] = pd.cut(df['AveragePrice'], bins, labels=groups, include_lowest = True)

#turn categorial into quantitative data (one-hot encoding)
dummy = pd.get_dummies(df['region'])
pd.concat([df, dummy], axis=1)
df.drop('region', axis=1, inplace=True)

#counting categorial data
regions = df['region'].value_counts().to_frame()
regions.index.name = 'region'
regions.rename(column={'region':'value_count'}, inplace=True)

#grouping data by categorial vals
data = df[['AveragePrice', 'year', 'region']]
grouped_data = data.groupby(['year', 'region'], as_index=False).mean()
df_pivot = grouped_data.pivot(index='region', columns='year')
#plot using heatmap
plt.pcolor(df_pivot, cmap='RdBu')
plt.colorbar()
plt.show()


#calc correlation using scipy
pearson_coef, p_val = stats.pearsonr(df['price'], df['region'])
#heat map of correlation between vars can yield interesting results

#regression plot
import seaborn as sns
sns.regplot(x = 'year', y = 'AveragePrice', data = df)

#box plot
sns.boxplot(x='region', y='AveragePrice', data = df)

#Linear Regression
lm = LinearRegression()
lm.fit(df[['year']], df['price'])

#Multivariate linear regression
lm2 = LinearRegression()
Z = df[['year', 'Volume']]
Y = df['price']
lm2.fit(Z,Y)
prediction = lm2.predict(Z)

"""
Note
use regression and distribution plots to analize if the data can be fitted linearly
and how well it can be fitted
"""

#Polynomial Regression with skilearn pipeline
pipeline = [('scale', StandardScaler()), ('polynomial', PolynomialFeatures(degree=2)), ('model', LinearRegression())]
pipe = Pipeline(pipeline)
pipe.train(Z)
prediction = pipe.predict(Z)
#evaluate prediction
mean_squared_error(df['price'], prediction)

#evaluate model using R^2
r = pipe.score(Z, Y)

