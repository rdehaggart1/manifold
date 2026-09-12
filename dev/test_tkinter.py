import sys
import tkinter
import tkinter.messagebox
from tkintermapview import TkinterMapView

import json
import time
import cairosvg
from PIL import Image, ImageTk
from io import BytesIO
import os

POS_HISTORY_LENGHT = 20

class my_aircraft:
    def __init__(self, callsign, lat, lon, alt, track, category):
        self.callsign = callsign
        self.lat = lat
        self.lon = lon
        self.alt = alt
        self.track = track
        self.category = category
        self.marker = None
        self.position_history = [(None,None) for x in range(POS_HISTORY_LENGHT)]
        self.marker_history = [None for x in range(POS_HISTORY_LENGHT)]

def load_svg(path, size=(60, 60)):
    png = cairosvg.svg2png(
        url=path,
        output_width=size[0],
        output_height=size[1],
    )
    return Image.open(BytesIO(png)).convert("RGBA")

class App(tkinter.Tk):

    APP_NAME = "MANIFOLD"
    ADDRESS = "Low Bradley, England"
    ZOOM = 12
    AIRCRAFT_JSON_FILE = "/run/dump1090-fa/aircraft.json"
    UPDATE_PERIOD_MS = 1000
    

    def __init__(self, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)

        self.title(self.APP_NAME)

        display_width  = self.winfo_screenwidth()               
        display_height = self.winfo_screenheight()               
        self.geometry(f"{display_width}x{display_height}")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        self.grid_rowconfigure(1, weight=1)

        self.map_widget = TkinterMapView()
        self.map_widget.grid(row=1, column=0, columnspan=3, sticky="nsew")

        self.current_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
        self.default_icon = Image.open(os.path.join(self.current_path, "markers/default.png")).resize((60, 60)).rotate(-60)
        self.home_icon = ImageTk.PhotoImage(Image.open(os.path.join(self.current_path, "markers/home.png")).resize((40, 40)))
        self.path_icon = ImageTk.PhotoImage(Image.open(os.path.join(self.current_path, "markers/history.png")).resize((10, 10)))
        self.category_icons = {
            "A0": load_svg(os.path.join(self.current_path, "markers/A0.svg")),
            "A1": load_svg(os.path.join(self.current_path, "markers/A1.svg")),
            "A2": load_svg(os.path.join(self.current_path, "markers/A2.svg")),
            "A3": load_svg(os.path.join(self.current_path, "markers/A3.svg")),
            "A4": load_svg(os.path.join(self.current_path, "markers/A4.svg")),
            "A5": load_svg(os.path.join(self.current_path, "markers/A5.svg")),
            "A6": load_svg(os.path.join(self.current_path, "markers/A6.svg")),
            "A7": load_svg(os.path.join(self.current_path, "markers/A7.svg"))
        }

        self.marker_list_box = tkinter.Listbox(self, height=8)
        self.marker_list_box.grid(row=2, column=0, columnspan=1, sticky="ew", padx=10, pady=10)

        self.set_home_position()

        self.aircraft_dict = {
            "TEST": my_aircraft("TEST", 0, 0, 0, 0, "")
        }

    def read_aircraft_file(self):
        with open(self.AIRCRAFT_JSON_FILE) as file:
            data = json.load(file)

        aircraft_json_data = data["aircraft"]

        for a in aircraft_json_data:
            lat, lon, alt   = self.get_aircraft_position(a)
            callsign        = a.get("flight", "").strip()
            hex_id          = a.get("hex")
            track           = a.get("track")
            category        = a.get("category")

            if callsign not in self.aircraft_dict:
                print(f"New callsign: {callsign}")
                print(f"Found {len(aircraft_json_data)} aircraft")
                print(f"Dict: {len(self.aircraft_dict)}")
                self.aircraft_dict[callsign] = my_aircraft(callsign, lat, lon, alt, track, category)

            # todo: 'update' function to write new values
            if callsign is not None:
                self.aircraft_dict[callsign].lat = lat
                self.aircraft_dict[callsign].lon = lon
                self.aircraft_dict[callsign].category = category
                self.aircraft_dict[callsign].track = track
                self.aircraft_dict[callsign].position_history.insert(0, (lat, lon))
                self.aircraft_dict[callsign].position_history.pop()

    def get_aircraft_position(self, aircraft):
        lat = aircraft.get("lat")
        lon = aircraft.get("lon")
        alt = aircraft.get("alt_baro")

        return lat, lon, alt

    def plot_aircraft_markers(self):
        for aircraft in self.aircraft_dict.values():
            if (aircraft.lat is not None) and (aircraft.lon is not None) and (aircraft.callsign):
                icon = self.default_icon
                if (aircraft.category is not None):
                    label = aircraft.callsign
                    if aircraft.category in self.category_icons:
                        icon = self.category_icons[aircraft.category]
                else:
                    label = aircraft.callsign

                if (aircraft.track is not None):
                    rotated_icon = ImageTk.PhotoImage(icon.rotate(-aircraft.track))
                else:
                    rotated_icon = ImageTk.PhotoImage(self.default_icon)

                if (aircraft.marker is None):
                    aircraft.marker = self.map_widget.set_marker(aircraft.lat, aircraft.lon, icon=rotated_icon)
                else:
                    aircraft.marker.set_position(aircraft.lat, aircraft.lon)

                aircraft.marker.text = label
                aircraft.marker.change_icon(rotated_icon)

                self.plot_position_history(aircraft)

    def plot_position_history(self, aircraft):
        #print(f"{aircraft.callsign}:{aircraft.position_history}")
        for idx, marker in enumerate(aircraft.marker_history):
            if marker is not None:
                aircraft.marker_history[idx].set_position(*aircraft.position_history[idx])
            else:
                if aircraft.position_history[idx] is not (None, None):
                    aircraft.marker_history[idx] = self.map_widget.set_marker(*aircraft.position_history[idx], icon=self.path_icon)
                if (None,None) not in aircraft.position_history:
                    self.map_widget.set_path(aircraft.position_history)
            

    def update_map(self):
        self.read_aircraft_file()
        self.plot_aircraft_markers()
        self.after(self.UPDATE_PERIOD_MS, self.update_map)

    def set_home_position(self):
        self.map_widget.set_address(self.ADDRESS, marker=True, text="", icon=self.home_icon)
        self.map_widget.set_zoom(self.ZOOM)
    
    def on_closing(self, event=0):
        self.destroy()
        exit()

    def start(self):
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.update_map()
    app.start()