def Systems(temperature, wilgotnosc, predkosc_wiatru, pm10, pm25,
            co, o3, so2, no2):

    return window(temperature, predkosc_wiatru), airPurifier(pm10, pm25, co), \
        humidifier(wilgotnosc), airSifter(o3, so2, no2)


def window(temp, windSpeed):
    return temp >= 15 and windSpeed < 5


def airPurifier(pm10, pm25, co):
    return pm10 > 50 or pm25 > 25 or co > 26


def humidifier(wilgotnosc):
    return wilgotnosc > 80


def airSifter(o3, so2, no2):
    return o3 > 100 or so2 > 20 or no2 > 40
