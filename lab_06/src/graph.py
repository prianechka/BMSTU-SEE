import numpy as np
import matplotlib.pyplot as plt

ACAP = np.array([1.46, 1.19, 1, 0.86, 0.71])
PCAP = np.array([1.42, 1.17, 1, 0.86, 0.72])
MODP = np.array([1.24, 1.1, 1, 0.91, 0.82])
TOOL = np.array([1.24, 1.1, 1, 0.91, 0.82])

work = np.zeros(shape=(20,))
time = np.zeros(shape=(20,))
i = 0

project_modes = {
    'c1': [3.2, 3.0, 2.8],
    'p1': [1.05, 1.12, 1.2],
    'c2': [2.5, 2.5, 2.5],
    'p2': [0.38, 0.35, 0.32]
}

proj_type = 1

C1 = project_modes['c1'][proj_type]
P1 = project_modes['p1'][proj_type]
C2 = project_modes['c2'][proj_type]
P = project_modes['p2'][proj_type]

CPLX = 1
SIZE = 25000

levels = ["Очень низкий", "Низкий", "Номинальный", "Высокий", "Очень высокий"]

for el in ACAP:
    work[i] = C1 * CPLX * el * 25 ** P1
    time[i] = C2 * work[i]**P
    i += 1

for el in PCAP:
    work[i] = C1 * CPLX * el * 25 ** P1
    time[i] = C2 * work[i]**P
    i += 1

for el in MODP:
    work[i] = C1 * CPLX * el * 25 ** P1
    time[i] = C2 * work[i]**P
    i += 1

for el in TOOL:
    work[i] = C1 * CPLX * el * 25 ** P1
    time[i] = C2 * work[i]**P
    i += 1

plt.plot(levels, work[:5], label="ACAP")
plt.plot(levels, work[5:10], label="PCAP")
plt.plot(levels, work[10:15], label="MODP", color='red')
plt.plot(levels, work[15:], label="TOOL", color='red')
plt.title("Исследование трудозатрат от драйверов затрат (встроенный тип проекта)")
plt.xlabel("Уровень драйвера")
plt.ylabel("Время в месяцах")
plt.legend()
plt.show()

plt.plot(levels, time[:5], label="ACAP")
plt.plot(levels, time[5:10], label="PCAP")
plt.plot(levels, time[10:15], label="MODP", color='red')
plt.plot(levels, time[15:], label="TOOL", color='red')
plt.title("Исследование времени от драйверов затрат (встроенный тип проекта)")
plt.xlabel("Уровень драйвера")
plt.ylabel("Время в месяцах")
plt.legend()
plt.show()