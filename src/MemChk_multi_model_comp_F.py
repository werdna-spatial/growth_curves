import tracemalloc
import multi_model_comp_F 
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--MemCheck', dest='MemChk', action='store_true')
parser.add_argument("NumIter")
parser.set_defaults(MemChk=False, NumIter=1000)
args = parser.parse_args()

if MemChk:
  tracemalloc.start()
Model_Run(NumIter)
if MemChk:
  current, peak = tracemalloc.get_traced_memory()
  print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
  tracemalloc.stop()
