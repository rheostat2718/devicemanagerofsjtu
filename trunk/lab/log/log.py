import os,sys
import time

fd = 2
class log_conf(object):
    """
    class log_conf():

    description: log configure class
    attribution:
        file : file to store log
        mode : 0 - not write anything
               1 - write user operation
               2 - (debug) write each function call
    method:
        __init__(file,mode)

    global callback function:
        log_null(...) : mode 0
        log_simple(...) : mode 1
        log_detail(...) : mode 2
    """
    
    def __init__(self,file,mode):
        self.file_name = file
        #self.file_handle = open(self.file,'w')
        self.file_handle = os.open(file,os.O_APPEND | os.O_WRONLY | os.O_CREAT | os.O_SYNC)
        self.mode = mode
        if mode == 0:
            sys.settrace(log_null)
        elif mode == 1:
            sys.settrace(log_simple)
        elif mode == 2:
            sys.settrace(log_detail)
        else:
            raise ValueError("Unknown mode")
        global fd
        fd = self.file_handle
       
def log_null(frame,event,arg):
    pass

def log_simple(frame,event,arg):
    if event != 'call':
        return
    code = frame.f_code
    fname = code.co_name
    caller = frame.f_back
    ccode = caller.f_code
    cname = ccode.co_name
    os.write(fd,'%s %s "%s" (%s line %d) by '%(time.asctime(),event,fname,code.co_filename,frame.f_lineno))
    os.write(fd,'"%s" (%s line %d) .\n'%(cname,ccode.co_filename,caller.f_lineno))
    
def log_detail(frame,event,arg):
#    if event != 'call':
#        return
    code = frame.f_code
    fname = code.co_name
    caller = frame.f_back
    ccode = caller.f_code
    cname = ccode.co_name
    os.write(fd,'%s %s "%s" (%s line %d) by '%(time.asctime(),event,fname,code.co_filename,frame.f_lineno))
    os.write(fd,'"%s" (%s line %d) .\n'%(cname,ccode.co_filename,caller.f_lineno))
#    print dir(frame),arg

def log_exec(file,mode,func):
    cb = sys.gettrace()
    p = log_conf(file,mode)
    #run something
    func()
    sys.settrace(cb)
    pass

if __name__=='__main__':
    def abc():
        pass
    log_exec('log',1,abc)
    abc()
