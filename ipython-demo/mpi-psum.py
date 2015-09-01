from mpi4py import MPI
import numpy as np

def psum(a):
    s = np.sum(a)
    rcvBuf = np.array(0.0,'d')
    MPI.COMM_WORLD.Allreduce(s,
        rcvBuf,
        op=MPI.SUM)
    return rcvBuf

def pmean(a):
    n = np.array(len(a),'d')
    N = np.array(0.0,'d')
    local_sum = np.array(np.sum(a),'d')
    s = np.zeros(1,'d')

    MPI.COMM_WORLD.Allreduce(n,
        N,
        op=MPI.SUM)

    print n, N

    MPI.COMM_WORLD.Allreduce(local_sum,
        s,
        op=MPI.SUM)

    print local_sum, s

    return s/N

if __name__=="__main__":
    
    a = np.random.normal(size=(10000,), loc=12345)
    print pmean(a)
