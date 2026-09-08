# https://github.com/TomSchimprintansky/TkinterMapView/blob/main/examples/map_view_simple_example.py

import tkinter
import tkintermapview

# create tkinter window
root_tk = tkinter.Tk()
root_tk.geometry(f"{1000}x{700}")
root_tk.title("map_view_simple_example.py")

# create map widget
map_widget = tkintermapview.TkinterMapView(root_tk, width=1000, height=700, corner_radius=0)
map_widget.pack(fill="both", expand=True)

# set current position and zoom
# map_widget.set_position(52.516268, 13.377695, marker=False)  # Berlin, Germany
# 

# set current position with address
map_widget.set_address("Oxford England", marker=False)

def marker_click(marker):
    print(f"marker clicked - text: {marker.text}  position: {marker.position}")

root_tk.mainloop()