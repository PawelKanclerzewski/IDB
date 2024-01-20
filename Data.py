import os
import pandas as pd
import numpy as np
from natsort import index_natsorted
from IPython.display import display

def WriteToCSV(czas, temperature, wilgotnosc, predkosc_wiatru, aqi,
        o3, so2, no2, pm10, pm25, co):
    
    # with open('HistoricalData.csv', 'w') as file:
        
    #     fieldnames = ['czas','temperature','wilgotnosc', 'predkosc_wiatru','aqi',
    #                   'o3','so2','no2','pm10','pm25','co']
    #     writer = csv.DictWriter(file, fieldnames=fieldnames)
        
    #     writer.writeheader()
    #     for i in range(0, len(czas)):
    #         writer.writerow({'czas':czas[i],'temperature':temperature[i], 
    #                          'wilgotnosc':wilgotnosc[i],'predkosc_wiatru':predkosc_wiatru[i],
    #                          'aqi':aqi[i],'o3':o3[i],'so2':so2[i],'no2':no2[i],'pm10':pm10[i],
    #                          'pm25':pm25[i],'co':co[i]})

    if os.path.exists('HistoricalData.csv'):
        data = pd.read_csv('HistoricalData.csv')

        for i in range(0, len(czas)):
                new_row = {'czas':czas[i],'temperature':temperature[i], 
                             'wilgotnosc':wilgotnosc[i],'predkosc_wiatru':predkosc_wiatru[i],
                             'aqi':aqi[i],'o3':o3[i],'so2':so2[i],'no2':no2[i],'pm10':pm10[i],
                             'pm25':pm25[i],'co':co[i]}
                data.loc[len(data)]=new_row
                data.sort_values(by="czas",key=lambda x: np.argsort(index_natsorted(data["czas"])))
                data.to_csv('HistoricalData.csv')
    else:
        data = pd.DataFrame({'czas':czas,'temperature':temperature,'wilgotnosc':wilgotnosc
                             ,'predkosc_wiatru':predkosc_wiatru,'aqi':aqi,'o3':o3,
                             'so2':so2,'no2':no2,'pm10':pm10,'pm25':pm25,'co':co})
        data.sort_values(by="czas",key=lambda x: np.argsort(index_natsorted(data["czas"])))
        data.to_csv('HistoricalData.csv')


def GetDataSplitToday(start_date):
    data = pd.read_csv('HistoricalData.csv')
    return data.get("czas"),data.get("temperature"),data.get("wilgotnosc"),data.get("predkosc_wiatru"),\
        data.get("aqi"),data.get("o3"),data.get("so2"),data.get("no2"),data.get("pm10"),data.get("pm25"),data.get("co")

def GetNewestHistoricalDate():
    data = pd.read_csv('HistoricalData.csv')
    
    Date = data['czas'].iloc[0]
    Date = Date[:10]
    return str(Date)


def GetOldestHistoricalDate():
    data = pd.read_csv('HistoricalData.csv')
    
    Date = data['czas'].iloc[-1]
    Date = Date[:10]

    return str(Date)


def CheckIfNeedsUpdatingFront(endDate): #sprawdza czy należy zaktualizować o nowe daty
    
    newestDate = str(endDate)+"T00:00:00"

    data = pd.read_csv('HistoricalData.csv')
    
    if newestDate not in data['czas'].values:
        return True
    else: 
        return False


def CheckIfNeedsUpdatingTail(startDate): #sprawdza czy należy zaktualizować o nowe daty
    
    oldestDate = str(startDate)+"T01:00:00"

    data = pd.read_csv('HistoricalData.csv')
    if oldestDate not in data['czas'].values:
        return True
    else: 
        return False


def CheckIfFileExists():
    
    
    if os.path.exists('HistoricalData.csv'):
        return True
    else:
        return False