Harpy
=====

Harpy ( Host Address Resolution Protocol in Python ) is a small program that utilises scapy, tcpdump to perform low level monitoring of the data packets in the Ethernet port while provide a simple web interface using Flask, that allows the user to set alerts for specific devices joining his network.

Harpy requires scapy and tcpdump, which can be installed in Ubuntu and Debian using:
sudo apt-get install scapy tcpdump

Scapy needs root priviledges to bind to the socket in raw mode.
