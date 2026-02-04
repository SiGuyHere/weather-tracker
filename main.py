import tkinter as tk
from tkinter import messagebox
import firebase_admin
from firebase_admin import credentials, firestore
import requests
import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

#firebase setup
cred = credentials.Certificate(r"C:\Users\siigu\OneDrive\Desktop\database project\weather-tracker-36e4f-firebase-adminsdk-fbsvc-99d17bbc4b.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)
db = firestore.client()

#api key
API_KEY = "c16fd325fa7be68835e908f697503fcd"

#all the fun stuff
def fetch_weather(zip_code, country_code="US"):
    #fetch weather data using zip code
    try:
        #get lat and lon from zip code
        geo_url = f"http://api.openweathermap.org/geo/1.0/zip?zip={zip_code},{country_code}&appid={API_KEY}"
        geo_response = requests.get(geo_url)
        geo_data = geo_response.json()

        if geo_data.get("cod") is not None and geo_data["cod"] != 200:
            messagebox.showerror("Error", f"Zip code not found: {zip_code}")
            return None

        lat = geo_data["lat"]
        lon = geo_data["lon"]
        city_name = geo_data["name"]

        #get weather using lat/lon
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        weather_response = requests.get(weather_url)
        weather_data = weather_response.json()

        return {
            "stationCity": city_name,
            "temperature": weather_data["main"]["temp"],
            "humidity": weather_data["main"]["humidity"],
            "windSpeed": weather_data["wind"]["speed"],
            "description": weather_data["weather"][0]["description"],
            "timestamp": firestore.SERVER_TIMESTAMP
        }
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch weather: {e}")
        return None

def add_station():
    station_name = station_entry.get().strip()
    zip_code = zip_entry.get().strip()

    if not station_name or not zip_code:
        messagebox.showwarning("Input Error", "Please enter both station name and ZIP code.")
        return

    # save to Firestore
    db.collection("weatherStations").document(station_name).set({
        "zip": zip_code
    })

    messagebox.showinfo(
        "Station Added",
        f"Station '{station_name}' with ZIP '{zip_code}' added successfully!"
    )

    load_stations_from_db()

def update_weather():
    """Fetch and display weather for selected station"""
    station_name = selected_station.get()
    if station_name == "Select a station":
        messagebox.showwarning("No Station Selected", "Please select a station.")
        return

    zip_code = stations.get(station_name)
    weather = fetch_weather(zip_code)
    if weather:
        #show the current weather
        weather_text = f"Station: {station_name}\nCity: {weather['stationCity']}\n" \
                       f"Temperature: {weather['temperature']}°C\nHumidity: {weather['humidity']}%\n" \
                       f"Wind Speed: {weather['windSpeed']} m/s\nDescription: {weather['description']}"
        weather_label.config(text=weather_text)

        #save to firestone
        timestamp_str = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        doc_ref = db.collection("weatherStations").document(station_name)\
                    .collection("readings").document(timestamp_str)
        doc_ref.set(weather)
        print(f"Weather data saved for {station_name} at {timestamp_str}")


        plot_history(station_name)

def plot_history(station_name):
    """Fetch historical temperature data and plot it"""
    readings_ref = db.collection("weatherStations").document(station_name).collection("readings")
    readings = readings_ref.order_by("timestamp").stream()

    timestamps = []
    temperatures = []

    for doc in readings:
        data = doc.to_dict()
        ts = doc.id
        # converting firestone datestamp to one that you can understand
        try:
            ts_dt = datetime.datetime.strptime(ts, "%Y%m%d%H%M%S")
            timestamps.append(ts_dt)
        except:
            timestamps.append(datetime.datetime.now())
        temperatures.append(data.get("temperature"))

    ax.clear()
    if temperatures:
        ax.plot(timestamps, temperatures, marker='o', linestyle='-', color='blue')
        ax.set_title(f"Temperature History: {station_name}")
        ax.set_xlabel("Time")
        ax.set_ylabel("Temperature (°C)")
        fig.autofmt_xdate()
    else:
        ax.text(0.5, 0.5, "No historical data", horizontalalignment='center', verticalalignment='center')

    fig.tight_layout()

    canvas.draw()

def load_stations_from_db():
    stations.clear()
    station_dropdown['menu'].delete(0, 'end')

    docs = db.collection("weatherStations").stream()
    for doc in docs:
        data = doc.to_dict()
        zip_code = data.get("zip")
        if zip_code:
            stations[doc.id] = zip_code
            station_dropdown['menu'].add_command(
                label=doc.id,
                command=tk._setit(selected_station, doc.id)
            )
#gui setup
root = tk.Tk()
root.title("Weather Dashboard")
root.geometry("600x600")


stations = {}

selected_station = tk.StringVar(root)
selected_station.set("Select a station")

tk.Label(root, text="Select Station:").pack(pady=5)
station_dropdown = tk.OptionMenu(root, selected_station, "Loading...")
station_dropdown.pack(pady=5)

load_stations_from_db()

tk.Button(root, text="Update Weather", command=update_weather).pack(pady=10)


weather_label = tk.Label(root, text="", font=("Helvetica", 12), justify="left")
weather_label.pack(pady=15)


tk.Label(root, text="Add New Station:").pack(pady=5)
tk.Label(root, text="Station Name:").pack()
station_entry = tk.Entry(root)
station_entry.pack(pady=3)

tk.Label(root, text="ZIP Code:").pack()
zip_entry = tk.Entry(root)
zip_entry.pack(pady=3)

tk.Button(root, text="Add Station", command=add_station).pack(pady=10)


fig, ax = plt.subplots(figsize=(5, 3))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(pady=20)

root.mainloop()