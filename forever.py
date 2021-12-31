from subprocess import Popen



while True:
    print("\n ReStarting bot1" )
    p = Popen("python " + "bot1.py", shell=True)
    p.wait()