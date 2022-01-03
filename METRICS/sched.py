import time
import schedule

def do_nothing():
    print("HELLLOO")

schedule.every(10).seconds.do(do_nothing)

while 1:
    schedule.run_pending()
    time.sleep(1)