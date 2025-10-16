from scipy.optimize import curve_fit
from matplotlib import pyplot as plt
import numpy as np
import math
import pandas as pd

D10 = pd.read_csv('D:/python/1.1.4/10.csv', header = None)
D20 = pd.read_csv('D:/python/1.1.4/20.csv', header = None)
D40 = pd.read_csv('D:/python/1.1.4/40.csv', header = None)
D80 = pd.read_csv('D:/python/1.1.4/80.csv', header = None)

d10 = D10.to_numpy().reshape(10,40)
d10 = D10.to_numpy().reshape(10,40)
d10 = D10.to_numpy().reshape(10,40)
d10 = D10.to_numpy().reshape(10,40)

print(d10)