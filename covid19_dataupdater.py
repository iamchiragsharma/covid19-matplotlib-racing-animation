import pandas as pd
import requests
import json

covid19_data = json.loads(requests.get("https://api.rootnet.in/covid19-in/stats/history").text)
dates = [d['day'] for d in covid19_data['data']]
national_data = [d['summary'] for d in covid19_data['data']]
regional_data= [d['regional'] for d in covid19_data['data']]

dataframe_cols = ['Date','State','ConfirmedCasesIndian','ConfirmedCasesForeign','Discharged','Deaths','TotalConfirmed']
dataframe_data = []
for element,date in zip(regional_data,dates):
    jk_ladakh_per_day = [date,'JK and Ladakh',0, 0, 0, 0, 0]
    for entry in element:
        if entry['loc'] not in ['Jammu and Kashmir', 'Ladakh']:
            dataframe_data.append([date,entry['loc'],entry['confirmedCasesIndian'],entry['confirmedCasesForeign'],entry['discharged'],entry['deaths'],entry['totalConfirmed']])
        else:
            jk_ladakh_per_day[2] += entry['confirmedCasesIndian']
            jk_ladakh_per_day[3] += entry['confirmedCasesForeign']
            jk_ladakh_per_day[4] += entry['discharged']
            jk_ladakh_per_day[5] += entry['deaths']
            jk_ladakh_per_day[6] += entry['totalConfirmed']
    dataframe_data.append(jk_ladakh_per_day)
            
df_regional = pd.DataFrame(dataframe_data,columns=dataframe_cols)
df_regional['Date'] = pd.to_datetime(df_regional['Date'])
df_regional.replace("Nagaland#",'Nagaland',inplace=True)
df_regional.replace("Jharkhand#",'Jharkhand',inplace=True)
df_regional.replace("Madhya Pradesh#",'Madhya Pradesh',inplace=True)
df_regional.replace("Dadar Nagar Haveli",'D&N Haveli and Daman&Diu',inplace=True)
df_regional.replace("Dadra and Nagar Haveli and Daman and Diu",'D&N Haveli and Daman&Diu',inplace=True)

df_national = pd.DataFrame(national_data)
df_national.columns=[x+"_National" for x in dataframe_cols if x != 'Date']
df_national.insert(0,'Date',dates)
df_national['Date'] = pd.to_datetime(df_national['Date'])

df_regional.to_csv("covid_data/covid19_statewise.csv", index=False)
df_national.to_csv("covid_data/covid19_india.csv",index=False)
