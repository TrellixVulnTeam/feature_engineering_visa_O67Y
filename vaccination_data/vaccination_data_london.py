#%%
import pandas as pd
import numpy as np
#%%
path='/Users/anaraquelpengelly/Desktop/imperial_postdoc/visa/vaccination_data/'
data = pd.read_csv(path+'data_2021-Jul-26.csv')
data.head()
#%%select wanted columns:
data = data[['date', 'cumPeopleVaccinatedFirstDoseByVaccinationDate', 'cumPeopleVaccinatedSecondDoseByVaccinationDate']]
data.columns = ['date', 'cumFirstDose', 'cumSecondDose']
data.date = pd.to_datetime(data.date)
#%% replace NAs with 0 in the cumseconddose
data.cumSecondDose= data.cumSecondDose.replace(np.nan, 0)
#%%save data
data.to_csv('london_vaccination_2021_07_26.csv', index=False)
#%%
path_v= '/Users/anaraquelpengelly/Desktop/imperial_postdoc/visa/variant_data/'
variants = pd.read_csv('variant_data_2021_07_09.csv')