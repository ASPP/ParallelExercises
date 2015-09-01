from multiprocessing import Process, Value, Array
import mythreads

num = Value('d', 0.0)
arr1 = Array('i', range(10))
arr2 = Array('i', range(20))

p1 = Process(target=mythreads.f, args=(num, arr1))
p2 = Process(target=mythreads.f, args=(num, arr2))
p1.start(); p2.start()
p1.join(); p2.join()

print num.value

