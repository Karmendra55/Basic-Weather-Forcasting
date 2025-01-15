from tkinter import *
import tkinter as tk
from geopy.geocoders import Nominatim
from tkinter import ttk, messagebox
from timezonefinder import TimezoneFinder
from datetime import datetime
import requests
import pytz
import Api

root = Tk()
root.title("Weather Forecast")
root.geometry("920x520+300+220")
root.resizable(False, False)

# On Tab Change
def on_tab_change(event):
    for frame in notebook.winfo_children():
        frame.pack_forget()
    notebook.select(notebook.select())

# Function to get Weather Information
def getWeather():
    city = textfield.get()
    if not city:
        messagebox.showerror("Error", "Please enter a city name!")
        return
        
    # Initialize geolocator with a user agent
    geolocator = Nominatim(user_agent="weather_app_karme")
    location = geolocator.geocode(city)
        
    if not location:
        messagebox.showerror("Error", "City not found!")
        return
        
    obj = TimezoneFinder()
    result = obj.timezone_at(lng=location.longitude, lat=location.latitude)
        
    if not result:
        messagebox.showerror("Error", "Timezone not found for the given location!")
        return
        
    # Timezone and local time
    home = pytz.timezone(result)
    local_time = datetime.now(home)
    current_time = local_time.strftime("%I:%M %p")
    clock.config(text=current_time)
    name.config(text="CURRENT WEATHER")
        
    # Weather API call
    api = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={Api.API_Retrive()}"
    response = requests.get(api)
    if response.status_code != 200:
        messagebox.showerror("Error", "Unable to fetch weather data!")
        return
        
    json_data = response.json()
        
    # Parse weather data
    condition = json_data['weather'][0]['main']
    description = json_data['weather'][0]['description']
    temp = int(json_data['main']['temp'] - 273.15)  # Convert Kelvin to Celsius
    pressure = json_data['main']['pressure']
    humidity = json_data['main']['humidity']
    wind = json_data['wind']['speed']
        
    # Update labels
    t.config(text=f"{temp}°C")
    c.config(text=f"{condition} | FEELS LIKE {temp}°C")
    w.config(text=f"{wind} m/s")
    h.config(text=f"{humidity}%")
    d.config(text=description.capitalize())
    p.config(text=f"{pressure} hPa")
    
# Function to Get 5-Days Forecast
def get_5_day_forcast():
    city = textfield2.get()
    if not city:
        messagebox.showerror("Error", "Please enter a Valid City Name!")
        return
    
    geolocator = Nominatim(user_agent="weather_app_karme")
    location = geolocator.geocode(city)
    
    if not location:
        messagebox.showerror("Error", "City Not Found!")
        return
    
    #Api Retrieval
    api = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={Api.API_Retrive()}"
    response = requests.get(api)
    if response.status_code != 200:
        messagebox.showerror("Error", "Unable to fetch weather data!")
        return
    
    json_data = response.json()
    if 'list' not in json_data:
        messagebox.showerror("Error", "Invalid response from weather API!")
        return
    
    forecast_list = json_data['list']
    for i in range(0, 40, 8):  # Iteration to find the 5 days, 8 intervals each
        day_data = forecast_list[i]
        date_text = day_data['dt_txt'].split()[0]
        temp_max = int(day_data['main']['temp_max'] - 273.15)
        temp_min = int(day_data['main']['temp_min'] - 273.15)
        weather = day_data['weather'][0]['description']
        
        #Iteration to Feed the Values
        if i == 0:
            Date1.config(text=date_text)
            Day1_h.config(text=f"{temp_max}°C")
            Day1_l.config(text=f"{temp_min}°C")
            Day1_w.config(text=weather.capitalize())
        elif i == 8:
            Date2.config(text=date_text)
            Day2_h.config(text=f"{temp_max}°C")
            Day2_l.config(text=f"{temp_min}°C")
            Day2_w.config(text=weather.capitalize())
        elif i == 16:
            Date3.config(text=date_text)
            Day3_h.config(text=f"{temp_max}°C")
            Day3_l.config(text=f"{temp_min}°C")
            Day3_w.config(text=weather.capitalize())
        elif i == 24:
            Date4.config(text=date_text)
            Day4_h.config(text=f"{temp_max}°C")
            Day4_l.config(text=f"{temp_min}°C")
            Day4_w.config(text=weather.capitalize())
        elif i == 32:
            Date5.config(text=date_text)
            Day5_h.config(text=f"{temp_max}°C")
            Day5_l.config(text=f"{temp_min}°C")
            Day5_w.config(text=weather.capitalize())

# Notebook
notebook = ttk.Notebook(root)

