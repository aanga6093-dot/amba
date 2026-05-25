import requests

API_KEY = "MASUKKAN_API_KEY"
city = "Bandung"

url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

data = requests.get(url)
if data.status_code == 200:
   info = data.json()
   print(info)
else:
   print("eror bang status code:",data.status_code)

