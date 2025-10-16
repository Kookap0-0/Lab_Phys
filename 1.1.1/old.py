from scipy.optimize import curve_fit
from matplotlib import pyplot as plt
import numpy as np
import math
import pandas as pd

def linear_func(x, a, b):
    return a * x + b

d1 = 0.4 #штангенциркуль, мм
D = pd.read_csv('D:/python/1.1.1/d.csv', sep=';', decimal=',', header = None) #микрометр, мм
R20 = pd.read_csv('D:/python/1.1.1/R20.csv', sep=';', decimal=',', header = None)
R30 = pd.read_csv('D:/python/1.1.1/R30.csv', sep=';', decimal=',', header = None)
R50 = pd.read_csv('D:/python/1.1.1/R50.csv', sep=';', decimal=',', header = None)
d = D.to_numpy()
r20 = R20.to_numpy()
r30 = R30.to_numpy()
r50 = R50.to_numpy()
r20[0, :] = r20[0, :]*4
r30[0, :] = r30[0, :]*4
r50[0, :] = r50[0, :]*4

d2 = np.mean(d[1,:])
d2_std = np.std(d[1, :])/math.sqrt(np.shape(D)[1])
d2_sist = 0.01
d2_delt = math.sqrt(d2_sist**2+d2_std**2)

s = math.pi*d2**2/4
s_delt = 2*s*d2_delt/d2


#Приборная погрешность измерений
x20_err = np.full(r20.shape[1], 4)
y20_err = np.full(r20.shape[1], 0.1)
x30_err = np.full(r30.shape[1], 4)
y30_err = np.full(r30.shape[1], 0.1)
x50_err = np.full(r50.shape[1], 4)
y50_err = np.full(r50.shape[1], 0.1)

#Настройка графика
fig, ax = plt.subplots(figsize=(12, 6), dpi=100)
ax.set_xlabel('Сила тока I (mA)', fontsize=14, fontweight='light', labelpad=10)
ax.set_ylabel('Напряжение V (mV)', fontsize=14, fontweight='light', labelpad=10)
ax.set_title('Зависимость V(I)', fontsize=16, fontweight='semibold', pad=20)
ax.set_xlim(0, 250)
ax.set_ylim(0, 600)

#Точки с крестами погрешностей
ax.errorbar(r20[1,:], r20[0,:], xerr=x20_err, fmt='o', capsize=3,
             color='green', ecolor='green', markersize=2,elinewidth=0.5,
             label='Экспериментальные данные',
             linestyle='')
ax.errorbar(r30[1,:], r30[0,:], xerr=x30_err, fmt='o', capsize=3,
             color='blue', ecolor='blue', markersize=2,elinewidth=0.5,
             label='Экспериментальные данные',
             linestyle='')
ax.errorbar(r50[1,:], r50[0,:], xerr=x50_err, fmt='o', capsize=3,
             color='red', ecolor='red', markersize=2,elinewidth=0.5,
             label='Экспериментальные данные',
             linestyle='')

#Графики МНК и значение сопротивлений
def lsm(list): # Применяем МНК
    params, covariance = curve_fit(linear_func, list[1,:], list[0,:])
    x = np.linspace(0, max(list[1,:])*1.15, 100)
    y= params[0] * x + params[1]
    return x,y,params[0]
x20, y20, resist20 = lsm(r20)
x30, y30, resist30 = lsm(r30)
x50, y50, resist50 = lsm(r50)
ax.plot(x20,y20, label='20cm theory', marker='o',color='green',linewidth=0.5,ms=0)
ax.plot(x30,y30, label='30cm theory', marker='o',color='blue',linewidth=0.5,ms=0)
ax.plot(x50,y50, label='50cm theory', marker='o',color='red',linewidth=0.5,ms=0)
plt.show()
print(resist20, resist30, resist50)