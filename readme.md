# MANIFOLD 
MANIFOLD (**MA**nifold of **N**earby **I**dentified **F**lying **O**bjects for **L**ocal **D**isplay) is one of my proudest achievements... The acronym, that is. 

MANIFOLD is an open-source project for tracking flights and displaying them locally. Think Flight Radar 24 but on your wall instead of your phone, and without any broader connectivity required. 

# Dependencies and setup
## python (and virtual environment)
### tkinter
```bash
sudo apt-get install python3-tk
```

## dump1090
```bash
sudo bash -c "$(wget -O - https://raw.githubusercontent.com/abcd567a/piaware-ubuntu-debian-amd64/master/install-dump1090-fa.sh)"
```
Then restart your computer

Then verify that it dump1090 is running as a service
```bash
systemctl status dump1090-fa
```

# Hardware
FlightAware Pro Stick Plus - [The Pi Hut](https://thepihut.com/products/flightaware-pro-stick-plus-usb-sdr-ads-b-receiver)

1090MHz ADS-B SMA Antenna - [The Pi Hut](https://thepihut.com/products/3dbi-ads-b-1090mhz-sma-antenna-w-magnetic-base)


# Installation