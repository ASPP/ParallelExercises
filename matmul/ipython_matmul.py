# Start a "ipcluster" to run this script:

# Vanilla
# $ ipcluster start -n 4

# or with MPI support
# $ ipcluster start -n 4 --engines=MPIEngineSetLauncher

# For older versions of ipython, it was like this:
# $ ipcluster local


import subprocess
import numpy
import math
from time import time

# For older versions of ipython
#from IPython.kernel import client
#mec = client.MultiEngineClient()

from ipyparallel import Client
rc = Client()
mec = rc[:]
mec.block=True

init_code = """
import numpy
"""
mec.execute(init_code)

# older versions of ipython
#num_cpus = len(mec.get_ids())
num_cpus = len(mec.targets)

N = 4096
x = math.ceil((N/num_cpus)*num_cpus)
y = 256

# Create a dictionary with objects to
# send once to worker

a = numpy.random.uniform(size=(x,y))
b = numpy.random.uniform(size=(y,x))

# send second matrix to workers
mec['b'] = b

print("starting.")
t1 = time()
ans1 = numpy.dot(a,b)
print("1 CPU:", time()-t1)


# This beautfial code is VERY slow
# note we work with 1000x200 here
# not 4000x200 as with mpi and multiprocessing examples
t1 = time()
mec.scatter('a', a)
mec.execute("c = numpy.dot(a,b)")
ans2 = mec.gather('c')

print("%d CPUs:" % num_cpus, time()-t1)

print("Same?:", numpy.alltrue(abs(ans1-ans2)<1e-11))
