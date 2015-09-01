from multiprocessing import Process, Value, Array, Lock
import mythreads
import time

num = Value('d', 0.0)
arr1 = Array('i', range(10))
arr2 = Array('i', range(20))

# lock obj for read and write
lock = Lock()

p1 = Process(target=mythreads.h, args=(num, arr1,lock))
p2 = Process(target=mythreads.h, args=(num, arr2,lock))
p1.start(); p2.start()
p1.join()

# p2 is still waiting for release (deadlock)
print p2.is_alive()

# resolve the deadlock without killing processes
lock.release()
time.sleep(1)
print p2.is_alive()
p2.join()

print num.value

