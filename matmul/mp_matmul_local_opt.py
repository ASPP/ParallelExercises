from multiprocessing import Pool, cpu_count
import numpy
from time import time


def calc_target(id):
    global a,b
    return numpy.dot(a,b)


def update_pool_global(dict):
    globals().update(dict)

def mat_rowrange_mul(a_row):
    global a,b

    return numpy.dot(a[a_row[0]:a_row[1],:],b) 


def mat_rowcol_mul(a_row):
    global a,b

    return numpy.dot(a[a_row,:],b) 






if __name__ == '__main__':

    num_cpus = cpu_count()
    N = 4096
    #y = 2048
    y = 256
    x = N//num_cpus*num_cpus

    # Create a dictionary with objects to
    # send once to worker
    worker_globals = {}
    a = worker_globals['a'] = numpy.random.uniform(size=(x,y))
    b = worker_globals['b'] = numpy.random.uniform(size=(y,x))

    print("starting.")
    t1 = time()
    ans1 = numpy.dot(a,b)
    print("1 CPU:", time()-t1)
    
    p = Pool(num_cpus,update_pool_global,(worker_globals,))

    #domains = ((0,999),(1000,1999),(2000,2999),(3000,3999))
    step = x//num_cpus
    domains = zip(numpy.arange(0,x,step),numpy.arange(0,x,step)+step)


    t1 = time()
    tmp = p.map(mat_rowrange_mul, domains)

    ans2 = numpy.empty((x,x))

    for i,domain in enumerate(domains):
        ans2[domain[0]:domain[1],:] = tmp[i]

    print("%d CPUs:" % num_cpus, time()-t1)

    

    # ans2 needs a bit of reformatting

    print("Same?:", numpy.alltrue(abs(ans1-ans2)<1e-11))
