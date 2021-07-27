#%%
#1-scrape all the dayly files from the website
#2-then open them all at the right tab
#3-then get the totals (first dose, second dose etc)
#4-then copncat with the next day

#%%
from bs4 import BeautifulSoup
import requests
import urllib.request
import time
#%%

url ='https://www.england.nhs.uk/statistics/statistical-work-areas/covid-19-vaccinations/covid-19-vaccinations-archive/'
response=requests.get(url)
#%%
text = response.text
status= response.status_code
#%%
soup = BeautifulSoup(text, 'html.parser')
#%%
xls_links=soup.find(class_='page-content')
#%%
xls_links_list = xls_links.find_all('a')
#%%
for element in xls_links_list:
    print(element.prettify())

#%%
all_links=[]
for element in xls_links_list:
    links = element.get('href')
    all_links.append(links)

#%%
all_names = []
for element in xls_links_list:
    names= element.contents[0]
    all_names.append(names)
all_names
#%%
daily_names= [e for e in all_names if 'daily announced vaccinations' in e]
daily_names
#%%
#now get the daily vaccination links

daily_vacc =[e for e in all_links if 'COVID-19-daily-announced-vaccinations' in e]

#%%
daily_vacc
#%%Now make function to open each of the links and get 
# the totals per LAD and the date and add to a df
import pandas as pd
import numpy as np
df=pd.read_excel(daily_vacc[0], sheet_name='Vaccinations by LTLA and Age ', skiprows=12)
df = df[['UTLA Code', 'UTLA Name', 'LTLA Code4', 'LTLA Name4', 'Total 1st Doses8', 'Total 2nd Doses8', 'Cumulative Total Doses (1st and 2nd doses) to Date8']]
df = df[3:]
#%%
df.head()
df['date'] = daily_names[0][38:]
#%%
df['date'] = pd.to_datetime(df['date'])
#%%
df=df[:-14]

#%%
def get_df(l, n):
    df=pd.read_excel(l, sheet_name='Vaccinations by LTLA and Age ', skiprows=12)
    df = df[['UTLA Code', 'UTLA Name', 'LTLA Code4', 'LTLA Name4', 'Total 1st Doses8', 'Total 2nd Doses8', 'Cumulative Total Doses (1st and 2nd doses) to Date8']]
    df = df[3:]
    df['date'] = n[38:]
    df['date'] = pd.to_datetime(df['date'])
    df=df[:-14]
    return df
#%%
df1=get_df(daily_vacc[1],daily_names[1])
#%%
df2=get_df(daily_vacc[2],daily_names[2])
#%%
df3=get_df(daily_vacc[3],daily_names[3])
df3.head()
#%%
df3.tail()
#%%
df4=pd.read_excel(daily_vacc[4], sheet_name='Vaccinations by LTLA and Age ', skiprows=11)
df4 = df[['UTLA Code', 'UTLA Name', 'LTLA Code4', 'LTLA Name4', 'Total 1st Doses8', 'Total 2nd Doses8', 'Cumulative Total Doses (1st and 2nd doses) to Date8']]
df4 = df[3:]
df4['date'] = daily_names[4][38:]
df4['date'] = pd.to_datetime(df4['date'])
df4.tail()

#%%
df5=get_df(daily_vacc[5],daily_names[5])
#%%
len(daily_vacc)
#%%
df.tail(20)
#%%
df6=df_list[0]
df6=df6[:-14]
df6.tail()
#%%
df8=df_list[0]
df9=df_list[1]
df10=df_list[2]
df11=df_list[3]
#%%
df_list=[]

