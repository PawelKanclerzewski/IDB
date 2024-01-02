import numpy as np
from sklearn.ensemble import IsolationForest

def start(temperature, wilgotnosc, predkosc_wiatru, pm10, pm25, co, o3, so2, no2):
    x1 = detect_anomalies(temperature)
    x2 = detect_anomalies(wilgotnosc)
    x3 = detect_anomalies(predkosc_wiatru)
    x4 = detect_anomalies(pm10)
    x5 = detect_anomalies(pm25)
    x6 = detect_anomalies(co)
    x7 = detect_anomalies(o3)
    x8 = detect_anomalies(so2)
    x9 = detect_anomalies(no2)

    return x1, x2, x3, x4, x5, x6, x6, x7, x8, x9

def detect_anomalies(x):

    # Konwersja danych do numpy array
    data_array = np.array(x).reshape(-1, 1)

    # Inicjalizacja modelu Isolation Forest
    isolation_forest_model = IsolationForest(contamination=0.05)  # contamination to odsetek uznawanych za anomalie

    # Trening modelu na danych
    isolation_forest_model.fit(data_array)

    # Predykcja anomalii (1 - normalne, -1 - anomalie)
    predictions = isolation_forest_model.predict(data_array)

    # Zwróć tablicę z wynikami predykcji (1 - normalne, 0 - anomalie)
    anomaly_results = [1 if prediction == 1 else 0 for prediction in predictions]

    return anomaly_results