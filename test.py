import threading
import time
import inspect
from scipy.stats import t

# class Thread(threading.Thread):
#     def __init__(self, t, *args):
#         threading.Thread.__init__(self, target=t, args=args)
#         self.start()

class Thread(threading.Thread):
    def __init__(self, t, *args):
        threading.Thread.__init__(self, target=t, args=args)
        self.start()

count = 0
commonLock = threading.Lock()

def database(lock):
    
    acquired = lock.acquire(0)
    print(acquired)
    while not acquired:
        
        print("Sleeping...")
        time.sleep(1)
        acquired = lock.acquire(0)
    
    print ("database........")
    time.sleep(10)
   
    lock.release()



def getData():
    database(commonLock)
    
    

def main():    
    t1 = threading.Thread(target = getData, args = (), name = "t1")
    t2 = threading.Thread(target = getData, args = (), name = "t2")
    t3 = threading.Thread(target = getData, args = (), name = "t3")
    
    t1.start()
    t2.start()
    t3.start()

# if __name__ == '__main__':
#     main()
    
# price, priceAvg = [], []
# price.append(1)
# priceAvg.append(1)
# 
# print(price)
# print(priceAvg)

print('test')
print(t.ppf(1-0.05, 24))