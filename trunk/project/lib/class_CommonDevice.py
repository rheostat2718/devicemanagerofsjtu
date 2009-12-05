import os

class CommonDevice:
    def __init__(self):
        txt=os.popen('./all_devices')
        for t in txt.readlines():
            ts=t.split(":")
            for ss in ts:
                print ss,
        txt.close()

cd=CommonDevice()
