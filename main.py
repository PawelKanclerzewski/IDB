import DataAnalyse
import GetWeatherData
import ShowGraph
from Systems import Systems

if __name__ == "__main__":

    czas, temperature, wilgotnosc, predkosc_wiatru, aqi, \
        o3, so2, no2, pm10, pm25, co = GetWeatherData.startReques()

    ShowGraph.startVisualize(czas, temperature, wilgotnosc, predkosc_wiatru, aqi,
                             o3, so2, no2, pm10, pm25, co)

    systems = Systems(temperature[0], wilgotnosc[0], predkosc_wiatru[0], pm10[0], pm25[0],
                                     co[0], o3[0], so2[0], no2[0])

    anomalies = DataAnalyse.start(temperature, wilgotnosc, predkosc_wiatru,
                                             pm10, pm25, co, o3, so2, no2)
