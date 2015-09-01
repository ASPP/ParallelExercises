import multiprocessing
import time
import numpy.random
from functools import reduce

def f(n, a):
    factor = 5
    time.sleep(numpy.random.uniform()/factor)
    tmp = n.value
    time.sleep(numpy.random.uniform()/2/factor)
    n.value = tmp + reduce(lambda x,y: x+y, a)

def g(n, a, lock):
    
    lock.acquire()
    time.sleep(numpy.random.uniform()/5)
    tmp = n.value
    time.sleep(numpy.random.uniform()/20)
    n.value = tmp + reduce(lambda x,y: x+y, a)
    lock.release()

def h(n, a, lock):
    lock.acquire()
    time.sleep(numpy.random.uniform()/5)
    tmp = n.value
    time.sleep(numpy.random.uniform()/20)
    n.value = tmp + reduce(lambda x,y: x+y, a)

    
