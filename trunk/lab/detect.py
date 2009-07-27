#it seems a simple shell script may fulfill the task
#but we may need some post processing ... later
def daemon():
    import time
    import os
    oldconf = '/tmp/conf.old'
    newconf = '/tmp/conf.new'
    os.system('prtconf > '+oldconf)
    while True:
        time.sleep(2)
        os.system('prtconf > '+newconf)
        os.system('diff '+oldconf+' '+newconf)
        os.system('mv '+newconf+' '+oldconf)
        #ch = raw_input('Press enter ...')
if __name__=='__main__':
    daemon()
