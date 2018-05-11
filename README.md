# Simple Python script for chase car upload to Habitat

Created by Dave Akerman (dave@sccs.co.uk)

This script uses GPSD to get the current time and position from a GPS device.  Refer to the GPSD documentation on how to install and configure GPSD, and please confirm that it is working and you have a valid position from GPSD before trying this script.


## Hardware ##

The script was tested on a Raspberry Pi with a USB GPS, but should run fine on any computer that has GPSD installed and working.

USB GPS devices are available from ebay, Amazon etc. very cheaply.  Remember that they need to have a good view of the sky in order to work, so you may find it preferable to purchase one that has a long lead so you can place the GPS receiver in the car roof, rather than the ones that have the antenna next to the USB plug.

 
## Installation ##

Refer to the GPSD documentation on how to install and configure GPSD, and please confirm that it is working and you have a valid position from GPSD before trying this script.

Make sure you have Python 3.x installed.


## Usage ##

Run the script with a command like so:

	python3 chase.py MYCAR_chase

Replace "MYCAR" with something meaningful - e.g. your ham radio callsign, name, team name etc. 


## Map ##

If all is well your position will appear on the live map at [https://tracker.habhub.org](https://tracker.habhub.org)


## Notes ##

The script uses threading, for no reason other than that the code was almost entirely a cut and paste job from my LCARS chase car script.  So, it could have been simpler, but it was less work to leave it as it is.
