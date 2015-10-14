# Harpy #

Harpy ( Host Address Resolution Protocol in Python ) is a small program that utilises scapy, tcpdump to perform low level monitoring of the data packets in the Ethernet port while provide a simple web interface using Flask, that allows the user to set alerts for specific devices joining his network.The basic use case of harpy is to 
provide seamless visual allerts.

Scapy needs root priviledges to bind to the socket in raw mode.

### Requirements: ###

* [Flask](http://flask.pocoo.org/), [pypi](https://pypi.python.org/pypi/Flask)
* [Scapy](http://www.secdev.org/projects/scapy/), [Pypi](https://pypi.python.org/pypi/scapy)
* [tcpudmp](http://www.tcpdump.org/)
* Optional requirement for LED notifications in Raspberry pi, the [PiBlinker](https://github.com/minosg/piblinker.gitPiBlinker) library. Adding --recursive in the clone will automatically download it.
* Python 2.7.X
* Linux, Posix System

### Installation: ###
Asuming a working python 2.7.X installation with pip installed.
*2.7.9 includes pip by default*
```
  # Install the dependancies
  sudo pip install -r dependancies.pip  # Linux
  sudo pip install -r dependancies_raspberryPI.pip # Raspberry PI

  # Clone the project
  git clone git@github.com:minosg/harpy.git --recursive
  cd harpy
  # Get ip of system
  hostname -I
  # Run it with elevated priviledges
  sudo python harpy.py
```

Open Browser and navigate to ip http://X.X.X.X:7777 or the port configured in harpy.py entry to see the interface

### Work in progress ###

