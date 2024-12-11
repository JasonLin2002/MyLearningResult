import socket
import tkinter as tk
import threading

s = None
clientName = ''
clientAddr = ''
#------------------------------Chat Server class-----------------
class ChatServer():
    def __init__(self):
        hostname = socket.gethostname()
        global ipAddr
        ipAddr = socket