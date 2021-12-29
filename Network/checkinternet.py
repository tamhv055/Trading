import urllib.request
import socket



def Connect_on_Binance():
    try:
        urllib.request.urlopen('https://www.binance.com', timeout=1)
        return True
    except socket.timeout as err: 
        return False

def Connect_on_Firebase():
    try:
        urllib.request.urlopen('https://firebase.google.com/', timeout=1)
        return True
    except socket.timeout as err: 
        return False


def wait_for_connection_Binance():
    while True:
        try:
            response = urllib.request.urlopen('https://www.binance.com',timeout=1)
            return
        except :
            pass

def wait_for_connection_firebase():
    while True:
        try:
            response = urllib.request.urlopen('https://firebase.google.com/',timeout=1)
            return
        except :
            pass



def wait_for_internet_connection():
    while True:
        try:
            response = urllib.request.urlopen('http://74.125.113.99',timeout=1)
            return
        except :
            pass