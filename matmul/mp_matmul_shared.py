from multiprocessing import Pool,Process
from multiprocessing import sharedctypes
import ctypes
import numpy
from numpy import ctypeslib

import numpy
from time import time


def mat_rowrange_mul(args):

    # a little ugly, but allows running with a Pool
    # which accept only 1 argument
    a_row_domain = args[0]
    a_shape = args[1]
    b_shape = args[2]
    shared_a = args[3]
    shared_b = args[4]
    shared_c = args[5]

    # access shared memory object as numpy array, set dimensions
    nd_c = ctypeslib.as_array(shared_c).reshape((a_shape[0],b_shape[1]))
    nd_a = ctypeslib.as_array(shared_a).reshape(a_shape)
    nd_b = ctypeslib.as_array(shared_b).reshape(b_shape)

    # write answer to shared memory
    # it would be better if numpy.dot could write "in-place"
    nd_c[a_row_domain[0]:a_row_domain[1],:] = \
    numpy.dot(nd_a[a_row_domain[0]:a_row_domain[1],:],nd_b)

    return None



if __name__ == '__main__':


    x = 4000
    # y = 2000
    y = 200

    num_cpus = 2
    #num_cpus = 4

    a_shape = (x,y)
    b_shape = (y,x)

    # allocate source and dest. arrays
    a = numpy.random.uniform(size=a_shape)
    b = numpy.random.uniform(size=b_shape)
    c = numpy.zeros((x,x))

    # allocated shared memory
    shared_a = sharedctypes.Array(ctypes.c_double,a.flat,lock=False)
    shared_b = sharedctypes.Array(ctypes.c_double,b.flat,lock=False)
    shared_c = sharedctypes.Array(ctypes.c_double,c.flat,lock=False)

    # access the answer as a numpy array, set dimensions
    nd_c = ctypeslib.as_array(shared_c).reshape((a_shape[0],b_shape[1]))

    # 1 process reference
    print "starting."
    t1 = time()
    ans1 = numpy.dot(a,b)
    print "1 CPU:", time()-t1
    
    # x must be a multiple of num_cpus
    assert(x%num_cpus==0)

    step = x/num_cpus

    # define row domains for each process
    domains = zip(numpy.arange(0,x,step),numpy.arange(0,x,step)+step)
    static_args = (a_shape,b_shape,shared_a,shared_b,shared_c)

    # allocate processes
    p = [Process(target=mat_rowrange_mul, args=((x,)+static_args,) ) for x in domains]

    t1 = time()

    for x in p:
        x.start()
    for x in p:
        x.join()

    ans2 = nd_c

    print "%d CPUs:" % num_cpus, time()-t1

    print "Same?:", numpy.alltrue(abs(ans1-ans2)<1e-11)
