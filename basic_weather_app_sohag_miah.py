from tkinter import *
from tkinter import ttk
import requests

city_coords = {
    "Dhaka": (23.8103, 90.4125),
    "Chittagong": (22.3569, 91.7832),
    "Rajshahi": (24.3745, 88.6042),
    "Khulna": (22.8456, 89.5403),
    "Barisal": (22.7010, 90.3535),
    "Sylhet": (24.8949, 91.8687),
    "Rangpur": (25.7439, 89.2752),
    "Mymensingh": (24.7471, 90.4203),
    "Cumilla": (23.4682, 91.1788),
    "Narayanganj": (23.6238, 90.5000),
    "Gazipur": (23.9999, 90.4203),
    "Tongi": (23.8930, 90.4021),
    "Bogra": (24.8465, 89.3777),
    "Kushtia": (23.9013, 89.1204),
    "Jessore": (23.1667, 89.2167),
    "Cox's Bazar": (21.4272, 92.0058),
    "Dinajpur": (25.6279, 88.6332),
    "Habiganj": (24.3749, 91.4155),
    "Noakhali": (22.8696, 91.0994),
    "Pabna": (24.0108, 89.2347),
    "Faridpur": (23.6071, 89.8406),
    "Tangail": (24.2513, 89.9167),
    "Jamalpur": (24.9375, 89.9375),
    "Patuakhali": (22.3596, 90.3299),
    "Bhola": (22.6859, 90.6481)
}

cities = list(city_coords.keys())

def get_weather():
    city = com.get().strip()
    if city not in city_coords:
        result_label.config(text="Error: Please select a valid city from the list.")
        return

    lat, lon = city_coords[city]
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=relative_humidity_2m,surface_pressure"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        current = data['current_weather']
        temp_c = current['temperature']
        temp_f = (temp_c * 9/5) + 32
        wind_speed = current['windspeed']
        humidity = data['hourly']['relative_humidity_2m'][0]
        pressure = data['hourly']['surface_pressure'][0]
        
        result_label.config(
            text=f"City: {city}, BD\n"
                 f"Temperature: {temp_c:.2f} °C / {temp_f:.2f} °F\n"
                 f"Humidity: {humidity}%\n"
                 f"Wind Speed: {wind_speed} km/h\n"
                 f"Pressure: {pressure:.1f} hPa"
        )
    except requests.exceptions.ConnectionError:
        result_label.config(text="Network Error: Please check your internet connection.")
    except Exception as e:
        result_label.config(text=f"Error: {e}")

def on_key_release(event):
    value = event.widget.get()
    if value:
        matches = [city for city in cities if value.lower() in city.lower()]
        listbox_update(matches)
    else:
        listbox_update([])

def listbox_update(matches):
    listbox.delete(0, END)
    for match in matches:
        listbox.insert(END, match)

def on_select(event):
    if listbox.curselection():
        selected_city = listbox.get(listbox.curselection())
        com.set(selected_city)
        listbox_update([])

win = Tk()
win.title("Bangladesh Weather App")
win.config(bg="#f5f5f5")
win.geometry("600x420")
win.resizable(False, False)

name_label = Label(win, text="Weather App", font=("Helvetica", 28, "bold"), fg="#333", bg="#f5f5f5")
name_label.place(x=180, y=15)

com = ttk.Combobox(win, values=cities, font=("Helvetica", 12))
com.place(x=200, y=75, width=200)
com.bind('<KeyRelease>', on_key_release)

listbox = Listbox(win, font=("Helvetica", 11), bd=1, relief="solid")
listbox.place(x=200, y=102, width=200, height=90)
listbox.bind('<<ListboxSelect>>', on_select)

done_button = Button(win, text="Get Weather", font=("Helvetica", 11, "bold"), bg="#4CAF50", fg="white", cursor="hand2", command=get_weather)
done_button.place(x=245, y=202, width=110, height=35)

result_label = Label(win, text="", font=("Helvetica", 12), wraplength=500, justify="left", bg="#f5f5f5", fg="#222")
result_label.place(x=60, y=255)

win.mainloop()