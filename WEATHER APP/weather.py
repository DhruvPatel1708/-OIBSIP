import tkinter as tk
from tkinter import messagebox
import requests
from datetime import datetime
from time import strftime

def update_time():
    """Update the time display every second"""
    current_time = strftime('%I:%M:%S %p')  # 12-hour format with AM/PM
    current_date = strftime('%A, %B %d, %Y')  # Full date format
    
    time_label.config(text=f"🕐 {current_time}")
    date_label.config(text=f"📅 {current_date}")
    
    # Update every 1000 milliseconds (1 second)
    root.after(1000, update_time)

def get_weather():
    city = city_entry.get()
    api_key = "0efc3505d8f6399f4f1625487ca71e2b"  # Replace with your API key
    
    if not city:
        messagebox.showwarning("Warning", "Please enter a city name!")
        return
    
    # Show loading
    result_label.config(text="🔄 Loading weather data...")
    
    try:
        # API request
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200:
            # Get weather info
            temp = data['main']['temp']
            feels_like = data['main']['feels_like']
            humidity = data['main']['humidity']
            description = data['weather'][0]['description']
            city_name = data['name']
            country = data['sys']['country']
            wind_speed = data['wind']['speed']
            pressure = data['main']['pressure']
            
            # Get weather emoji
            weather_main = data['weather'][0]['main']
            weather_emojis = {
                'Clear': '☀️',
                'Clouds': '☁️',
                'Rain': '🌧️',
                'Drizzle': '🌦️',
                'Thunderstorm': '⛈️',
                'Snow': '🌨️',
                'Mist': '🌫️',
                'Fog': '🌫️'
            }
            emoji = weather_emojis.get(weather_main, '🌤️')
            
            # Display weather with emoji
            weather_text = f"""
🌍 City: {city_name}, {country}
{emoji} Weather: {description.title()}
🌡️ Temperature: {temp:.1f}°C
🔥 Feels Like: {feels_like:.1f}°C
💧 Humidity: {humidity}%
💨 Wind Speed: {wind_speed} m/s
📊 Pressure: {pressure} hPa
            """
            result_label.config(text=weather_text)
            
        else:
            result_label.config(text="❌ City not found!\nPlease check spelling and try again.")
            
    except requests.exceptions.ConnectionError:
        result_label.config(text="🚫 No internet connection!\nPlease check your connection.")
    except Exception as e:
        result_label.config(text=f"⚠️ Error occurred!\n{str(e)}")

# Create main window
root = tk.Tk()
root.title("🌤️ Weather App with Live Clock")
root.geometry("500x650")
root.config(bg='lightblue')

# Header Frame for Time and Date
header_frame = tk.Frame(root, bg='darkblue', relief='raised', bd=2)
header_frame.pack(fill='x', pady=(0, 10))

# Live Time Display
time_label = tk.Label(header_frame, text="🕐 Loading...", 
                     font=('Arial', 16, 'bold'), 
                     fg='white', bg='darkblue')
time_label.pack(pady=5)

# Live Date Display  
date_label = tk.Label(header_frame, text="📅 Loading...", 
                     font=('Arial', 12), 
                     fg='lightgray', bg='darkblue')
date_label.pack(pady=(0, 10))

# Title
title_label = tk.Label(root, text="🌤️ Weather App", 
                      font=('Arial', 22, 'bold'), 
                      bg='lightblue', fg='darkblue')
title_label.pack(pady=15)

# Input Section
input_frame = tk.Frame(root, bg='lightblue')
input_frame.pack(pady=10)

tk.Label(input_frame, text="🌍 Enter City Name:", 
         font=('Arial', 14, 'bold'), bg='lightblue', fg='darkblue').pack(pady=5)

city_entry = tk.Entry(input_frame, font=('Arial', 16), width=20, 
                     justify='center', relief='flat', bd=5)
city_entry.pack(pady=8)

# Bind Enter key to search
city_entry.bind('<Return>', lambda e: get_weather())

# Search button
search_btn = tk.Button(input_frame, text="🔍 Get Weather", 
                      command=get_weather,
                      font=('Arial', 14, 'bold'), 
                      bg='orange', fg='white',
                      width=15, relief='flat', bd=0,
                      cursor='hand2')
search_btn.pack(pady=10)

# Result display
result_label = tk.Label(root, text="🌟 Welcome to Weather App! 🌟\n\nEnter a city name above and click 'Get Weather'\nto see live weather information!\n\n⏰ Current time is displayed at the top", 
                       font=('Arial', 12), 
                       bg='white', 
                       width=50, height=18,
                       relief='sunken', bd=2,
                       justify='left', fg='darkblue')
result_label.pack(pady=20, padx=20)

# Footer with instructions
footer_label = tk.Label(root, text="💡 Tip: Press Enter after typing city name for quick search!", 
                       font=('Arial', 10, 'italic'), 
                       bg='lightblue', fg='gray')
footer_label.pack(pady=(0, 10))

# Start the time update function
update_time()

# Run the app
root.mainloop()
