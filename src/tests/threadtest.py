import pandas as pd
import threading
import time
from copy import deepcopy

class Test:
    def __init__(self):
        self.df = pd.DataFrame({'a': [1,2,3], 'b': ['one', 'two', 'three']})
        x = threading.Thread(target=self.add_to)
        x.start()

        #flush_time = time.time() + 5
        while True:
            #if time.time() >= flush_time:
            y = threading.Thread(target=self.flush_fun)
            y.start()
            y.join()
                #flush_time = flush_time + 5

    def add_to(self):
        counter = 4
        while True:
            self.df = self.df.append({'a': counter, 'b': 'four'}, ignore_index=True)
            counter += 1
            print('add_to')
            time.sleep(.5)

    def flush_fun(self):
        print('start flush')
        time.sleep(5)
        temp = deepcopy(self.df)
        print(temp)
        print("end flush_fun")


if __name__=="__main__":
    z = Test()