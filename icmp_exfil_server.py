#!/usr/bin/python
from optparse import OptionParser
import socket


def listen():
  s = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_ICMP)
  s.setsockopt(socket.SOL_IP, socket.IP_HDRINCL, 1)

  f = open("test.txt", "a")
  while 1:
    data, addr = s.recvfrom(1508)
    #print "Packet from %r: %r" % (addr,data)

    print data[28:]
    f.write(data[28:])




if __name__ == '__main__':

    # Parse command line options


    listen()
