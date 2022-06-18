import threading, timeit
ans_array = []
def print_cube(num):
    """
    function to print cube of given num
    """
    #print("Cube: {}".format(num * num * num))
    ans = num * num * num
    ans_array.append(ans)
def print_square(num):
    """
    function to print square of given num
    """
    #print("Square: {}".format(num * num))
    ans = num * num
    ans_array.append(ans)
if __name__ == "__main__":
    start = timeit.default_timer()
    # creating thread
    t1 = threading.Thread(target=print_square, args=(10,))
    t2 = threading.Thread(target=print_cube, args=(10,))
  
    # starting thread 1
    t1.start()
    # starting thread 2
    t2.start()
  
    # wait until thread 1 is completely executed
    t1.join()
    # wait until thread 2 is completely executed
    t2.join()
  
    # both threads completely executed
    stop = timeit.default_timer()
    print('Runtime: ', stop - start)
    print(ans_array)