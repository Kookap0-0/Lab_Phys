from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import lsm

# LaTeX configuration with Cyrillic support
plt.rcParams.update({
    'text.usetex': True,
    'font.family': 'serif',
    'text.latex.preamble': r'\usepackage[utf8]{inputenc} \usepackage[russian]{babel}',
})

nu = pd.read_csv('D:/python/1.4.5/1.4.5.csv', sep=';', decimal='.', header=None).to_numpy()
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
labels = nu[0,1:]
u2 = np.zeros(5)
u2_err = np.zeros(5)
L = 0.5 # 0.5 м - длина струны
dL = 0.001

fig, ax = plt.subplots(figsize=(12, 6), dpi=100)
ax.set_xlabel(r'Номер гармоники $n$', fontsize=14, fontweight='light', labelpad=10)
ax.set_ylabel(r'Частота колебаний струны $\nu_n$, Гц', fontsize=14, fontweight='light', labelpad=10)
ax.set_title(r'Зависимость частоты от номера гармоники', fontsize=16, fontweight='semibold', pad=20)
ax.set_xlim(0, 10)
ax.set_ylim(0, 2100)
ax.grid(which='major', linestyle='-')
ax.minorticks_on() 
ax.grid(which='minor', linestyle='--', linewidth=0.5)

fig2, ax2 = plt.subplots(figsize=(12, 6), dpi=100)
ax2.set_xlabel(r'Сила натяжения $T$, Н', fontsize=14, fontweight='light', labelpad=10)
ax2.set_ylabel(r'Скорость $u^2, \ (m/c)^2$', fontsize=14, fontweight='light', labelpad=10)
ax2.set_title(r'Зависимость квадрата скорости от силы натяжения', fontsize=16, fontweight='semibold', pad=20)
ax2.grid(which='major', linestyle='-')
ax2.minorticks_on() 
ax2.grid(which='minor', linestyle='--', linewidth=0.5)


nu_error = [0.1]
for i in range(1,9):
    nu_error.append(1)
nu_error = np.array(nu_error)

for i in range(0,5):
    x, y, k, sigma_k_random, b, sigma_b_random = lsm.lsm(nu[1:,0],nu[1:,i+1])
    ax.plot(x,y, marker='o',color=colors[i],linewidth=0.5,ms=0)
    ax.errorbar(nu[1:,0], nu[1:,i+1], yerr=nu_error, fmt='o', capsize=1,
             color=colors[i], ecolor=colors[i], markersize=2,elinewidth=0.5,
             label=r"$T = " + str(labels[i]) + r"$ Н",
             linestyle='')
    u2[i] = (2*L*k)**2
    u2_err[i] = 4*dL*sigma_k_random*u2[i]


x, y, k, sigma_k_random, b, sigma_b_random = lsm.lsm(nu[0,1:],u2)
ax2.plot(x,y, marker='o',color=colors[3],linewidth=0.5,ms=0)
ax2.errorbar(nu[0,1:], u2, yerr=u2_err, fmt='o', capsize=1,
            color=colors[3], ecolor=colors[3], markersize=2,elinewidth=0.5,
            linestyle='')

ro_l = (f"({1/k:.2e}, {sigma_k_random/(k**2):.1e})")

ax2.set_xlim(0, max(nu[0,1:]) * 1.1)
ax2.set_ylim(0, max(u2 + u2_err) * 1.1)    

print(ro_l)
ax.legend()
plt.tight_layout()
plt.close(fig)
#fig.savefig('1.4.5/plot.png', dpi = 300)
#fig2.savefig('1.4.5/plot2.png', dpi = 300)
#plt.show()