import tracemalloc
from multi_model_comp_F import *
tracemalloc.start()
multi_model_comp_F.main()
current, peak = tracemalloc.get_traced_memory()
print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
tracemalloc.stop()