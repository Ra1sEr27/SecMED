from multiprocessing.dummy import Pool as ThreadPool
import timeit, random
from threading import Thread
import threading
def XOR (a, b):
    if a != b:
        return 1
    else:
        return 0

def genR1(R, constR):
    
    R1_Binary = ""
    for i in range(len(R)):
        temp1 = XOR(R[i],constR[i])
        R1_Binary += str(temp1)
    #Transform binary to text
    binary_int = int(R1_Binary, 2)
    # Getting the byte number
    byte_number = binary_int.bit_length() + 7 // 8
    # Getting an array of bytes
    binary_array = binary_int.to_bytes(byte_number, "big")
    R1_text = binary_array.decode('ISO-8859-1')
    #print("R1: ",R1_text)
    return R1_text

start = timeit.default_timer()
R = ""
for i in range(1200):
    temp = str(random.randint(0,1))
    R += temp
#print(len(R))
constR = "111011101110011010000100101111000101000100100101111001010000110010010000110110001111000110010001101111010100010010101110000101000101110100001001011010111100001001110111011101110101111011111011111110010010101010010001101010001000000011001001001111000100100100001001000111011001111001111110100101011111011001101101100110111100111100011100011100011010000010101010011010000011100001011011110011010010001010000010111001010001110011010010000000001001101100010001110111111101100111100000010110000101000011010110010001111000001010011001001001100001101101000101101010010010001101111111011001111111010000011010011101001100001010011111101100011010111101001001100001001100011000001011100010011111010110110100010111011100001100111000101000110110100010111100100111011001101000010100111010100010010011111010110010000111111001010001111111011001110110000001000100010011101010110011001001111011000101001111110111111110010110000111010110000100011001101001000000001101011100110100000000101110001001100000111100111000101110010011001100110110001110001110101100000111000011011010101001111010001110011110110000001101101010100111101000111001111011000"
constR += constR
constR = constR[:len(R)]
#print(len(constR))

R_array = [R[:600], R[601:]]

constR_array = [constR[:600], constR[601:]]

threads = []
# In this case 'urls' is a list of urls to be crawled.
for i in range(len(R_array)):
    # We start one thread per url present.
    process = Thread(target=genR1, args=[R_array[i], constR_array[i]])
    process.start()
    threads.append(process)
# We now pause execution on the main thread by 'joining' all of our started threads.
# This ensures that each has finished processing the urls.
for process in threads:
    process.join()
# pool = ThreadPool(4)
# results = pool.map(genR1, my_array)
# pool.close()
# pool.join()
# t1 = threading.Thread(target=genR1, args = (my_array,), daemon = True)
# t2 = threading.Thread(target=genR1, args = (my_array,), daemon = True)
# t3 = threading.Thread(target=genR1, args = (my_array,), daemon = True)
# t4 = threading.Thread(target=genR1, args = (my_array,), daemon = True)

# t1.start()
# t2.start()
# t3.start()
# t4.start()

# t1.join()
# t2.join()
# t3.join()
# t4.join()
stop = timeit.default_timer()
print('DSXORR & R1 Time: ', stop - start)
#print(results)