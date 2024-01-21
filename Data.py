import os
import pandas as pd

def GetYear(date): #YYYY-MM-DDTHH:MM:SS
    return date[:4]

def GetMonth(date): #YYYY-MM-DDTHH:MM:SS
    return date[5:7]

def GetDay(date): #YYYY-MM-DDTHH:MM:SS
    return date[8:10]

def GetHour(date): #YYYY-MM-DDTHH:MM:SS
    return date[11:13]



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
    year = []
    month = []
    day = []
    hour = []
    if os.path.exists('HistoricalData.csv'):
        data = pd.read_csv('HistoricalData.csv')
        for i_czas in czas:
            year.append(GetYear(i_czas))
            month.append(GetMonth(i_czas))
            day.append(GetDay(i_czas))
            hour.append(GetHour(i_czas))
        new_data = pd.DataFrame({'year':year,'month':month,'day':day,'hour':hour,
                            'czas':czas,'temperature':temperature,'wilgotnosc':wilgotnosc
                             ,'predkosc_wiatru':predkosc_wiatru,'aqi':aqi,'o3':o3,
                             'so2':so2,'no2':no2,'pm10':pm10,'pm25':pm25,'co':co})
        updated_data = pd.concat([data,new_data], join="inner", ignore_index=True)       
        # for i in range(0, len(czas)):
        #         print(i)
        #         new_row = {'year':GetYear(czas[i]),'month':GetMonth(czas[i]),'day':GetDay(czas[i]),'hour':GetHour(czas[i]),
        #                       'czas':czas[i],'temperature':temperature[i], 
        #                        'wilgotnosc':wilgotnosc[i],'predkosc_wiatru':predkosc_wiatru[i],
        #                        'aqi':aqi[i],'o3':o3[i],'so2':so2[i],'no2':no2[i],'pm10':pm10[i],
        #                        'pm25':pm25[i],'co':co[i]}
        #         print(new_row)
                #data.loc[len(data)]=new_row

                #data.loc[len(data)]=[year[i],month[i],day[i],hour[i],czas[i],temperature[i],wilgotnosc[i],
                #                     predkosc_wiatru[i],aqi[i],o3[i],so2[i],no2[i],pm10[i],pm25[i],co[i]]
                #data.concat([data, pd.DataFrame([new_row])], ignore_index=True)
                # data._append({'year':year[i],'month':month[i],'day':day[i],'hour':hour[i],
                #               'czas':czas[i],'temperature':temperature[i], 
                #                'wilgotnosc':wilgotnosc[i],'predkosc_wiatru':predkosc_wiatru[i],
                #                'aqi':aqi[i],'o3':o3[i],'so2':so2[i],'no2':no2[i],'pm10':pm10[i],
                #                'pm25':pm25[i],'co':co[i]}, ignore_index=True)
        updated_data.sort_values(by=['year','month','day','hour'])
        updated_data.to_csv('HistoricalData.csv')
    else:
        for i_czas in czas:
            year.append(GetYear(i_czas))
            month.append(GetMonth(i_czas))
            day.append(GetDay(i_czas))
            hour.append(GetHour(i_czas))
        data = pd.DataFrame({'year':year,'month':month,'day':day,'hour':hour,
                            'czas':czas,'temperature':temperature,'wilgotnosc':wilgotnosc
                             ,'predkosc_wiatru':predkosc_wiatru,'aqi':aqi,'o3':o3,
                             'so2':so2,'no2':no2,'pm10':pm10,'pm25':pm25,'co':co})
        data.sort_values(by=['year','month','day','hour'])
        data.to_csv('HistoricalData.csv')


def GetDataSplitToday(start_date): #przekazuje dane od start_date do today
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