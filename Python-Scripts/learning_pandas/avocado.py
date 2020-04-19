import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('avocado.csv')
df = df.copy()[df['type']=='organic']
df['Date'] = pd.to_datetime(df["Date"])
df.sort_values(by='Date', ascending=True, inplace=True)

"""
#print(df.head())

#print(df["AveragePrice"].head())

albany_df = df[df['region'] == 'Albany']
#albany_df = df.copy()[df['region'] == 'Albany']

albany_df.set_index('Date', inplace=True)
#or
#albany_df = albany_df.set_index('Date')

#print(albany_df.head())
#albany_df.plot()
#albany_df['AveragePrice'].plot()
albany_df.sort_index(inplace=True)
#albany_df['AveragePrice'].rolling(25).mean().plot()
albany_df['price25ma'] = albany_df['AveragePrice'].rolling(25).mean()
#albany_df.dropna().head()
plt.show()
"""
graph_df = pd.DataFrame()
regions = df['region'].unique()

for region in regions:
    region_df = df.copy()[df['region']==region]
    region_df.set_index("Date", inplace=True)
    region_df.sort_index(inplace=True)
    region_df[f'{region}price25ma'] = region_df['AveragePrice'].rolling(25).mean()

    if graph_df.empty:
        graph_df = region_df[[f"{region}price25ma"]]
    else:
        graph_df = graph_df.join(region_df[f'{region}price25ma'])

graph_df.plot(figsize=(8,5), legend=False)
plt.show()
