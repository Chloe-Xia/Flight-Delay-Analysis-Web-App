import json
import pandas as pd
import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse
from collections import defaultdict
import datetime
# 其他视图函数

def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        username = request.POST.get("name")
        password = request.POST.get("pwd")
        if username == 'root' and password == "123":
            return render(request, 'index.html')
        else:
            return render(request, 'login.html', {"error_msg": "Name or password is wrong"})

def index(request):
    return render(request, 'index.html')

def register(request):
    return HttpResponse("register page")

def search(request):
    return render(request, 'search.html')


def comment(request):
    return render(request, 'comment.html')

def favorite_d(request):
    return render(request, 'favorite.html')

import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse

def search_flight(request):
    context = {}
    if request.method == "POST":
        starting_point = request.POST.get('starting-point')
        destination = request.POST.get('destination')
        date = request.POST.get('date')
        airplane_type = request.POST.get('airplane-type')

        print("Received form data - Starting Point:", starting_point)
        print("Received form data - Destination:", destination)
        print("Received form data - Date:", date)
        print("Received form data - Airplane Type:", airplane_type)

        file_path = 'translated_flights_schedule.xlsx'
        df = pd.read_excel(file_path)

        print("DataFrame head:")
        print(df.head())

        df['日期'] = pd.to_datetime(df['日期']).dt.strftime('%Y-%m-%d')
        print("Converted dataframe dates:", df['日期'].unique())

        filtered_df = df[(df['出发机场'] == starting_point) &
                         (df['到达机场'] == destination) &
                         (df['日期'] == date)]

        if airplane_type:
            filtered_df = filtered_df[filtered_df['航空公司'] == airplane_type]
        any=df['航空公司']
        print("Filtered DataFrame:")
        print(filtered_df)

        # 获取天气数据
        api_key = "7fe4a8b124d41b9b5c76f6335b115c04"
        weather_starting_point = get_five_day_forecast(api_key, starting_point.split(' ')[0])
        weather_destination = get_five_day_forecast(api_key, destination.split(' ')[0])

        # 找到所选日期的天气数据
        start_weather = next((w for w in weather_starting_point if w['date'] == date), None)
        dest_weather = next((w for w in weather_destination if w['date'] == date), None)

        # 添加天气数据到DataFrame中
        filtered_df['天气_出发'] = start_weather['description'] if start_weather else None
        filtered_df['最低气温_出发'] = start_weather['min_temp'] if start_weather else None
        filtered_df['最高气温_出发'] = start_weather['max_temp'] if start_weather else None
        filtered_df['天气_到达'] = dest_weather['description'] if dest_weather else None
        filtered_df['最低气温_到达'] = dest_weather['min_temp'] if dest_weather else None
        filtered_df['最高气温_到达'] = dest_weather['max_temp'] if dest_weather else None

        # 替换天气描述为数值
        departure_replace_dict = {
            '中雨': 0.51, '中雨转大雨': 0.54, '中雨转小雨': 0.38, '中雨转阴': 0.55, '中雨转阵雨': 0.49,
            '多云': 0.24, '多云转中雨': 0.15, '多云转大雨': 0.86, '多云转小雨': 0.16, '多云转阴': 0.27,
            '多云转阵雨': 0.5, '多雨转雷阵雨': 0.29, '大雨': 0.54, '大雨转中雨': 0.6, '大雨转小雨': 0.67,
            '大雨转暴雨': 0.44, '大雨转阴': 0.38, '大雨转阵雨': 0.65, '大雨转雷阵雨': 0.50, '小雨': 0.25,
            '小雨转中雨': 0.46, '小雨转多云': 0.34, '小雨转阴': 0.29, '小雨转阵雨': 0.26, '晴': 0.29,
            '晴转多云': 0.24, '晴转阴': 1.00, '晴转雷阵雨': 0.30, '暴雨': 0.89, '暴雨转大雨': 0.32,
            '暴雨转阵雨': 0.78, '阴': 0.20, '阴转多云': 0.30, '阴转小雨': 0.21, '阴转晴': 0.18,
            '阴转阵雨': 0.60, '阴转雷阵雨': 0.88, '阴转雾': 0.14, '阵雨': 0.34, '阵雨转中雨': 0.30,
            '阵雨转多云': 0.39, '阵雨转大雨': 0.39, '阵雨转小雨': 0.46, '阵雨转阴': 0.19, '阵雨转雷阵雨': 0.61,
            '雷阵雨': 0.53, '雷阵雨转中雨': 0.48, '雷阵雨转多云': 0.57, '雷阵雨转大雨': 0.54, '雷阵雨转晴': 0.58,
            '雷阵雨转阴': 0.50, '雷阵雨转阵雨': 0.48, '雾': 0.12, '雾转晴': 0.26, '多云转大雨': 0.04, '多云转雷阵雨': 0.30, '多云转晴': 0.27, '多云转小雨': 0.16, '中雨转雷阵雨': 0.53
        }

        arrival_replace_dict = {
            '中雨': 0.32, '中雨转大雨': 0.62, '中雨转小雨': 0.44, '中雨转阴': 0.60, '中雨转阵雨': 0.67,
            '多云': 0.37, '多云转中雨': 0.52, '多云转小雨': 0.31, '多云转晴': 0.36, '多云转阴': 0.28,
            '多云转阵雨': 0.64, '多雨转雷阵雨': 0.47, '大雨转中雨': 0.19, '小雨': 0.3, '小雨转中雨': 0.27,
            '小雨转多云': 0.26, '小雨转大雨': 0.13, '小雨转晴': 0.22, '小雨转暴雨': 0.33, '小雨转阴': 0.34,
            '小雨转阵雨': 0.39, '小雨转雨夹雪': 0.80, '晴': 0.37, '晴转多云': 0.29, '晴转大雨': 0.50,
            '晴转小雨': 0.41, '晴转阴': 0.36, '阴': 0.28, '阴转中雨': 0.25, '阴转多云': 0.27,
            '阴转大雨': 0.48, '阴转小雨': 0.24, '阴转晴': 0.31, '阴转阵雨': 0.66, '阴转雷阵雨': 0.61,
            '阵雨': 0.46, '阵雨转中雨': 0.50, '阵雨转多云': 0.64, '阵雨转小雨': 0.30, '阵雨转阴': 0.42,
            '阵雨转雷阵雨': 0.10, '雷阵雨转中雨': 0.74, '多云转雷阵雨': 0.48,
        }

        airline_dict = {
            '上海航空': 0.48, '东方航空': 0.37, '中国国航': 0.40, '中国联合航空': 1.00, '南方航空': 0.42, '厦门航空': 0.62,
            '吉祥航空': 0.36, '四川航空': 0.35, '山东航空': 1.00, '成都航空': 0.39, '昆明航空': 0.40, '春秋航空': 0.42,
            '河北航空': 0.33, '海南航空': 0.43, '深圳航空': 0.43, '瑞丽航空': 0.29, '祥鹏航空': 0.39, '荷兰航空': 0.33,
            '西藏航空': 0.40, '重庆航空': 1.00, '长龙航空': 0.42, '首都航空': 0.40,
        }

        # 确保所有温度数据都是数值类型
        filtered_df['最低气温_出发'] = pd.to_numeric(filtered_df['最低气温_出发'], errors='coerce')
        filtered_df['最高气温_出发'] = pd.to_numeric(filtered_df['最高气温_出发'], errors='coerce')
        filtered_df['最低气温_到达'] = pd.to_numeric(filtered_df['最低气温_到达'], errors='coerce')
        filtered_df['最高气温_到达'] = pd.to_numeric(filtered_df['最高气温_到达'], errors='coerce')

        filtered_df['天气_出发'] = filtered_df['天气_出发'].replace(departure_replace_dict).astype(float)
        filtered_df['天气_到达'] = filtered_df['天气_到达'].replace(arrival_replace_dict).astype(float)
        filtered_df['航空公司'] = filtered_df['航空公司'].replace(airline_dict).astype(float)

        # 转换温度数据为延误率权重
        mask1 = (filtered_df['最低气温_出发'] >= 0) & (filtered_df['最低气温_出发'] <= 10)
        mask2 = (filtered_df['最低气温_出发'] >= 11) & (filtered_df['最低气温_出发'] <= 19)
        mask3 = (filtered_df['最低气温_出发'] >= 20) & (filtered_df['最低气温_出发'] <= 28)

        filtered_df.loc[mask1, '最低气温_出发'] = 0.30
        filtered_df.loc[mask2, '最低气温_出发'] = 0.26
        filtered_df.loc[mask3, '最低气温_出发'] = 0.38

        mask4 = (filtered_df['最高气温_出发'] >= 6) & (filtered_df['最高气温_出发'] <= 17)
        mask5 = (filtered_df['最高气温_出发'] >= 18) & (filtered_df['最高气温_出发'] <= 27)
        mask6 = (filtered_df['最高气温_出发'] >= 28) & (filtered_df['最高气温_出发'] <= 37)

        filtered_df.loc[mask4, '最高气温_出发'] = 0.29
        filtered_df.loc[mask5, '最高气温_出发'] = 0.28
        filtered_df.loc[mask6, '最高气温_出发'] = 0.38

        mask7 = (filtered_df['最低气温_到达'] >= -3) & (filtered_df['最低气温_到达'] <= 6)
        mask8 = (filtered_df['最低气温_到达'] >= 7) & (filtered_df['最低气温_到达'] <= 16)
        mask9 = (filtered_df['最低气温_到达'] >= 17) & (filtered_df['最低气温_到达'] <= 26)

        filtered_df.loc[mask7, '最低气温_到达'] = 0.27
        filtered_df.loc[mask8, '最低气温_到达'] = 0.28
        filtered_df.loc[mask9, '最低气温_到达'] = 0.42

        mask10 = (filtered_df['最高气温_到达'] >= 3) & (filtered_df['最高气温_到达'] <= 13)
        mask11 = (filtered_df['最高气温_到达'] >= 14) & (filtered_df['最高气温_到达'] <= 24)
        mask12 = (filtered_df['最高气温_到达'] >= 25) & (filtered_df['最高气温_到达'] <= 36)

        filtered_df.loc[mask10, '最高气温_到达'] = 0.26
        filtered_df.loc[mask11, '最高气温_到达'] = 0.27
        filtered_df.loc[mask12, '最高气温_到达'] = 0.43

        filtered_df['延误率'] = 0.42 * filtered_df['天气_出发'] + 0.37 * filtered_df['天气_到达'] + 0.04 * filtered_df[
            '最低气温_出发'] + 0.03 * filtered_df['最低气温_到达'] + 0.06 * filtered_df['最高气温_到达'] + 0.04 * filtered_df[
            '最高气温_出发'] + 0.05 * filtered_df['航空公司']-1

        filtered_df['日期'] = pd.to_datetime(filtered_df['日期'])
        filtered_df['日期'] = pd.to_datetime(filtered_df['日期'])

        dates = filtered_df['日期'].dt.strftime('%Y-%m-%d').tolist()
        delay_rates = filtered_df['延误率'].tolist()

        flight_numbers = filtered_df['航班号'].tolist()
        delay_rates_by_flight = filtered_df['延误率'].tolist()
        print(delay_rates)
        print(flight_numbers)
        weather_data = {
            "starting_point": weather_starting_point,
            "destination": weather_destination
        }
        filtered_df['航空公司']=any
        context = {
            'starting_point': starting_point,
            'destination': destination,
            'date': date,
            'airplane_type': airplane_type,
            'flights': filtered_df.to_dict(orient='records'),
            'weather_data': weather_data,
            'debug': {
                'submitted_date': date,
                'dataframe_dates': df['日期'].tolist(),
                'filtered_count': len(filtered_df)
            },
            'flight_numbers': json.dumps(flight_numbers),
            'delay_rates_by_flight': json.dumps(delay_rates_by_flight)
        }

    return render(request, 'search.html', context)




