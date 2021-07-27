#%% Seeing if the data can be read:
import pandas as pd
path_v= '/Users/anaraquelpengelly/Desktop/imperial_postdoc/visa/variant_data/'

df = pd.read_csv(path_v+'variant_data_2021_07_26.tsv', sep='\t')
#%%
df.head()
df.shape
df.columns
#%% replace the 'not shown data with NA
import numpy as np
#replace cells 'suppressed' or 'None' in the 'Lineage' column
df['Lineage'] = df['Lineage'].replace('None', np.nan)
df['Lineage'] = df['Lineage'].replace('Lineage data suppressed', np.nan)

#%%checking it worked
'Lineage data suppressed' in df['Lineage'].value_counts()

#%%
df.isna().sum()
#%%
df.columns=['date','LAD', 'Lineage', 'counts']
#%%
df['date'] = pd.to_datetime(df['date'])
#%% get london lad codes
ldn_path='/Users/anaraquelpengelly/Desktop/MSc_HDAML/term_3_project/visa/deaths/excess_deaths_dash/per_lad/london_lad_codes'
import pickle
with (open(ldn_path, 'rb')) as l:
    ldn = pickle.load(l)
#%%
variants_london = df[df['LAD'].isin(ldn)]
variants_london = variants_london.groupby(["date", "Lineage"]).agg({'counts':['sum']}).reset_index()
variants_london.columns=['date', 'lineage', 'counts']
variants_london.head()
#%%
variants_london['lineage'].replace('B.1.617.2', 'B.1.617.2_delta', inplace=True)
variants_london['lineage'].replace('B.1.1.7', 'B.1.1.7_alpha', inplace=True)
#%%
def rename_variantes(row):
    if row['lineage'] == 'B.1.617.2_delta':
        name = 'B.1.617.2_delta'
    elif row['lineage'] == 'B.1.1.7_alpha':
        name = 'B.1.1.7_alpha'
    else:
        name = 'Others'
    return name
#%%
variants_london['variants'] = variants_london.apply(rename_variantes, axis=1)
variants_london['variants'].value_counts()
#%%
variants_london.sort_values('date', ascending=True, inplace=True)
#%%
variants_london = variants_london.groupby(['date', 'variants']).agg({'counts': ['sum']}).reset_index()
variants_london.head()
#%%
variants_london.columns = ['date', 'variants', 'counts']
#%%now pivot df
variants_london = variants_london.pivot(index='date', columns='variants', values='counts')
variants_london.reset_index(inplace=True)
variants_london.head()
#%% Lets replace nans for 0
variants_london.replace(np.nan, 0, inplace=True)
#%%
variants_london.rename_axis(None, axis=1, inplace=True)
variants_london.head()
#now get proportion of alpha and percentage of beta of the variants:
variants_london['prop_B.1.1.7_alpha'] = variants_london['B.1.1.7_alpha']/(variants_london['B.1.617.2_delta']+variants_london['B.1.1.7_alpha']+variants_london['Others'])
variants_london['prop_B.1.1.7_delta'] = variants_london['B.1.617.2_delta']/(variants_london['B.1.617.2_delta']+variants_london['B.1.1.7_alpha']+variants_london['Others'])
variants_london['prop_others'] = 1-(variants_london['prop_B.1.1.7_alpha']+variants_london['prop_B.1.1.7_delta'])
variants_london.head()

#%%lets look at the curves
import plotly as plt
import plotly_express as px
#%%

fig= px.scatter(variants_london, x='date', y=variants_london.columns)
fig.show()


#%%now interpolate (not entirely sure that the linear method is the best... maybe polynomial order=2?)
variants_london.set_index('date', inplace=True)
variants_london = variants_london.resample('D').interpolate(method='linear')

#%%
variants_london.reset_index(inplace=True)
variants_london.head()
#%%
fig=px.line(variants_london, x='date', y=variants_london.columns)
fig.show()
#%%
variants_london.to_csv(path_v+'london_variants_2021_07_26.csv', index=False)