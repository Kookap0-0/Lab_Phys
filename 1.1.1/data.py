from scipy.optimize import curve_fit
from matplotlib import pyplot as plt
import numpy as np
import math
import pandas as pd
import lsm

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

d2,d2_std = lsm.lsm1(d[1,:])
d2_delt = lsm.err(d2_std, 0.01)

s = math.pi*d2**2/4
s_delt = 2*s*d2_delt/d2

#Приборная погрешность измерений
x20_err = np.full(r20.shape[1], 4)
y20_err = 0.002 * r20[1, :] + 0.02
x30_err = np.full(r30.shape[1], 4)
y30_err = 0.002 * r30[1, :] + 0.02
x50_err = np.full(r50.shape[1], 4)
y50_err = 0.002 * r50[1, :] + 0.02

#Настройка графика
fig, ax = plt.subplots(figsize=(12, 6), dpi=100)
ax.set_xlabel('Сила тока I (mA)', fontsize=14, fontweight='light', labelpad=10)
ax.set_ylabel('Напряжение V (mV)', fontsize=14, fontweight='light', labelpad=10)
ax.set_title('Зависимость V(I)', fontsize=16, fontweight='semibold', pad=20)
ax.set_xlim(0, 320)
ax.set_ylim(0, 620)
ax.grid(which='major', linestyle='-')
ax.minorticks_on() 
ax.grid(which='minor', linestyle='--', linewidth=0.5)

#Точки с крестами погрешностей
ax.errorbar(r20[1,:], r20[0,:], xerr=x20_err, fmt='o', capsize=3,
             color='green', ecolor='green', markersize=2,elinewidth=0.5,
             label='Экспериментальные данные 20 см',
             linestyle='')
ax.errorbar(r30[1,:], r30[0,:], xerr=x30_err, fmt='o', capsize=3,
             color='blue', ecolor='blue', markersize=2,elinewidth=0.5,
             label='Экспериментальные данные 30 см',
             linestyle='')
ax.errorbar(r50[1,:], r50[0,:], xerr=x50_err, fmt='o', capsize=3,
             color='red', ecolor='red', markersize=2,elinewidth=0.5,
             label='Экспериментальные данные 50 см',
             linestyle='')

x20, y20, resist20, rand20, b20, b20_rand= lsm.lsm(r20[1,:], r20[0,:])
x30, y30, resist30, rand30, b30, b30_rand= lsm.lsm(r30[1,:], r30[0,:])
x50, y50, resist50, rand50, b50, b50_rand= lsm.lsm(r50[1,:], r50[0,:])
ax.plot(x20,y20, label='Прямая МНК 20 см', marker='o',color='green',linewidth=0.5,ms=0)
ax.plot(x30,y30, label='Прямая МНК 30 см', marker='o',color='blue',linewidth=0.5,ms=0)
ax.plot(x50,y50, label='Прямая МНК 50 см', marker='o',color='red',linewidth=0.5,ms=0)
ax.legend()
#plt.savefig('1.1.1/plot.png', dpi = 300)
#plt.show()

#Систематическая погрешность
def dI(Imax):
    return 0.002*Imax + 0.02
def syst(I,dI, V, dV):
    return np.sqrt((dI/I)**2+(dV/V)**2)
Imax20 = 300
Imax30 = 200
Imax50 = 110
dI20 = dI(Imax20)
dI30 = dI(Imax30)
dI50 = dI(Imax50)
Vmax = 600
dV = 2
syst20 = syst(Imax20,dI20, Vmax, dV)
syst30 = syst(Imax30,dI30, Vmax, dV)
syst50 = syst(Imax50,dI50, Vmax, dV)

#Полная погрешность
def sigma(rand, syst):
    return np.sqrt(rand**2+syst**2)
sigma20 = sigma(rand20, syst20)
sigma30 = sigma(rand30, syst30)
sigma50 = sigma(rand50, syst50)

#Пересчет значений сопротивления с поправкой на неидеальность вольтметра
Rv = 5e6
def Rnew(R,Rv):
    return R*(1+R/Rv)
resist20 = Rnew(resist20, Rv)
resist30 = Rnew(resist30, Rv)
resist50 = Rnew(resist50, Rv)

#Нахождение удельного сопротивления и его погрешность
def rho(R,l,S):
    return R*S/l
def sigma_rho(rho, S, dS, l, dl, R, dR):
    return rho*(dS/S+dR/R+dl/l)
rho20 = rho(resist20, 0.2, s)
rho30 = rho(resist30, 0.3, s)
rho50 = rho(resist50, 0.5, s)
sigma_rho20 = sigma_rho(rho20, s, s_delt, 0.2, 0.005, resist20, sigma20)
sigma_rho30 = sigma_rho(rho30, s, s_delt, 0.3, 0.005, resist30, sigma30)
sigma_rho50 = sigma_rho(rho50, s, s_delt, 0.5, 0.005, resist50, sigma50)

rho20_most = rho(2.007, 0.2, s)
rho30_most = rho(3.021, 0.3, s)
rho50_most = rho(5.020, 0.5, s)
print(rho20, sigma_rho20)
print(rho30, sigma_rho30)
print(rho50, sigma_rho50)