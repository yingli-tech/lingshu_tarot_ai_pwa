import requests

# my API key and city name
api_key = "f67c76f07b43540e4f20e1baf724f9f9"
city = "Evanston"
url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

response = requests.get(url)
data = response.json()

# 提取并打印天气信息
print("城市:", data["name"])
print("天气:", data["weather"][0]["description"])
print("温度:", data["main"]["temp"], "°C")
print("湿度:", data["main"]["humidity"], "%")

-----the latter one has been executed.

import requests

# my API key and city name
api_key = "71b057bf071849f3aa2bf54881079b15"
city = "Evanston"
url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

response = requests.get(url)
print("请求的URL:", url)
print("\n")
print("响应状态码:", response.status_code)
print("\n")

if response.status_code == 200:
    data = response.json()

# 提取并打印天气信息
    print("城市:", data["name"])
    print("天气:", data["weather"][0]["description"])
    print("温度:", data["main"]["temp"], "°C")
    print("湿度:", data["main"]["humidity"], "%")
    print("\n")
    print("所有:",response.json())

else:
    print("请求失败^_^:", response.json().get("message", "未知错误"))