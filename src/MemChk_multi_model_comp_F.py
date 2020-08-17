import tracemalloc
from multi_model_comp_F import Model_Run 
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("VALnits")
parser.add_argument("VALpits")
parser.add_argument("VALburnin")
#parser.set_defaults(VALnits=1000,VALpits=100,VALburnin=500)
args = parser.parse_args()

##tracemalloc.start()
print("VALnits,VALpits,VALburnin")
print(VALnits,VALpits,VALburnin, sep=',')
Model_Run(VALnits,VALpits,VALburnin)
##current, peak = tracemalloc.get_traced_memory()
##print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
##tracemalloc.stop()
