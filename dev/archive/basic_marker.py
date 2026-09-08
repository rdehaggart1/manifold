import tkinter
import tkintermapview
import json
import time
import haversine as hs
from haversine import Unit

AIRCRAFT_JSON = "/run/dump1090-fa/aircraft.json"
MY_LAT = 51.741529
MY_LON = -1.220428
MY_POS = (MY_LAT, MY_LON)

# create tkinter window
root_tk = tkinter.Tk()
root_tk.geometry(f"{2000}x{700}")
root_tk.title("basic_marker.py")

# for full fullscreen, no toolbar. nice for display
#root_tk.attributes('-fullscreen',True)

width= root_tk.winfo_screenwidth()               
height= root_tk.winfo_screenheight()               
root_tk.geometry("%dx%d" % (width, height))

# create map widget
map_widget = tkintermapview.TkinterMapView(root_tk, width=1000, height=700, corner_radius=0)
map_widget.pack(fill="both", expand=True)

# set current position and zoom
# map_widget.set_position(52.516268, 13.377695, marker=False)  # Berlin, Germany

# set current position with address
map_widget.set_address("Skipton England", marker=False)

centre_coords = map_widget.get_position()

print(f"Centre: {centre_coords}")

with open(AIRCRAFT_JSON) as file:
    data = json.load(file)

aircraft = data["aircraft"]

print(f"{len(aircraft)} aircraft")

closest_aircraft = ""
min_distance = 1e6

for a in aircraft:
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

root_tk.mainloop()