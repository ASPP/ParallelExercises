from mpi4py import MPI
import numpy
import math
from time import time

# mpiexec -n X python mpi_matmul.py

COMM = MPI.COMM_WORLD
num_cpus = COMM.size
rank = COMM.rank    


# get a dimension which is multiple of # of cpus
N = 4096
x = N//num_cpus*num_cpus
#y = 2048
y = 256
print("x=%d" % x)

step = x//num_cpus


# scatter destination
domain = numpy.empty((step,y),dtype='d')

# gather destination
c = numpy.empty((x,x),dtype='d')


print("CPU %d of %d: Hello world from %s!" % (rank,num_cpus, MPI.Get_processor_name()))

if rank==0:
    # central source process

    # two matrices to multiply
    a = numpy.random.uniform(size=(x,y)).astype('d')
    b = numpy.random.uniform(size=(y,x)).astype('d')

else:
    # target buffers
    a = numpy.empty((x,y),dtype='d')
    b = numpy.empty((y,x),dtype='d')


t1 = time()
# broadcast 2nd matrix
COMM.Bcast([b,MPI.DOUBLE])

COMM.Scatter([a,MPI.DOUBLE],[domain,MPI.DOUBLE])
ans = numpy.dot(domain,b)    
COMM.Gather([ans,MPI.DOUBLE],[c,MPI.DOUBLE])

t2 = time()-t1
if rank==0:
    print("MPI matmul on %d CPUS (s)" % num_cpus, t2)

if rank==0:
    t1 = time()
    single_c = numpy.dot(a,b)
    print("1 CPU (s)", time()-t1)

    
    print(numpy.alltrue(abs(c-single_c)<1e-5))

