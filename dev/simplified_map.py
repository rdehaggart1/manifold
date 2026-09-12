import tkinter
import tkintermapview
import json
import time
import haversine as hs
from haversine import Unit
from PIL import Image, ImageTk
import os

AIRCRAFT_JSON_FILE = "/run/dump1090-fa/aircraft.json"

# todo: easier way to input lat/lon

# Oxford
MY_LAT = 51.741529
MY_LON = -1.220428

# Bradley
MY_LAT = 53.933192
MY_LON = -1.997486
MY_POS = (MY_LAT, MY_LON)

class my_aircraft:
    callsign = "0"
    hex_id   = 0
    location = (0, 0)
    altitude = 0
    marker   = 0

def create_map():
    """Creates a tkinter window and a map widget within it

        Returns
        ------
        root_tk
            The tkinter window handle
        map_widget
            The tkintermapview widget handle
    """

    # create tkinter window
    root_tk = tkinter.Tk()
    root_tk.title("local_map")

    # for full fullscreen, no toolbar. nice for display
    # root_tk.attributes('-fullscreen',True)

    display_width  = root_tk.winfo_screenwidth()               
    display_height = root_tk.winfo_screenheight()               
    root_tk.geometry("%dx%d" % (display_width, display_height))

    map_widget = tkintermapview.TkinterMapView(root_tk, width=1000, height=700, corner_radius=0)
    map_widget.pack(fill="both", expand=True)

    map_widget.set_address("Low Bradley England", marker=False)

    centre_coords = map_widget.get_position()
    # print(f"Centre: {centre_coords}")

    return root_tk, map_widget

def load_nearby_aircraft(aircraft_json_file):
    """Reads the aircraft from the json file

            Parameters
            ------
            aircraft_json_file
                The full path to the dump1090 .json file for detected aircraft
    
            Returns
            ------
            list_of_aircraft
                A list of the detected aircraft and their associated properties
        """
    
    with open(aircraft_json_file) as file:
        data = json.load(file)

    list_of_aircraft = data["aircraft"]

    print(f"{len(list_of_aircraft)} aircraft")

    return list_of_aircraft

def get_aircraft_position(aircraft):
    lat = aircraft.get("lat")
    lon = aircraft.get("lon")
    alt = aircraft.get("alt_baro")

    return lat, lon, alt

def plot_aircraft_markers(list_of_aircraft, map_widget, marker_icon):

    for a in list_of_aircraft:
        aircraft          = my_aircraft()
        lat, lon, alt     = get_aircraft_position(a)
        aircraft.callsign = a.get("flight", "").strip()
        aircraft.hex_id   = a.get("hex")
        aircraft.position = (lat, lon)

        print(aircraft.callsign)

        if (not aircraft.callsign) or (not lat) or (not lon):
            # print(callsign)
            break
        else:
            # * operator unpacks the position tuple into separate coords
            aircraft.marker = map_widget.set_marker(*aircraft.position, text=aircraft.callsign, icon=marker_icon)

            #print(
            #    hex_id,
            #    callsign,
            #    lat,
            #    lon,
            #    alt,
            #    f"{distance:.2f}km"
            #)

def update_markers(root_tk, map_widget, plane_icon):
    list_of_aircraft = load_nearby_aircraft(AIRCRAFT_JSON_FILE)
    plot_aircraft_markers(list_of_aircraft, map_widget, plane_icon)
    root_tk.after(1000, update_markers, root_tk, map_widget, plane_icon) 

if __name__=="__main__":

    root_tk, map_widget = create_map()

    current_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    plane_icon = ImageTk.PhotoImage(Image.open(os.path.join(current_path, "plane_icon.png")).resize((40, 40)))

    list_of_aircraft = load_nearby_aircraft(AIRCRAFT_JSON_FILE)
    plot_aircraft_markers(list_of_aircraft, map_widget, plane_icon)

    update_markers(root_tk, map_widget, plane_icon)

    root_tk.mainloop()