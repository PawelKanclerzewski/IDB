import requests
import Data
from geopy.geocoders import Nominatim
from datetime import date

# DANE
start_date = "2024-01-24"  # DATA ROZPOCZECIA
end_date = "2024-01-25"  # DATA ZAKONCZENIA
first_api_key = "9b7bb06e07fa4b659f52a6556d1a0fc4"  # KLUCZ API
second_api_key = "9b7bb06e07fa4b659f52a6556d1a0fc4"  # ZASTEPCZY KLUCZ API


def SetStartDate():
    global start_date
    print("Podaj rok rozpoczecia: ")
    year = input()
    print("Podaj miesiac rozpoczecia: ")
    month = input()
    print("Podaj dzien rozpoczecia: ")
    day = input()

    start_date = setDate(year, month, day)


def SetEndDate():
    global end_date
    end_date = date.today()
    #end_date = "2023-06-30"

def setDate(year, month, day):
    # Poprawki: sprawdzenie długości miesiąca i dnia, ustawienie wartości domyślnych
    monthString = month.zfill(2)
    dayString = day.zfill(2)

    return f'{year}-{monthString}-{dayString}'


def get_location():
    global lat, long
    loc = Nominatim(user_agent="GetLoc")
    getLoc = loc.geocode('Bydgoszcz')
    print("Latitude = ", getLoc.latitude)
    print("Longitude = ", getLoc.longitude)
    lat = round(getLoc.latitude, 3)
    long = round(getLoc.longitude, 3)


def getHistoricalWeather(api_key):
    global first_api_key, second_api_key
    global lat, long, start_date, end_date
    print(start_date, end_date)
    print(lat, long)
    url = f'https://api.weatherbit.io/v2.0/history/hourly?lat={lat}&lon={long}&start_date={start_date}&end_date={end_date}&tz=local&key={api_key}'
    print('Sending weatherAPI request...')
    response = requests.get(url)

    if response.status_code == 200:
        dane = response.json()
        return dane
    else:
            print(f'Błąd przy pobieraniu danych. Kod odpowiedzi: {response.status_code}')
            return


def SetHistoricalWeatherData(dane):
    if dane is not None and "data" in dane:
        tablica_danych = dane["data"]

        # Przykład przypisania do kilku tablic
        temperature = [rekord["temp"] for rekord in tablica_danych]
        wilgotnosc = [rekord["rh"] for rekord in tablica_danych]
        predkosc_wiatru = [rekord["wind_spd"] for rekord in tablica_danych]
        return temperature, wilgotnosc, predkosc_wiatru
    else:
        print('Brak danych do przypisania do tablic.')
        return None


def getHistoricalAirQuality(api_key):
    global first_api_key, second_api_key
    #print(first_api_key, second_api_key)
    global lat, long, start_date, end_date
    url = f'https://api.weatherbit.io/v2.0/history/airquality?lat={lat}&lon={long}&start_date={start_date}&end_date={end_date}&tz=local&key={first_api_key}'
    print('Sending airqualityAPI request...')
    response = requests.get(url)

    if response.status_code == 200:
        dane = response.json()
        return dane
    else:
        url = f'https://api.weatherbit.io/v2.0/history/airquality?lat={lat}&lon={long}&start_date={start_date}&end_date={end_date}&tz=local&key={second_api_key}'
        
        response = requests.get(url)

        if response.status_code == 200:
            dane = response.json()
            return dane
        else:
            return None


def SetHistoricalAirQualityData(dane):
    if dane is not None and "data" in dane:
        tablica_danych = dane["data"]
        # Przykład przypisania do kilku tablic
        czas = [rekord["timestamp_local"] for rekord in tablica_danych]
        aqi = [rekord["aqi"] for rekord in tablica_danych]
        o3 = [rekord["o3"] for rekord in tablica_danych]
        so2 = [rekord["so2"] for rekord in tablica_danych]
        no2 = [rekord["no2"] for rekord in tablica_danych]
        pm10 = [rekord["pm10"] for rekord in tablica_danych]
        pm25 = [rekord["pm25"] for rekord in tablica_danych]
        co = [rekord["co"] for rekord in tablica_danych]
        return czas, aqi, o3, so2, no2, pm10, pm25, co
    else:
        print('Brak danych do przypisania do tablic.')
        return None


def trim_arrays(czas, temperature, wilgotnosc, predkosc_wiatru, aqi,
                o3, so2, no2, pm10, pm25, co):
    min_length = min(len(czas), len(temperature), len(wilgotnosc), len(predkosc_wiatru),
                     len(aqi), len(o3), len(so2), len(no2), len(pm25), len(co))

    data_list = [czas, temperature, wilgotnosc, predkosc_wiatru, aqi, o3, so2, no2, pm10, pm25, co]

    for i in range(len(data_list)):
        while len(data_list[i]) > min_length:
            data_list[i].pop()

    return data_list


def startReques():
    get_location()
    

    weather_data = getHistoricalWeather(second_api_key)

    if weather_data:
        temperature, wilgotnosc, predkosc_wiatru = SetHistoricalWeatherData(weather_data)

        air_quality_data = getHistoricalAirQuality(second_api_key)
        if air_quality_data:
            czas, aqi, o3, so2, no2, pm10, pm25, co = SetHistoricalAirQualityData(air_quality_data)

            data = trim_arrays(czas, temperature, wilgotnosc, predkosc_wiatru, aqi,
                               o3, so2, no2, pm10, pm25, co)

            Data.WriteToCSV(data[0], data[1], data[2], data[3], data[4], data[5], \
                data[6], data[7], data[8], data[9], data[10],)
            return data[0], data[1], data[2], data[3], data[4], data[5], \
                data[6], data[7], data[8], data[9], data[10],
        else:
            print("BŁĄD: Brak danych dotyczących jakości powietrza.")
            return None
    else:
        print("BŁĄD: Brak danych dotyczących pogody.")
        return None
    
def startGetData():
    global start_date
    global end_date
    get_location()
    SetStartDate()
    SetEndDate()
    
    if Data.CheckIfFileExists():
        if Data.CheckIfNeedsUpdatingTail(start_date):
            end_date = Data.GetOldestHistoricalDate()
            data = startReques()

        SetEndDate()
        if Data.CheckIfNeedsUpdatingFront(end_date):
            start_date = Data.GetNewestHistoricalDate()
            return startReques()
        
        return Data.GetDataSplitToday(start_date)
    else:
        return startReques()