for i in range(13):
    df= pd.read_excel(daily_vacc[i], sheet_name='Vaccinations by LTLA and Age ', skiprows=12)
    if 'UTLA Code' in list(df.columns):
        df = df[['UTLA Code', 'UTLA Name', 'LTLA Code4', 'LTLA Name4', 'Total 1st Doses8', 'Total 2nd Doses8', 'Cumulative Total Doses (1st and 2nd doses) to Date8']]
        df = df[3:]
        df['date'] = daily_names[i][38:]
        df['date'] = pd.to_datetime(df['date'])
        df=df[:-14]
        df_list.append(df)
    elif 'UTLA Code' not in list(df.columns):
        try:
            df= pd.read_excel(daily_vacc[i], sheet_name='Vaccinations by LTLA and Age ', skiprows=11)
            df = df[['UTLA Code', 'UTLA Name', 'LTLA Code4', 'LTLA Name4', 'Total 1st Doses8', 'Total 2nd Doses8', 'Cumulative Total Doses (1st and 2nd doses) to Date8']]
            df = df[3:]
            df['date'] = daily_names[i][38:]
            df['date'] = pd.to_datetime(df['date'])
            df_list.append(df)
        except KeyError:
            df= pd.read_excel(daily_vacc[i], sheet_name='Vaccinations by LTLA and Age ', skiprows=10)
            df = df[['UTLA Code', 'UTLA Name', 'LTLA Code4', 'LTLA Name4', 'Total 1st Doses8', 'Total 2nd Doses8', 'Cumulative Total Doses (1st and 2nd doses) to Date8']]
            df = df[3:]
            df['date'] = daily_names[i][38:]
            df['date'] = pd.to_datetime(df['date'])
            df_list.append(df)



#%%
len(df_list) # number 14 a problem
#%%
df14=pd.read_excel(daily_vacc[14], sheet_name='Vaccinations by LTLA and Age ', skiprows=10)
df14 = df14[['UTLA Code', 'UTLA Name', 'LTLA Code5', 'LTLA Name5', 'Total 1st Doses9', 'Total 2nd Doses9', 'Cumulative Total Doses (1st and 2nd doses) to Date9']]
df14 = df14[3:]
df14['date'] = daily_names[14][38:]
df14['date'] = pd.to_datetime(df14['date'])
df14.head()

#%% In the end , the function did not work because the structure of the files was different ! 
df_list1=[]

for i in range(15,len(daily_vacc)):
    df= pd.read_excel(daily_vacc[i], sheet_name='Vaccinations by LTLA and Age ', skiprows=12)
    if 'UTLA Code' in list(df.columns):
        df = df[['UTLA Code', 'UTLA Name', 'LTLA Code4', 'LTLA Name4', 'Total 1st Doses8', 'Total 2nd Doses8', 'Cumulative Total Doses (1st and 2nd doses) to Date8']]
        df = df[3:]
        df['date'] = daily_names[i][38:]
        df['date'] = pd.to_datetime(df['date'])
        df=df[:-14]
        df_list1.append(df)
    elif 'UTLA Code' not in list(df.columns):
        try:
            df= pd.read_excel(daily_vacc[i], sheet_name='Vaccinations by LTLA and Age ', skiprows=11)
            df = df[['UTLA Code', 'UTLA Name', 'LTLA Code4', 'LTLA Name4', 'Total 1st Doses8', 'Total 2nd Doses8', 'Cumulative Total Doses (1st and 2nd doses) to Date8']]
            df = df[3:]
            df['date'] = daily_names[i][38:]
            df['date'] = pd.to_datetime(df['date'])
            df_list1.append(df)
        except KeyError:
            df= pd.read_excel(daily_vacc[i], sheet_name='Vaccinations by LTLA and Age ', skiprows=10)
            df = df[['UTLA Code', 'UTLA Name', 'LTLA Code4', 'LTLA Name4', 'Total 1st Doses8', 'Total 2nd Doses8', 'Cumulative Total Doses (1st and 2nd doses) to Date8']]
            df = df[3:]
            df['date'] = daily_names[i][38:]
            df['date'] = pd.to_datetime(df['date'])
            df_list1.append(df)

#%%
df31=pd.read_excel(daily_vacc[31], sheet_name='Vaccinations by LTLA and Age ', skiprows=12)
df31.head()
#%%

df31 = df31[['UTLA Code', 'UTLA Name', 'LTLA Code3', 'LTLA Name3', 'Total 1st Doses7', 'Total 2nd Doses7', 'Cumulative Total Doses (1st and 2nd doses) to Date7']]
df31 = df31[3:]
df31['date'] = daily_names[31][38:]
df31['date'] = pd.to_datetime(df31['date'])
df31=df31[:-14]
df31.tail(20)
#%%
df_list2=[]