def add_to_favorite(request):
    if request.method == "POST":
        flight_data = request.POST.get('flight_data')

        # 调试输出接收到的 JSON 数据
        print("Received flight_data:", flight_data)

        if flight_data:
            try:
                flight_data = json.loads(flight_data)
                print("Decoded flight_data:", flight_data)
            except json.JSONDecodeError as e:
                print("JSON decode error:", e)
                return HttpResponse("Invalid JSON data", status=400)

            # 获取现有的收藏列表
            favorite_flights = request.session.get('favorite_flights', [])

            # 添加新收藏的航班信息
            favorite_flights.append(flight_data)

            # 将更新后的收藏列表保存到会话中
            request.session['favorite_flights'] = favorite_flights

    return redirect('favorite')


def remove_from_favorite(request):
    if request.method == "POST":
        flight_id = int(request.POST.get('flight_id'))

        # 获取现有的收藏列表
        favorite_flights = request.session.get('favorite_flights', [])

        # 删除指定的航班信息
        if 0 <= flight_id < len(favorite_flights):
            del favorite_flights[flight_id]

        # 将更新后的收藏列表保存到会话中
        request.session['favorite_flights'] = favorite_flights

    return redirect('favorite')
def favorite(request):
    # 获取收藏的航班信息
    favorite_flights = request.session.get('favorite_flights', [])

    # 计算各个航空公司的占比
    airline_counts = {}
    for flight in favorite_flights:
        airline = flight['航空公司']
        if airline in airline_counts:
            airline_counts[airline] += 1
        else:
            airline_counts[airline] = 1

    airline_labels = list(airline_counts.keys())
    airline_sizes = list(airline_counts.values())

    # 计算各个到达机场的占比
    airport_counts = {}
    for flight in favorite_flights:
        airport = flight['到达机场']
        if airport in airport_counts:
            airport_counts[airport] += 1
        else:
            airport_counts[airport] = 1

    airport_labels = list(airport_counts.keys())
    airport_sizes = list(airport_counts.values())

    return render(request, 'favorite.html', {
        'favorite_flights': favorite_flights,
        'airline_labels': airline_labels,
        'airline_sizes': airline_sizes,
        'airport_labels': airport_labels,
        'airport_sizes': airport_sizes
    })

