#!/usr/bin/env python3
import pandas as pd
import numpy as np

df = pd.read_csv('min_wage_data.csv', encoding='latin')
#df.to_csv('min_wage_data.csv', encoding='utf-8')

print(df.head())

#-------organizing the data we are actually interested in-------
#group data by state and index by year
gb = df.groupby("State")
print(gb.get_group("Alabama").set_index("Year").head())

#create DF of each states lowest min wage per year
#option 1
act_min_wage = pd.DataFrame()
for name, group in df.groupby("State"):
    if act_min_wage.empty:
        act_min_wage = group.set_index("Year")[["Low.2018"]].rename(columns={"Low.2018":name})
    else:
        act_mine_wage = act_min_wage.join(group.set_index("Year")[["Low.2018"]].rename(columns={"Low.2018":name}))

#option 2
act_min_wage = df.pivot(index='Year', columns='State', values='Low.2018')

print(act_min_wage.head())

print(act_min_wage.describe()) #gives us info about mean low hig std var etc

print(act_min_wage.corr().head()) #gives correction between states data

issue_df = df[df['Low.2018']==0]
print(issue_df)

print(issue_df['State'].unique())

#------dropping bad data and checking if done corecctly--------
#set 0's to not a number and drop
min_wage_corr = act_min_wage.replace(0, np.NaN).dropna(axis=1) #axis 1 refers to column, 0 refers to rows

#check if there was actual data
for problem in issue_df['State'].unique():
    if problem in min_wage_corr.columns:
        print("we're missing data here")

grouped_issues = issue_df.groupby("State")
print(grouped_issues.get_group("Alabama").head(3))

grouped_issues.get_group("Alabama")['Low.2018'].sum() #check if col sum is actuall 0

#check if sum of each column is 0 or if we miseed something
for state, data in grouped_issues:
    if data['Low.2018'].sum() != 0:
        print('We missed something!')
