import time
import logging

def basic_setting():
    LOG_FILE='dmlog'
    LOG_FORMAT = '%(asctime)-15s '+logging.BASIC_FORMAT
    logging.basicConfig(filename=LOG_FILE,format=LOG_FORMAT,level=logging.DEBUG)

try:
    if LOG_SET==0:
        LOG_SET = 1
except NameError:
    LOG_SET = 1
    basic_setting()
    
if __name__=='__main__':
    logging.debug('Hello World')