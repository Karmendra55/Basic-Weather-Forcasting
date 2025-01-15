import requests
from datetime import datetime
from tkinter import *
from tkinter import ttk, messagebox
from Api import API_Retrive

# Function to fetch and process the 5-day forecast
def get_5_day_forecast():
    city = city_entry.get()
    if not city:
        messagebox.showerror("Error", "Please enter a city name!")
        return
    
    # OpenWeatherMap API Key (replace with your own key)
    API_KEY = "your_api_key_here"
    URL = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_Retrive()}&units=metric"

    try:
        response = requests.get(URL)
        response.raise_for_status()
        data = response.json()

        # Process the 5-day forecast
        forecast = {}
        for entry in data['list']:
            date_str = entry['dt_txt'].split(' ')[0]  # Extract the date
            time = entry['dt_txt'].split(' ')[1]  # Extract the time
            temp = entry['main']['temp']

            # Group by date
            if date_str not in forecast:
                forecast[date_str] = {'high': temp, 'low': temp, 'high_time': time, 'low_time': time}
            else:
                # Update high temperature and time
                if temp > forecast[date_str]['high']:
                    forecast[date_str]['high'] = temp
                    forecast[date_str]['high_time'] = time
                
                # Update low temperature and time
                if temp < forecast[date_str]['low']:
                    forecast[date_str]['low'] = temp
                    forecast[date_str]['low_time'] = time

        # Display the forecast
        forecast_text = ""
        for i, (date, values) in enumerate(forecast.items()):
            if i == 5:  # Limit to 5 days
                break
            day_name = datetime.strptime(date, "%Y-%m-%d").strftime("%A")
            high_temp = values['high']
            low_temp = values['low']
            high_time = values['high_time']
            low_time = values['low_time']
            forecast_text += (f"{date} ({day_name})\n"
                              f"High: {high_temp}°C at {high_time}\n"
                              f"Low: {low_temp}°C at {low_time}\n\n")

        forecast_label.config(text=forecast_text)
    
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Failed to fetch data: {e}")
    except KeyError:
        messagebox.showerror("Error", "City not found or API error!")

# Tkinter GUI
root = Tk()
root.title("5-Day Weather Forecast")
root.geometry("400x400")

# City Entry
Label(root, text="Enter City:", font=("Arial", 14)).pack(pady=10)
city_entry = Entry(root, font=("Arial", 14))
city_entry.pack(pady=5)

# Fetch Button
fetch_button = Button(root, text="Get 5-Day Forecast", font=("Arial", 14), command=get_5_day_forecast)
fetch_button.pack(pady=10)

# Forecast Label
forecast_label = Label(root, text="", font=("Arial", 12), justify=RIGHT, anchor="w")
forecast_label.pack(pady=10, fill="both", expand=True)

root.mainloop()