import numpy as np
def lsm(x,y):
    n = len(x)
    x_mean=np.mean(x)
    y_mean=np.mean(y)
    x2=np.mean(x**2)
    y2=np.mean(y**2)
    xy=np.mean(x*y)
    D_xx = x2-x_mean**2 #дисперсия x
    D_yy = y2-y_mean**2 # дисперсия y
    D_xy = xy-x_mean*y_mean # ковариация x,y
    k = D_xy/D_xx
    b = y_mean-k*x_mean
    sigma_k_random = np.sqrt((D_yy/D_xx-k**2)/(n-1)) # случайная погрешность k
    sigma_b_random = sigma_k_random*np.sqrt(x2) # случайная погрешность b
    x = np.linspace(0, np.max(x), 20)
    y = k*x+b
    return x, y, k, sigma_k_random, b, sigma_b_random
def syst(Sx, Xmax, Sy, Ymax, k): # Sx - приборная погрешность x, Xmax - максимальное значение x
    return k*np.sqrt((Sx/Xmax)**2+(Sy/Ymax)**2) # систематическая (приборная) погрешность k
def err(s_random, s_syst):
    return np.sqrt(s_random**2+s_syst**2)
def lsm1(x):
    n = len(x)
    x_mean=np.mean(x)
    x2=np.mean(x**2)
    return x_mean, np.sqrt((x2-x_mean**2)/n)
