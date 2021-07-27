#%%
import pandas as pd
import numpy as np
from datetime import date
start = np.datetime64('2020-03-01')
end = np.datetime64(date.today())

#%%
#create daily dates for the wanted period
dates = np.arange(start, end)

#%%
#create df
df=pd.DataFrame(dates, columns=['date'])
df.head()
#%% add the public health measures dates
#self isolation:
self_iso = np.arange(np.datetime64('2020-03-12'), end)
#schools closing:
schools_cl_prim_0 = np.arange(np.datetime64('2020-03-20'), np.datetime64('2020-06-01'))
schools_cl_sec_0 = np.arange(np.datetime64('2020-03-20'), np.datetime64('2020-06-15'))
schools_cl_prim_1 = np.arange('2021-01-06','2021-03-08', dtype='datetime64')
schools_cl_sec_1 = np.arange('2021-01-06','2021-03-08', dtype='datetime64')
#lockdown:
lockdown_0=np.arange(np.datetime64('2020-03-23'), np.datetime64('2020-05-11'))
lockdown_1= np.arange(np.datetime64('2020-11-05'), np.datetime64('2020-12-02'))
lockdown_2=np.arange('2021-01-06', '2021-07-19', dtype='datetime64')
#masks:
masks=np.arange('2020-07-24', '2021-07-26', dtype='datetime64')
#border_control:
border_ctrl=np.arange(np.datetime64('2021-02-15'), end)
#track and trace:
track=np.arange(np.datetime64('2020-05-28'), end)
#vaccination will be included in a different variable

#%% get all dates
schools_prim = np.append(schools_cl_prim_0,schools_cl_prim_1)
schools_sec = np.append(schools_cl_sec_0,schools_cl_sec_1)
lockdown = np.append(lockdown_0,lockdown_1)
lockdown = np.append(lockdown, lockdown_2)
#%% now create binary columns for each measure:
def date_to_binary_masks(row):
    '''takes x = np array of dates'''
    result = 0
    if row['date'] in masks:
        result += 1
    else:
        result += 0
    return result
def date_to_binary_lockdown(row):
    '''takes x = np array of dates'''
    result = 0
    if row['date'] in lockdown:
        result += 1
    else:
        result += 0
    return result

def date_to_binary_track(row):
    '''takes x = np array of dates'''
    result = 0
    if row['date'] in track:
        result += 1
    else:
        result += 0
    return result
    
def date_to_binary_border(row):
    '''takes x = np array of dates'''
    result = 0
    if row['date'] in border_ctrl:
        result += 1
    else:
        result += 0
    return result
def date_to_binary_iso(row):
    '''takes x = np array of dates'''
    result = 0
    if row['date'] in self_iso:
        result += 1
    else:
        result += 0
    return result
def date_to_binary_schools_p(row):
    '''takes x = np array of dates'''
    result = 0
    if row['date'] in schools_prim:
        result += 1
    else:
        result += 0
    return result
def date_to_binary_schools_s(row):
    '''takes x = np array of dates'''
    result = 0
    if row['date'] in schools_sec:
        result += 1
    else:
        result += 0
    return result
#%%
df['lockdown'] = df.apply(date_to_binary_lockdown, axis=1)
df['masks'] = df.apply(date_to_binary_masks, axis=1)
df['track'] = df.apply(date_to_binary_track, axis=1)
df['selfIso'] = df.apply(date_to_binary_iso, axis=1)
df['border_ctrl']=df.apply(date_to_binary_border, axis=1)
df['school_prim'] = df.apply(date_to_binary_schools_p, axis=1)
df['school_sec'] = df.apply(date_to_binary_schools_s, axis=1)

#%%add the school holidays and bank holidays
from datetime import date
import holidays
uk_hol = holidays.UnitedKingdom(years=[2020, 2021])
print('01-01-2021' in uk_hol)
#%%
def get_uk_holi(row):
    x=0
    if row['date'] in uk_hol:
        x+=1
    else:
        x+=0
    return x
#%%
df['bank_holiday'] = df.apply(get_uk_holi, axis=1)
#%% now get the school holidays
#taken from: https://schoolholidays-uk.co.uk/school-holidays-london/
schol_hol_m3=np.arange('2020-02-17', '2020-02-28', dtype='datetime64')
schol_hol_m2=np.arange('2020-04-06', '2020-04-17', dtype='datetime64')
schol_hol_m1=np.arange('2020-05-25', '2020-05-29', dtype='datetime64')
school_hol_0 = np.arange('2020-07-15', '2020-09-01', dtype='datetime64')
school_hol_1=np.arange('2020-10-19', '2020-10-30', dtype='datetime64')
school_hol_2 =np.arange('2020-12-14', '2021-01-04', dtype='datetime64')
school_hol_3 = np.arange('2021-02-15', '2021-02-19', dtype='datetime64')
school_hol_4 = np.arange('2021-03-29', '2021-04-19', dtype='datetime64')
school_hol_5 = np.arange('2021-05-31', '2021-06-04', dtype='datetime64')
school_hol_6 = np.arange('2021-07-26', '2021-09-01', dtype='datetime64')

school_hols = np.concatenate([school_hol_0, schol_hol_m1,schol_hol_m2,schol_hol_m3,
school_hol_1, school_hol_2, school_hol_3,school_hol_4, school_hol_5, school_hol_6])

#%%def function:
def get_school_holi(row):
    x=0
    if row['date'] in school_hols:
        x+=1
    else:
        x+=0
    return x
#create column:
df['school_holiday'] = df.apply(get_school_holi, axis=1)

#%%now get weekdays and weekends
#bus_day versus weekend

bus_day = np.is_busday(dates)
df['is_busday'] = bus_day.tolist()
def to_binary(row):
    x=0
    if row['is_busday']:
        x+=1
    else:
        x+=0
    return x
df['is_busday'] = df.apply(to_binary, axis=1)
#%% now days of the week:
df['dow'] = df['date'].dt.dayofweek
#%%
df.to_csv('PH_measures_london.csv', index=False)

