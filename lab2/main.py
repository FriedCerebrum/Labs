import requests

n=0
city = "Moscow,RU" #Укажите нужный вам город
appid = "e8b01f246d7310eef2991b67c7b2eb39"
res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                   params={'q': city, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
data = res.json()
print("Погода на настоящий момент: ")
print("Город:", city)
print("Погодные условия:", data['weather'][0]['description'])
print("Температура:", data['main']['temp'])
print("Минимальная температура:", data['main']['temp_min'])
print("Максимальная температура:", data['main']['temp_max'])
print("Видимость: ", data['visibility'])
print("Скорость ветра: ", data['wind']['speed'])
res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                   params={'q': city, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
data = res.json()
print("Недельный прогноз погоды")
for i in data['list']:
    print("Дата<<<", i['dt_txt'])