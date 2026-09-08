import tkinter
import tkintermapview
import json
import time
import haversine as hs
from haversine import Unit

aircraft_json_file = "/run/dump1090-fa/aircraft.json"

# todo: easier way to input lat/lon

# Oxford
MY_LAT = 51.741529
MY_LON = -1.220428

# Bradley
MY_LAT = 53.933192
MY_LON = -1.997486
MY_POS = (MY_LAT, MY_LON)

# create the tkinter window and a map widget within it
def create_map():
    # create tkinter window
    root_tk = tkinter.Tk()
    root_tk.title("local_map")

    # for full fullscreen, no toolbar. nice for display
    # root_tk.attributes('-fullscreen',True)

    # scale window to full display
    display_width  = root_tk.winfo_screenwidth()               
    display_height = root_tk.winfo_screenheight()               
    root_tk.geometry("%dx%d" % (display_width, display_height))

    # create map widget
    map_widget = tkintermapview.TkinterMapView(root_tk, width=1000, height=700, corner_radius=0)
    map_widget.pack(fill="both", expand=True)

    # set current position and zoom
    # map_widget.set_position(52.516268, 13.377695, marker=False)  # Berlin, Germany

    # set current position with address
    map_widget.set_address("Low Bradley England", marker=False)

    centre_coords = map_widget.get_position()
    print(f"Centre: {centre_coords}")

    return root_tk, map_widget

def load_nearby_aircraft():
    
    with open(aircraft_json_file) as file:
        data = json.load(file)

    list_of_aircraft = data["aircraft"]

    print(f"{len(list_of_aircraft)} aircraft")

    return list_of_aircraft

def plot_aircraft_markers(list_of_aircraft, map_widget):
    closest_aircraft = ""
    min_distance = 1e6

    for a in list_of_aircraft:
        callsign = a.get("flight", "").strip()
        hex_id = a.get("hex")
        lat = a.get("lat")
        lon = a.get("lon")
        altitude = a.get("alt_baro")

        aircraft_position = (lat, lon)

        if (not callsign) or (not lat) or (not lon):
            print(callsign)
        else:
            marker_3 = map_widget.set_marker(lat, lon, text=callsign)
            distance=hs.haversine(aircraft_position, MY_POS, unit=Unit.KILOMETERS)

            if distance < min_distance:
                min_distance = distance
                closest_aircraft = callsign

            print(
                hex_id,
                callsign,
                lat,
                lon,
                altitude,
                f"{distance:.2f}km"
            )

    print(f"Closest aircraft is {closest_aircraft} at {min_distance:.2f}km")

    print()

if __name__=="__main__":

    root_tk, map_widget = create_map()

    list_of_aircraft = load_nearby_aircraft()

    plot_aircraft_markers(list_of_aircraft, map_widget)

    root_tk.mainloop()
    