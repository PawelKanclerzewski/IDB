from fastapi import FastAPI
from reactpy import component, html, hooks
from reactpy.backend.fastapi import configure, Options
from fastapi.staticfiles import StaticFiles
from Systems import Systems
import DataAnalyse
import GetWeatherData
from reactpy_apexcharts import ApexChart

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
opt = Options(head=(
        html.title("Intelligent Project"),
        html.link({
            "rel": "icon",
            "href": "/_reactpy/assets/reactpy-logo.ico",
            "type": "image/x-icon",
            }),
        html.link({
            "rel": "stylesheet",
            "href": "static/mystyle.css",
            "type": "text/css",
            }),
        html.link({
            "rel": "stylesheet",
            "href": "static/tw.css",
            "type": "text/css",
        }),
        # html.link({
        #     "href": "https://unpkg.com/tailwindcss@2.2.19/dist/tailwind.min.css",
        #     "rel": "stylesheet",
        #     }),
        html.link({
            "rel": "preconnect",
            "href": "https://fonts.googleapis.com",
            }),
        html.link({
            "rel": "preconnect",
            "href": "https://fonts.gstatic.com",
            "crossorigin": "anonymous"
            }),
        html.link({
            "rel": "stylesheet",
            "href": "https://fonts.googleapis.com/css2?family=Exo+2:ital,wght@0,100..900;1,100..900&display=swap",
        }),
    ))

@component
def JakoscPowietrza(aqi):
    if aqi <= 50:
        return html.div({"class_name": "tileRowValue", "style": {"color": "green"}}, "Dobry")
    elif aqi <= 100:
        return html.div({"class_name": "tileRowValue", "style": {"color": "#FDFF04"}}, "Umiarkowany")
    elif aqi <= 150:
        return html.div({"class_name": "tileRowValue", "style": {"color": "#FF7E00"}}, "Niezdrowy dla grup wrażliwych")
    elif aqi <= 200:
        return html.div({"class_name": "tileRowValue", "style": {"color": "#FF0001"}}, "Niezdrowy")
    elif aqi <= 300:
        return html.div({"class_name": "tileRowValue", "style": {"color": "#99014C"}}, "Bardzo niezdrowy")
    else:
        return html.div({"class_name": "tileRowValue", "style": {"color": "#7E0023"}}, "Toksyczny")

@component
def Aktualne(temperature, wilgotnosc, predkosc_wiatru, aqi, o3, so2, no2, pm10, pm25, co):
    return html.div({"class_name": "tile"},
        html.div({"class_name": "tileTitle"}, "Dane aktualne:"),
        html.div({"class_name": "tileRow"}, "Temperatura:", html.div({"class_name": "tileRowValue"}, str(temperature[0])+"°C")),
        html.div({"class_name": "tileRow"}, "Wilgotność:", html.div({"class_name": "tileRowValue"}, str(wilgotnosc[0])+"%")),
        html.div({"class_name": "tileRow"}, "Prędkośc wiatru:", html.div({"class_name": "tileRowValue"}, str(predkosc_wiatru[0])+" m/s")),
        html.div({"class_name": "tileRow"}, "Indeks jakości powietrza:", JakoscPowietrza(aqi[0])),
        html.div({"class_name": "tileRow"}, "O3:", html.div({"class_name": "tileRowValue"}, str(o3[0])+" µg/m³")),
        html.div({"class_name": "tileRow"}, "SO2:", html.div({"class_name": "tileRowValue"}, str(so2[0])+" µg/m³")),
        html.div({"class_name": "tileRow"}, "NO2:", html.div({"class_name": "tileRowValue"}, str(no2[0])+" µg/m³")),
        html.div({"class_name": "tileRow"}, "PM10:", html.div({"class_name": "tileRowValue"}, str(pm10[0])+" µg/m³")),
        html.div({"class_name": "tileRow"}, "PM25:", html.div({"class_name": "tileRowValue"}, str(pm25[0])+" µg/m³")),
        html.div({"class_name": "tileRow"}, "CO:", html.div({"class_name": "tileRowValue"}, str(co[0])+" µg/m³")),
    )

@component
def Systemy(temperature, wilgotnosc, predkosc_wiatru, o3, so2, no2, pm10, pm25, co):
    systems = Systems(temperature[0], wilgotnosc[0], predkosc_wiatru[0], pm10[0], pm25[0], co[0], o3[0], so2[0], no2[0])
    return html.div({"class_name": "tile"},
        html.div({"class_name": "tileTitle"}, "Dane budynku:"),
        html.div({"class_name": "tileRow"}, "Okna:", html.div({"class_name": "tileRowValue"}, "Otwarte" if systems[0] else "Zamknięte")),
        html.div({"class_name": "tileRow"}, "Oczyszczacze powietrza:", html.div({"class_name": "tileRowValue"}, "Włączone" if systems[1] else "Wyłączone")),
        html.div({"class_name": "tileRow"}, "Nawilżacze:", html.div({"class_name": "tileRowValue"}, "Włączone" if systems[2] else "Wyłączone")),
        html.div({"class_name": "tileRow"}, "Filtry gazowe:", html.div({"class_name": "tileRowValue"}, "Włączone" if systems[3] else "Wyłączone")),
    )

@component
def Anomalia(value: bool):
    if value:
        return html.div({"class_name": "tileRowValue greenColor"}, "Brak")
    else:
        return html.div({"class_name": "tileRowValue redColor"}, "Anomalia")

