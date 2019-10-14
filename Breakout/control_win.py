# !/usr/bin/env python

'''
https://stackoverflow.com/questions/4688855/whats-the-difference-between-streams-and-datagrams-in-network-programming

QUOTE:
A long time ago I read a great analogy for explaining the difference between the two.
I don't remember where I read it so unfortunately I can't credit the author for the idea,
but I've also added a lot of my own knowledge to the core analogy anyway. So here goes:

A stream socket is like a phone call -- one side places the call, the other answers,
you say hello to each other (SYN/ACK in TCP), and then you exchange information.
Once you are done, you say goodbye (FIN/ACK in TCP). If one side doesn't hear a goodbye,
they will usually call the other back since this is an unexpected event;
usually the client will reconnect to the server.
There is a guarantee that data will not arrive in a different order than you sent it,
and there is a reasonable guarantee that data will not be damaged.

A datagram socket is like passing a note in class.
Consider the case where you are not directly next to the person you are passing the note to;
the note will travel from person to person. It may not reach its destination,
and it may be modified by the time it gets there. If you pass two notes to the same person,
they may arrive in an order you didn't intend, since the route the notes take through the classroom may not be the same,
one person might not pass a note as fast as another, etc.

So you use a stream socket when having information in order and intact is important.
File transfer protocols are a good example here. You don't want to download some file with its contents randomly
shuffled around and damaged!

You'd use a datagram socket when order is less important than timely delivery (think VoIP or game protocols),
when you don't want the higher overhead of a stream (this is why DNS is primarily a datagram protocol,
so that servers can respond to many, many requests at once very quickly), or when you don't care too much
if the data ever reaches its destination.

To expand on the VoIP/game case, such protocols include their own data-ordering mechanism.
But if one packet is damaged or lost, you don't want to wait on the stream protocol (usually TCP)
to issue a re-send request -- you need to recover quickly. TCP can take up to some number of minutes to recover,
and for realtime protocols like gaming or VoIP even three seconds may be unacceptable!
Using a datagram protocol like UDP allows the software to recover from such an event extremely quickly,
by simply ignoring the lost data or re-requesting it sooner than TCP would.

VoIP is a good candidate for simply ignoring the lost data -- one party would just hear a short gap,
similar to what happens when talking to someone on a cell phone when they have poor reception.
Gaming protocols are often a little more complex, but the actions taken will usually be to either ignore
the missing data (if subsequently-received data supercedes the data that was lost), re-request the missing data,
or request a complete state update to ensure that the client's state is in sync with the server's.
'''

import socket
import socketserver
from PIL import Image, ImageDraw, ImageFont, ImageColor
import pygame

import os
import io
# import imageio

import sys

def bytes_to_int(bytes):
    result = 0
    for b in bytes:
        result = result * 256 + int(b)
    return result

def int_to_bytes(value, length):
    result = []
    for i in range(0, length):
        result.append(value >> (i * 8) & 0xff)
    result.reverse()
    return result

def byte_array_to_int_array(bytearray):
    i_result = []
    for b in bytearray:
        i = int.from_bytes(b, byteorder='big', signed=False)
        i_result.append(i)
    return i_result

game_image_dir = 'game'
image_number = 1
fname_base = 'fromserver'
fname_ext = '.png'

while True:
    # for sending command asking for image to return using UDP portocol,
    # simply send, doesn't involve any handshake or received feedback
    # note, this port is more like communication between two computers,
    # not exactly server-client structure
    # UDP_IP = "10.44.121.45"
    UDP_IP = "127.0.0.1"
    UDP_PORT = 46087
    command_sock = socket.socket(socket.AF_INET,  # Internet
                                 socket.SOCK_DGRAM)  # UDP

    # for receiving image from TCP, IP and the port to receive from is the same as UDP
    # TCP_IP = '10.44.121.45'
    TCP_IP = '127.0.0.1'
    TCP_PORT = 46087
    BUFFER_SIZE = 1024
    image_sock = socket.socket(socket.AF_INET,  # Internet
                               socket.SOCK_STREAM)  # TCP

    try:
        # construct and send game command to the server
        message = 'G'
        message_bytes_obj = bytearray(message, 'utf-8')  # needed by sock.sendto
        command_sock.sendto(message_bytes_obj, (UDP_IP, UDP_PORT))

        # connect to the server ready to receive image
        image_sock.connect((TCP_IP, TCP_PORT))

        # fname = os.path.join(game_image_dir, '{}_{}.{}'.format(fname_base, image_number, fname_ext))
        fname = '{}_{}.{}'.format(fname_base, image_number, fname_ext)
        image_file = open(fname, 'wb')

        while True:
            data = image_sock.recv(BUFFER_SIZE)  # data is bytearay
            image = Image.fr
            print("received data:", data)
            if not data:
                break
            image_file.write(data)


        buffer = io.BytesIO()
        while True:
            data = sock.recv(BUFFER_SIZE)
            if not data:
                break
            buffer.write(data)


        image_1 = Image.open(buffer)
        image_1.show()
        image_file.close()
        image_number += 1
    finally:
        image_sock.close()


# outfilenr = 1
# while True:
#     try:
#         filename = os.path.join(outdir, 'file%04u.%s' % (outfilenr, imgformat))
#         with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock, \
#                 open(filename, 'wb') as handle:
#             sock.connect((HOST, PORT))
#             while True:
#                 data = sock.recv(102400)
#                 if not (data):
#                     break
#                 handle.write(data)
#             outfilenr += 1
#         time.sleep(0.1)
#     except ConnectionRefusedError:
#         print("Server not running. Waiting.")
#         time.sleep(2)


