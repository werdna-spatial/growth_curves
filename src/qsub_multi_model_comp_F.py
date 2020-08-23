from multi_model_comp_Fpar import Model_Run
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("RUN_ID")
parser.add_argument("VALnits")
parser.add_argument("VALpits")
parser.add_argument("VALburnin")
parser.set_defaults(RUN_ID=123456789, VALnits=1000, VALpits=100, VALburnin=500)
args = parser.parse_args()

print('RUN_ID, VALnits, VALpits, VALburnin')
print(args.RUN_ID, args.VALnits, args.VALpits, args.VALburnin, sep=',')
Model_Run(str(args.RUN_ID), int(args.VALnits), int(args.VALpits), int(args.VALburnin))