for i in range(32,len(daily_vacc)):
    df= pd.read_excel(daily_vacc[i], sheet_name='Vaccinations by LTLA and Age ', skiprows=12)
    if 'UTLA Code' in list(df.columns):
        df = df[['UTLA Code', 'UTLA Name', 'LTLA Code4', 'LTLA Name4', 'Total 1st Doses8', 'Total 2nd Doses8', 'Cumulative Total Doses (1st and 2nd doses) to Date8']]
        df = df[3:]
        df['date'] = daily_names[i][38:]
        df['date'] = pd.to_datetime(df['date'])
        df=df[:-14]
        df_list2.append(df)
    elif 'UTLA Code' not in list(df.columns):
        try:
            df= pd.read_excel(daily_vacc[i], sheet_name='Vaccinations by LTLA and Age ', skiprows=11)
            df = df[['UTLA Code', 'UTLA Name', 'LTLA Code4', 'LTLA Name4', 'Total 1st Doses8', 'Total 2nd Doses8', 'Cumulative Total Doses (1st and 2nd doses) to Date8']]
            df = df[3:]
            df['date'] = daily_names[i][38:]
            df['date'] = pd.to_datetime(df['date'])
            df_list2.append(df)
        except KeyError:
            df= pd.read_excel(daily_vacc[i], sheet_name='Vaccinations by LTLA and Age ', skiprows=10)
            df = df[['UTLA Code', 'UTLA Name', 'LTLA Code4', 'LTLA Name4', 'Total 1st Doses8', 'Total 2nd Doses8', 'Cumulative Total Doses (1st and 2nd doses) to Date8']]
            df = df[3:]
            df['date'] = daily_names[i][38:]
            df['date'] = pd.to_datetime(df['date'])
            df_list2.append(df)


#%%
df35=pd.read_excel(daily_vacc[35], sheet_name='Vaccinations by LTLA and Age ', skiprows=12)
df35.head()
df35 = df35[['UTLA Code', 'UTLA Name', 'LTLA Code3', 'LTLA Name3', 'Total 1st Doses7', 'Total 2nd Doses7', 'Cumulative Total Doses (1st and 2nd doses) to Date7']]
df35 = df35[3:]
df35['date'] = daily_names[35][38:]
df35['date'] = pd.to_datetime(df35['date'])
df35=df35[:-14]
df35.tail(20)


#%%
for item in df_list1:
    df_list.append(item)
#%%
for item in df_list2:
    df_list.append(item)
#%%
df_list.append(df14)
#%%
df_list.append(df31)
df_list.append(df35)
#%%
df_list[0].columns
#%%

for df in df_list:
    df.columns = ['UTLA_Code', 'UTLA_Name', 'LTLA_Code', 'LTLA_Name', 'Total_1st_Doses', 'Total_2nd_Doses', 'Cumulative_Total_Doses_to_Date', 'date']
#%% check the dfs that don't have as a last row york:
bad=[]
for i in range(len(df_list)):
    if df_list[i].iloc[-1]['UTLA_Name'] != 'York':
        bad.append(i)
#%%
df_list[bad[0]].tail(20)
#%%
len(bad)
#%% correct the bad dfs:
df_list[bad[0]]=df_list[bad[0]][:-14]
#%%
df_list[bad[1]]=df_list[bad[1]][:-14]
#%%
df_list[bad[2]]=df_list[bad[2]][:-14]
#%%
df_list[bad[3]]=df_list[bad[3]][:-14]
#%%
df_list[bad[4]]=df_list[bad[4]][:-14]
#%%
df_list[bad[5]]=df_list[bad[5]][:-14]
#%%
df_list[bad[6]]=df_list[bad[6]][:-14]
#%%
df_list[bad[7]]=df_list[bad[7]][:-14]
#%%
df_list[bad[8]]=df_list[bad[8]][:-14]
#%%
df_list[bad[9]]=df_list[bad[9]][:-14]
#%%
df_list[bad[10]]=df_list[bad[10]][:-14]
#%%
df_list[bad[11]]=df_list[bad[11]][:-15]
#%% 
#check if it worked:
bad=[]
for i in range(len(df_list)):
    if df_list[i].iloc[-1]['UTLA_Name'] != 'York':
        bad.append(i)
len(bad)
#%% 
#concat
dfs = pd.concat(df_list)
dfs.shape
dfs['date'].value_counts()
#%%
dfs['date'] = pd.to_datetime(dfs['date'])
#%%
dfs = dfs.sort_values(by=['date'],ascending= True)
dfs.head()
#%%
dfs.to_csv('vaccination_data_lad_june_july.csv', index=False)