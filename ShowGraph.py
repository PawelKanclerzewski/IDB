import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import calendar


def plot_subplots(ax, czas, data, labels, colors):
    czas = [datetime.strptime(c, "%Y-%m-%dT%H:%M:%S") for c in czas]

    for d, label, color in zip(data, labels, colors):
        ax.plot(czas, d, linestyle='-', color=color, label=label, marker='None')  # Ustawienie marker='None'

    ax.set_xlabel('Czas')
    ax.xaxis.set_major_locator(mdates.WeekdayLocator())  # Zmiana na WeekdayLocator
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%B'))  # Zmiana na '%B' dla pełnych nazw miesięcy

    ax.legend(loc='upper left')


def show_plot():
    plt.title('Wykresy')
    plt.tight_layout()
    plt.show()


def startVisualize(czas, temperature, wilgotnosc, predkosc_wiatru, aqi,
        o3, so2, no2, pm10, pm25, co):
    print("Długość czas:", len(czas))
    fig, axs = plt.subplots(4, 3, figsize=(15, 10))  # 4 wiersze, 3 kolumny

    labels = ['Temperatura', 'Wilgotność', 'Predkosc Wiatru', 'TS', 'AQI', 'O3', 'SO2', 'NO2', 'PM10', 'PM2.5', 'CO']
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'purple', 'brown', 'orange', 'pink']

    data_list = [temperature, wilgotnosc, predkosc_wiatru, aqi, o3, so2, no2, pm10, pm25, co]

    for i, ax in enumerate(axs.flatten()):
        if i < len(data_list):
            plot_subplots(ax, czas, [data_list[i]], [labels[i]], [colors[i]])
        else:
            ax.axis('off')

    show_plot()