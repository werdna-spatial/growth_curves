import tracemalloc
from multi_model_comp_F import Model_Run

tracemalloc.start()
Model_Run()
current, peak = tracemalloc.get_traced_memory()
print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
tracemalloc.stop()
