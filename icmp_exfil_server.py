#!/usr/bin/python
from optparse import OptionParser
import socket
import base64

IPV4_HEAD_SIZE = 20
ICMP_HEAD_SIZE = 8

def dec_base64(dataBlob):
    return base64.b64decode(dataBlob)

def listen():
  s = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_ICMP)
  s.setsockopt(socket.SOL_IP, socket.IP_HDRINCL, 1)

  f = open("test.txt", "a")
  while 1:
    data, addr = s.recvfrom(1508)
    #print "Packet from %r: %r" % (addr,data)

    if(options.encoding.lower() == "base64".lower()):
        data = dec_base64(data)

    print data[IPV4_HEAD_SIZE+ICMP_HEAD_SIZE:]
    # Skip IP and ICMP headers and starting
    # writing data at the ICMP payload field
    f.write(data[IPV4_HEAD_SIZE+ICMP_HEAD_SIZE:])




if __name__ == '__main__':

    # Parse command line options
    parser = OptionParser()
    parser.add_option("-e", "--encoding", type="string", help="Encoding type (e.g. base64)")
    (options, args) = parser.parse_args()
    listen()