# Creating Frames for each task
Current_Forcast = ttk.Frame(notebook)
Forcast_5Days = ttk.Frame(notebook)

# Adding Tabs to Notebook
notebook.add(Current_Forcast, text="Current Forcast")
notebook.add(Forcast_5Days, text="5 Day Forcasting")

# Pack Notebook as a Widget
notebook.pack(expand=True, fill="both")

# 1st Tab UI
# Current Forcast Tab (Move all relevant widgets into this frame)
label1a = ttk.Label(Current_Forcast)
label1a.pack(pady=20)

# Search Box
Search_image = PhotoImage(file="icons/search.png")
myimage = Label(Current_Forcast, image=Search_image)
myimage.place(x=20, y=40)

# To Type in the City
textfield = tk.Entry(Current_Forcast, justify='center', width=17, font=("arial", 25, "bold"), bg="#404040", border=0, fg="white")
textfield.place(x=50, y=60)
textfield.focus()

# Searching Icon
Search_icon = PhotoImage(file="icons/search_icon.png")
myimage_icon = Button(Current_Forcast, image=Search_icon, borderwidth=0, cursor="hand2", bg="#404040", command=getWeather)
myimage_icon.place(x=400, y=54)

# Logo
Logo_image = PhotoImage(file="icons/logo.png")
logo = Label(Current_Forcast, image=Logo_image)
logo.place(x=150, y=110)

# Bottom Box
Frame_image = PhotoImage(file="icons/box.png")
Frame_myimage = Label(Current_Forcast, image=Frame_image)
Frame_myimage.pack(padx=5, pady=5, side=BOTTOM)

# Timing
name = Label(Current_Forcast, font=("arial", 15, "bold"))
name.place(x=30, y=110)
clock = Label(Current_Forcast, font=("Helvetica", 20))
clock.place(x=30, y=140)

# Labels for weather data
label1 = Label(Current_Forcast, text="WIND", font=("Helvetica", 15, "bold"), fg="white", bg="#1ab5ef")
label1.place(x=120, y=400)

label2 = Label(Current_Forcast, text="HUMIDITY", font=("Helvetica", 15, "bold"), fg="white", bg="#1ab5ef")
label2.place(x=250, y=400)

label3 = Label(Current_Forcast, text="DESCRIPTION", font=("Helvetica", 15, "bold"), fg="white", bg="#1ab5ef")
label3.place(x=430, y=400)

label4 = Label(Current_Forcast, text="PRESSURE", font=("Helvetica", 15, "bold"), fg="white", bg="#1ab5ef")
label4.place(x=650, y=400)

# Time and Conditions
t = Label(Current_Forcast, font=("arial", 70, "bold"), fg="#ee666d")
t.place(x=400, y=150)
c = Label(Current_Forcast, font=("arial", 15, 'bold'))
c.place(x=400, y=250)

