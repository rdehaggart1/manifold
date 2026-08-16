import json
import time
import haversine as hs
from haversine import Unit

AIRCRAFT_JSON = "/run/dump1090-fa/aircraft.json"
MY_LAT = 51.741529
MY_LON = -1.220428
MY_POS = (MY_LAT, MY_LON)

while True:
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

        a_pos = (lat, lon)

        if (not callsign) or (not lat) or (not lon):
            print("None")
        else:

            distance=hs.haversine(a_pos, MY_POS, unit=Unit.KILOMETERS)

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
    time.sleep(1)