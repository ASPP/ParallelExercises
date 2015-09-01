from multiprocessing import Process, Value, Array, Lock
import mythreads

num = Value('d', 0.0)
arr1 = Array('i', list(range(10)))
arr2 = Array('i', list(range(20)))

# lock obj for read and write
lock = Lock()

p1 = Process(target=mythreads.g, args=(num, arr1,lock))
p2 = Process(target=mythreads.g, args=(num, arr2,lock))
p1.start(); p2.start()
p1.join(); p2.join()

print(num.value)

