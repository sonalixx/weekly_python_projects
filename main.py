import tkinter as tk
from tkinter import messagebox
import requests
import matplotlib.pyplot as plt
import csv
from datetime import datetime, timedelta

# OpenWeather API Key (Replace with your own API key)
API_KEY = "YOUR_API_KEY"
CURRENT_WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather():
    city = city_entry.get()
    if not city:
        messagebox.showerror("Error", "Please enter a city name")
        return
    
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    response = requests.get(CURRENT_WEATHER_URL, params=params)
    data = response.json()
    
    if response.status_code == 200:
        weather = data["weather"][0]["description"].capitalize()
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        weather_info = f"Weather: {weather}\nTemperature: {temp}°C\nHumidity: {humidity}%\nWind Speed: {wind_speed} m/s"
        weather_label.config(text=weather_info)
        
        store_data(city, temp, timestamp)
    else:
        messagebox.showerror("Error", "City not found")

def store_data(city, temp, timestamp):
    with open("weather_data.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([city, temp, timestamp])

def plot_graph():
    city = city_entry.get()
    if not city:
        messagebox.showerror("Error", "Please enter a city name")
        return
    
    timestamps, temperatures = [], []
    try:
        with open("weather_data.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == city:
                    timestamps.append(datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S"))
                    temperatures.append(float(row[1]))
    except FileNotFoundError:
        messagebox.showinfo("Info", "No data available")
        return
    
    if not timestamps:
        messagebox.showinfo("Info", "No data available for this city")
        return
    
    plt.figure(figsize=(8, 5))
    plt.plot(timestamps, temperatures, marker='o', linestyle='-', color='blue')
    plt.xlabel("Date & Time")
    plt.ylabel("Temperature (°C)")
    plt.title(f"Temperature Trend for {city}")
    plt.xticks(rotation=45)
    plt.grid()
    plt.show()

# GUI Setup
root = tk.Tk()
root.title("Weather App")
root.geometry("400x400")

city_label = tk.Label(root, text="Enter City:")
city_label.pack()

city_entry = tk.Entry(root)
city_entry.pack()

get_weather_button = tk.Button(root, text="Get Weather", command=get_weather)
get_weather_button.pack()

plot_graph_button = tk.Button(root, text="Plot Temperature", command=plot_graph)
plot_graph_button.pack()

weather_label = tk.Label(root, text="", justify="left")
weather_label.pack()

root.mainloop()