import json
import requests
from collections import defaultdict
import datetime
from django.http import JsonResponse
from django.shortcuts import render


def get_five_day_forecast(api_key, city_name):
    base_url = "http://api.openweathermap.org/data/2.5/forecast?"
    complete_url = f"{base_url}q={city_name}&appid={api_key}&units=metric"

    response = requests.get(complete_url)
    data = response.json()

    weather_description_mapping = {
        "clear sky": "晴",
        "few clouds": "少云",
        "scattered clouds": "多云转阴",
        "broken clouds": "晴转多云",
        "shower rain": "阴",
        "rain": "阵雨",
        "thunderstorm": "雷暴",
        "snow": "雪",
        "mist": "雾",
        "overcast clouds": "多云",
        "moderate rain" : "中雨",
        "light rain":"小雨",
    }

    if data.get("cod") == "200":
        forecasts = data["list"]
        daily_data = defaultdict(lambda: {"min_temp": float("inf"), "max_temp": float("-inf"), "descriptions": []})

        for forecast in forecasts:
            date = datetime.datetime.fromtimestamp(forecast["dt"]).date()
            temp = forecast["main"]["temp"]
            description = forecast["weather"][0]["description"]

            if temp < daily_data[date]["min_temp"]:
                daily_data[date]["min_temp"] = temp
            if temp > daily_data[date]["max_temp"]:
                daily_data[date]["max_temp"] = temp
            daily_data[date]["descriptions"].append(description)

        city_weather_data = []
        for date in sorted(daily_data.keys())[:5]:
            day_data = daily_data[date]
            most_common_description = max(set(day_data["descriptions"]), key=day_data["descriptions"].count)
            chinese_description = weather_description_mapping.get(most_common_description, most_common_description)
            city_weather_data.append({
                "date": str(date),
                "min_temp": day_data['min_temp'],
                "max_temp": day_data['max_temp'],
                "description": chinese_description
            })

        return city_weather_data
    else:
        return []

