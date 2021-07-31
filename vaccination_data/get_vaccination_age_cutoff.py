#%%
from matplotlib.pyplot import get
import numpy as np 
import pandas as pd
#%%
from datetime import date
today =date.today()
today = np.datetime64(today)
#%%
def get_dates(start, end):
    x=np.arange(start, end, dtype='datetime64')
    return x
#%%
gp_0=get_dates(start='2020-12-08' , end='2021-01-18')#Residents in a care home for older adults and their carers; and all aged 80 and over
gp_1=get_dates('2021-01-18', '2021-03-01')# all 70 and over and clinically vulnerable
gp_2=get_dates('2021-03-01', '2021-03-17')# all 60 and over
gp_3=get_dates('2021-03-17', '2021-04-30')# all 50 and over
gp_4=get_dates('2021-04-30', '2021-05-26')# all 40 and over     
gp_5=get_dates('2021-05-26', '2021-06-18')#all 30 and over
gp_6=get_dates(np.datetime64('2021-06-18'), today)#all 18 and over 
#%%
gps=[gp_0, gp_1, gp_2, gp_3, gp_4, gp_5, gp_6]
#%%

cats=['ovr_80', 'ovr_70', 'ovr_60', 'ovr_50', 'ovr_40', 'ovr_30', 'ovr_18']
#%% Make df
start = np.datetime64('2020-03-01')
end = np.datetime64(date.today())
dates = np.arange(start, end)
df=pd.DataFrame(dates, columns=['date'])
df.head()
#%% Make function:
def get_priority_gp(row):
    x =''
    for i in range(len(gps)):
        if row['date'] in gps[i]:
            x+=(cats[i])
    return x

#%%apply function:
df['prio_vacc_gps'] = df.apply(get_priority_gp, axis=1)

# %%
df.replace('', np.nan, inplace=True)
df.head()
#%%now merge with the vaccination numbers:
vacci = pd.read_csv('/Users/anaraquelpengelly/Desktop/imperial_postdoc/visa/vaccination_data/london_vaccination_2021_07_26.csv')
vacci = pd.concat([vacci, df])
#%%
vacci.to_csv('/Users/anaraquelpengelly/Desktop/imperial_postdoc/visa/vaccination_data/london_vaccination_age_gps2021_07_26.csv', index=False)