# Placing Values
w = Label(Current_Forcast, text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
w.place(x=120, y=430)

h = Label(Current_Forcast, text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
h.place(x=265, y=430)

d = Label(Current_Forcast, text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
d.place(x=430, y=430)

p = Label(Current_Forcast, text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
p.place(x=650, y=430)


# 2nd Tab UI
# 5-Day Forcasting Tab
label2a = ttk.Label(Forcast_5Days)
label2a.pack(pady=20)

# Search Box
Search_image2 = PhotoImage(file="icons/search.png")
myimage2 = Label(Forcast_5Days, image=Search_image2)
myimage2.place(x=20, y=30)

# To Type in the City
textfield2 = tk.Entry(Forcast_5Days, justify='center', width=17, font=("arial", 25, "bold"), bg="#404040", border=0, fg="white")
textfield2.place(x=50, y=50)
textfield2.focus()

# Searching Icon
Search_icon2 = PhotoImage(file="icons/search_icon.png")
myimage_icon2 = Button(Forcast_5Days, image=Search_icon, borderwidth=0, cursor="hand2", bg="#404040", command=get_5_day_forcast)
myimage_icon2.place(x=400, y=44)

#Box for Dates
Frame_image2 = PhotoImage(file="icons/5 day forcast/Date_Day.png")
Frame_myimage2 = Label(Forcast_5Days, image=Frame_image2)
Frame_myimage2.place(x=20, y=120)


#5-Forcasting Days
Stats1 = Label(Forcast_5Days, text="Labels", font=("Helvetica", 20, "bold"), fg="white", bg="#ffb5ce")
Stats1.place(x=25, y=150)

Day1 = Label(Forcast_5Days, text="Day 1", font=("Helvetica", 15, "bold"), fg="white", bg="#ffb5ce")
Day1.place(x=190, y=135)

Day2 = Label(Forcast_5Days, text="Day 2", font=("Helvetica", 15, "bold"), fg="white", bg="#ffb5ce")
Day2.place(x=334, y=135)

Day3 = Label(Forcast_5Days, text="Day 3", font=("Helvetica", 15, "bold"), fg="white", bg="#ffb5ce")
Day3.place(x=478, y=135)

Day4 = Label(Forcast_5Days, text="Day 4", font=("Helvetica", 15, "bold"), fg="white", bg="#ffb5ce")
Day4.place(x=622, y=135)

Day5 = Label(Forcast_5Days, text="Day 5", font=("Helvetica", 15, "bold"), fg="white", bg="#ffb5ce")
Day5.place(x=766, y=135)

#5-Forcasting Dates
Date1 = Label(Forcast_5Days, text="Date 1", font=("Helvetica", 15, "bold"), fg="white", bg="#ffb5ce")
Date1.place(x=186, y=170)

Date2 = Label(Forcast_5Days, text="Date 2", font=("Helvetica", 15, "bold"), fg="white", bg="#ffb5ce")
Date2.place(x=330, y=170)

Date3 = Label(Forcast_5Days, text="Date 3", font=("Helvetica", 15, "bold"), fg="white", bg="#ffb5ce")
Date3.place(x=474, y=170)

Date4 = Label(Forcast_5Days, text="Date 4", font=("Helvetica", 15, "bold"), fg="white", bg="#ffb5ce")
Date4.place(x=618, y=170)

Date5 = Label(Forcast_5Days, text="Date 5", font=("Helvetica", 15, "bold"), fg="white", bg="#ffb5ce")
Date5.place(x=762, y=170)

# Text Forcasting Data
Day_High = Label(Forcast_5Days, text="High", font=("arial", 20, "bold"), fg="white", bg="#6ac7e2")
Day_High.place(x=12, y= 250)

Day_low = Label(Forcast_5Days, text="Low", font=("arial", 20, "bold"), fg="white", bg="#6ac7e2")
Day_low.place(x=12, y=330)

Day_Weather = Label(Forcast_5Days, text="Weather", font=("arial", 20, "bold"), fg="white", bg="#6ac7e2")
Day_Weather.place(x=5, y=420)

#5-Day Forcasting Data
Day1_h = Label(Forcast_5Days, text="", font=("arial", 20 , "bold"), fg="black")
Day1_l = Label(Forcast_5Days, text="", font=("arial", 20 , "bold"), fg="black")
Day1_w = Label(Forcast_5Days, text="", font=("arial", 16 , "bold"), fg="black")
Day1_h.place(x=195, y=250)
Day1_l.place(x=195, y=330)
Day1_w.place(x=155, y=420)

Day2_h = Label(Forcast_5Days, text="", font=("arial", 20 , "bold"), fg="black")
Day2_l = Label(Forcast_5Days, text="", font=("arial", 20 , "bold"), fg="black")
Day2_w = Label(Forcast_5Days, text="", font=("arial", 16 , "bold"), fg="black")
Day2_h.place(x=339, y=250)
Day2_l.place(x=339, y=330)
Day2_w.place(x=322, y=420)

Day3_h = Label(Forcast_5Days, text="", font=("arial", 20 , "bold"), fg="black")
Day3_l = Label(Forcast_5Days, text="", font=("arial", 20 , "bold"), fg="black")
Day3_w = Label(Forcast_5Days, text="", font=("arial", 16 , "bold"), fg="black")
Day3_h.place(x=483, y=250)
Day3_l.place(x=483, y=330)
Day3_w.place(x=470, y=420)

Day4_h = Label(Forcast_5Days, text="", font=("arial", 20 , "bold"), fg="black")
Day4_l = Label(Forcast_5Days, text="", font=("arial", 20 , "bold"), fg="black")
Day4_w = Label(Forcast_5Days, text="", font=("arial", 16 , "bold"), fg="black")
Day4_h.place(x=627, y=250)
Day4_l.place(x=627, y=330)
Day4_w.place(x=610, y=420)

Day5_h = Label(Forcast_5Days, text="", font=("arial", 20 , "bold"), fg="black")
Day5_l = Label(Forcast_5Days, text="", font=("arial", 20 , "bold"), fg="black")
Day5_w = Label(Forcast_5Days, text="", font=("arial", 16 , "bold"), fg="black")
Day5_h.place(x=781, y=250)
Day5_l.place(x=781, y=330)
Day5_w.place(x=758, y=420)


# Bind the event when switching tabs to the on_tab_change function
notebook.bind("<<NotebookTabChanged>>", on_tab_change)

root.mainloop()