def get_city_weather(request, city_name):
    api_key = "7fe4a8b124d41b9b5c76f6335b115c04"
    weather_data = get_five_day_forecast(api_key, city_name)
    return render(request, 'weather.html', {'city_name': city_name, 'weather_data': weather_data})

def analysis(request):
    if request.method == "GET":
        return render(request, 'analysis.html')
    else:
        airplanetype = request.POST.get("airplane-type")
        route = request.POST.get("airline")
        new_list = route.split("-")
        starting = new_list[0]
        destination = new_list[1]

        file_path = '广州-成都.xlsx'
        df = pd.read_excel(file_path, engine='openpyxl')

        filtered_df = df[(df['出发机场'].replace('CAN', "Guangzhou").replace('CTU', "Chengdu") == starting) &
                         (df['到达机场'].replace('CAN', "Guangzhou").replace('CTU', "Chengdu") == destination) &
                         (df['飞机机型'] == airplanetype)]

        departure_replace_dict = {
            '中雨': 0.51, '中雨转大雨': 0.54, '中雨转小雨': 0.38, '中雨转阴': 0.55, '中雨转阵雨': 0.49,
            '多云': 0.24, '多云转中雨': 0.15, '多雨转大雨': 0.86, '多雨转小雨': 0.16, '多云转阴': 0.27,
            '多云转阵雨': 0.5, '多雨转雷阵雨': 0.29, '大雨': 0.54, '大雨转中雨': 0.6, '大雨转小雨': 0.67,
            '大雨转暴雨': 0.44, '大雨转阴': 0.38, '大雨转阵雨': 0.65, '大雨转雷阵雨': 0.50, '小雨': 0.25,
            '小雨转中雨': 0.46, '小雨转多云': 0.34, '小雨转阴': 0.29, '小雨转阵雨': 0.26, '晴': 0.29,
            '晴转多云': 0.24, '晴转阴': 1.00, '晴转雷阵雨': 0.30, '暴雨': 0.89, '暴雨转大雨': 0.32,
            '暴雨转阵雨': 0.78, '阴': 0.20, '阴转多云': 0.30, '阴转小雨': 0.21, '阴转晴': 0.18,
            '阴转阵雨': 0.60, '阴转雷阵雨': 0.88, '阴转雾': 0.14, '阵雨': 0.34, '阵雨转中雨': 0.30,
            '阵雨转多云': 0.39, '阵雨转大雨': 0.39, '阵雨转小雨': 0.46, '阵雨转阴': 0.19, '阵雨转雷阵雨': 0.61,
            '雷阵雨': 0.53, '雷阵雨转中雨': 0.48, '雷阵雨转多云': 0.57, '雷阵雨转大雨': 0.54, '雷阵雨转晴': 0.58,
            '雷阵雨转阴': 0.50, '雷阵雨转阵雨': 0.48, '雾': 0.12, '雾转晴': 0.26,'多云转大雨':0.04,'多云转雷阵雨':0.30,'多云转晴':0.27,'多云转小雨':0.16,'中雨转雷阵雨':0.53
        }

        arrival_replace_dict = {
            '中雨': 0.32, '中雨转大雨': 0.62, '中雨转小雨': 0.44, '中雨转阴': 0.60, '中雨转阵雨': 0.67,
            '多云': 0.37, '多云转中雨': 0.52, '多云转小雨': 0.31, '多云转晴': 0.36, '多云转阴': 0.28,
            '多云转阵雨': 0.64, '多雨转雷阵雨': 0.47, '大雨转中雨': 0.19, '小雨': 0.3, '小雨转中雨': 0.27,
            '小雨转多云': 0.26, '小雨转大雨': 0.13, '小雨转晴': 0.22, '小雨转暴雨': 0.33, '小雨转阴': 0.34,
            '小雨转阵雨': 0.39, '小雨转雨夹雪': 0.80, '晴': 0.37, '晴转多云': 0.29, '晴转大雨': 0.50,
            '晴转小雨': 0.41, '晴转阴': 0.36, '阴': 0.28, '阴转中雨': 0.25, '阴转多云': 0.27,
            '阴转大雨': 0.48, '阴转小雨': 0.24, '阴转晴': 0.31, '阴转阵雨': 0.66, '阴转雷阵雨': 0.61,
            '阵雨': 0.46, '阵雨转中雨': 0.50, '阵雨转多云': 0.64, '阵雨转小雨': 0.30, '阵雨转阴': 0.42,
            '阵雨转雷阵雨': 0.10, '雷阵雨转中雨': 0.74 , '多云转雷阵雨': 0.48,
        }

        filtered_df.loc[:, '天气_出发'] = filtered_df['天气_出发'].replace(departure_replace_dict)
        filtered_df.loc[:, '天气_到达'] = filtered_df['天气_到达'].replace(arrival_replace_dict)

        mask1 = (filtered_df['最低气温_出发'] >= 0) & (filtered_df['最低气温_出发'] <= 10)
        mask2 = (filtered_df['最低气温_出发'] >= 11) & (filtered_df['最低气温_出发'] <= 19)
        mask3 = (filtered_df['最低气温_出发'] >= 20) & (filtered_df['最低气温_出发'] <= 28)

        filtered_df.loc[mask1, '最低气温_出发'] = 0.30
        filtered_df.loc[mask2, '最低气温_出发'] = 0.26
        filtered_df.loc[mask3, '最低气温_出发'] = 0.38

        mask4 = (filtered_df['最高气温_出发'] >= 6) & (filtered_df['最高气温_出发'] <= 17)
        mask5 = (filtered_df['最高气温_出发'] >= 18) & (filtered_df['最高气温_出发'] <= 27)
        mask6 = (filtered_df['最高气温_出发'] >= 28) & (filtered_df['最高气温_出发'] <= 37)

        filtered_df.loc[mask4, '最高气温_出发'] = 0.29
        filtered_df.loc[mask5, '最高气温_出发'] = 0.28
        filtered_df.loc[mask6, '最高气温_出发'] = 0.38

        mask7 = (filtered_df['最低气温_到达'] >= -3) & (filtered_df['最低气温_到达'] <= 6)
        mask8 = (filtered_df['最低气温_到达'] >= 7) & (filtered_df['最低气温_到达'] <= 16)
        mask9 = (filtered_df['最低气温_到达'] >= 17) & (filtered_df['最低气温_到达'] <= 26)

        filtered_df.loc[mask7, '最低气温_到达'] = 0.27
        filtered_df.loc[mask8, '最低气温_到达'] = 0.28
        filtered_df.loc[mask9, '最低气温_到达'] = 0.42

        mask10 = (filtered_df['最高气温_到达'] >= 3) & (filtered_df['最高气温_到达'] <= 13)
        mask11 = (filtered_df['最高气温_到达'] >= 14) & (filtered_df['最高气温_到达'] <= 24)
        mask12 = (filtered_df['最高气温_到达'] >= 25) & (filtered_df['最高气温_到达'] <= 36)

        filtered_df.loc[mask10, '最高气温_到达'] = 0.26
        filtered_df.loc[mask11, '最高气温_到达'] = 0.27
        filtered_df.loc[mask12, '最高气温_到达'] = 0.43

        filtered_df['延误率'] = 0.45 * filtered_df['天气_出发'] + 0.32 * filtered_df['天气_到达'] + 0.06 * filtered_df[
            '最低气温_出发'] + 0.04 * filtered_df['最低气温_到达'] + 0.05 * filtered_df['最高气温_到达'] + 0.08 * filtered_df['最高气温_出发']

        filtered_df['计划起飞时间'] = pd.to_datetime(filtered_df['计划起飞时间'], unit='s')
        filtered_df['计划到达时间'] = pd.to_datetime(filtered_df['计划到达时间'], unit='s')

        print(filtered_df)
        output_file_path = '最终合并的飞机和天气信息.xlsx'
        filtered_df.to_excel(output_file_path, index=False)

        dates = filtered_df['计划起飞时间'].dt.strftime('%Y-%m-%d %H:%M:%S').tolist()
        delay_rates = filtered_df['延误率'].tolist()

        return render(request, 'analysis.html', {
            "airtype_info": airplanetype,
            "start": starting,
            "end": destination,
            "dates": json.dumps(dates),
            "delay_rates": json.dumps(delay_rates)
        })

def ranking(request):
    # Load the Excel file
    file_path = '飞机延误.xlsx'
    df = pd.read_excel(file_path)

    # Filter the necessary columns and sort by delay rate
    df = df[['航空公司', '航空公司延误率']]
    df = df.dropna(subset=['航空公司延误率'])  # Ensure no NaN values in delay rate
    df = df.drop_duplicates(subset=['航空公司'])  # Ensure unique airline entries
    df = df.sort_values(by='航空公司延误率', ascending=False).reset_index(drop=True)

    # Get the top_n parameter from the GET request, default to 10 if not provided
    if request.method == 'POST':
        top_n = int(request.POST.get('top_n', 10))
    else:
        top_n = 10  # 默认显示前10名

    # Select top N
    top_n_df = df.head(top_n)

    # Add ranking column
    top_n_df['排名'] = top_n_df.index + 1

    # Convert the DataFrame to a list of dictionaries
    flights = top_n_df.to_dict(orient='records')

    # Pass the data to the template
    context = {
        'flights': flights,
        'top_n': top_n
    }
    return render(request, 'ranking.html', context)