@component
def Anomalie(temperature, wilgotnosc, predkosc_wiatru, o3, so2, no2, pm10, pm25, co):
    anomalie = DataAnalyse.start(temperature, wilgotnosc, predkosc_wiatru, pm10, pm25, co, o3, so2, no2)
    return html.div({"class_name": "tile"},
        html.div({"class_name": "tileTitle"}, "Anomalie:"),
        html.div({"class_name": "tileRow"}, "Temperatura:", Anomalia(anomalie[0])),
        html.div({"class_name": "tileRow"}, "Wilgotność:", Anomalia(anomalie[1])),
        html.div({"class_name": "tileRow"}, "Prędkośc wiatru:", Anomalia(anomalie[2])),
        html.div({"class_name": "tileRow"}, "O3:", Anomalia(anomalie[3])),
        html.div({"class_name": "tileRow"}, "SO2:", Anomalia(anomalie[4])),
        html.div({"class_name": "tileRow"}, "NO2:", Anomalia(anomalie[5])),
        html.div({"class_name": "tileRow"}, "PM10:", Anomalia(anomalie[6])),
        html.div({"class_name": "tileRow"}, "PM25:", Anomalia(anomalie[7])),
        html.div({"class_name": "tileRow"}, "CO:", Anomalia(anomalie[8])),
    )

@component
def Wykres(czas, value, name, color):
    return html.div({"class_name": ""},
        ApexChart(options={
            "series": [{"name": name, "data": value}],
            "chart": {"type": "line", "height": 600, "width": 900, "fontFamily": "Exo 2, sans-serif"},
            "xaxis": {
                "type": "datetime",
                "categories": czas,
                "title": {
                    "text": "Czas",
                    "style": {
                        "fontSize": "1.2rem"
                    },
                    "offsetY": 10,
                }
            },
            "colors": [color],
            "stroke": {
                "curve": "smooth",
                "colors": [color],
            },
            "yaxis": {
                "title": {
                    "text": name,
                    "style": {
                        "fontSize": "1.2rem"
                    },
                    "offsetX": 10,
                },
            },
            "grid": {
                "borderColor": "#90A4AE",
            },
            "tooltip": {
                "x": {
                    "format": "H d-MM-yyyy"
                }
            }
        })
    )

@component
def Button(text, func, active):
    def handle_click(event):
        func()

    return html.button({
            "class_name": f'{"buttonActive" if active else "button"}',
            "on_click": handle_click,
        }, text)

@component
def Wykresy(czas, temperature, wilgotnosc, predkosc_wiatru, aqi, o3, so2, no2, pm10, pm25, co):
    current, setCurrent = hooks.use_state(0)
    return html.div({"class_name": "graphs"},
        html.div({"class_name": "buttonsContainer"},
            Button("Temperatura", lambda: setCurrent(0), current == 0),
            Button("Wilgotność", lambda: setCurrent(1), current == 1),
            Button("Prędkość wiatru", lambda: setCurrent(2), current == 2),
            Button("Jakość powietrza", lambda: setCurrent(3), current == 3),
            Button("O3", lambda: setCurrent(4), current == 4),
            Button("SO2", lambda: setCurrent(5), current == 5),
            Button("NO2", lambda: setCurrent(6), current == 6),
            Button("PM10", lambda: setCurrent(7), current == 7),
            Button("PM25", lambda: setCurrent(8), current == 8),
            Button("CO", lambda: setCurrent(9), current == 9),
        ),
        Wykres(czas, temperature, "Temperatura", "#008FFB") if current == 0 else "",
        Wykres(czas, wilgotnosc, "Wilgotność", "#008FFB") if current == 1 else "",
        Wykres(czas, predkosc_wiatru, "Prędkość wiatru", "#008FFB") if current == 2 else "",
        Wykres(czas, aqi, "Jakość powietrza", "#008FFB") if current == 3 else "",
        Wykres(czas, o3, "O3", "#008FFB") if current == 4 else "",
        Wykres(czas, so2, "SO2", "#008FFB") if current == 5 else "",
        Wykres(czas, no2, "NO2", "#008FFB") if current == 6 else "",
        Wykres(czas, pm10, "PM10", "#008FFB") if current == 7 else "",
        Wykres(czas, pm25, "PM25", "#008FFB") if current == 8 else "",
        Wykres(czas, co, "CO", "#008FFB") if current == 9 else "",
    )

@component
def App():
    global czas, temperature, wilgotnosc, predkosc_wiatru, aqi, o3, so2, no2, pm10, pm25, co

    def fetch():
        global czas, temperature, wilgotnosc, predkosc_wiatru, aqi, o3, so2, no2, pm10, pm25, co
        czas, temperature, wilgotnosc, predkosc_wiatru, aqi, \
            o3, so2, no2, pm10, pm25, co = GetWeatherData.startReques()

    fetch()

    return html.div({"class_name": "mainContainer"},
        html.div({"class_name": "topHeader"}, "Suprime IntelliHouse"),
        html.div({"class_name": "contentContainer"},
            Button("Odśwież", fetch, False),
            html.div({"class_name": "topContainer"},
                Aktualne(temperature, wilgotnosc, predkosc_wiatru, aqi, o3, so2, no2, pm10, pm25, co),
                Systemy(temperature, wilgotnosc, predkosc_wiatru, o3, so2, no2, pm10, pm25, co),
                Anomalie(temperature, wilgotnosc, predkosc_wiatru, o3, so2, no2, pm10, pm25, co),
            ),
            html.div({"class_name": "bottomContainer"},
                Wykresy(czas, temperature, wilgotnosc, predkosc_wiatru, aqi, o3, so2, no2, pm10, pm25, co)
            ),
        )
    )


configure(app, App, opt)

