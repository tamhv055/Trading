from os import popen
from subprocess import Popen

from Data import Firebase





while True:
    print("\n ReStarting bot1" )
    p = Popen("python " + "bot1.py", shell=True)
    p.wait()