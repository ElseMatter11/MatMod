import numpy as np
import matplotlib.pyplot as plt

L = 9.0
W = 9.0
H_net = 2.43
H0 = 2.5
V0 = 12.0
theta0_deg = 45.0
g = 9.81

theta0 = np.radians(theta0_deg)
Vz = V0 * np.sin(theta0)
V_hor = V0 * np.cos(theta0)

def check_trajectory(x0, y0, alpha):
    Vx = V_hor * np.cos(alpha)
    Vy = V_hor * np.sin(alpha)

    if Vy <= 0:
        return False

    t_net = (L - y0) / Vy
    z_net = H0 + Vz * t_net - 0.5 * g * t_net**2
    if z_net <= H_net:
        return False

    discriminant = Vz**2 + 2 * g * H0
    t_land = (Vz + np.sqrt(discriminant)) / g

    if t_land <= t_net:
        return False

    x_land = x0 + Vx * t_land
    y_land = y0 + Vy * t_land

    if (L <= y_land <= 2*L) and (0 <= x_land <= W):
        return True
    else:
        return False

dx = 0.2
dy = 0.2
d_alpha = 0.05

x_range = np.arange(0, W + dx, dx)
y_range = np.arange(0, L + dy, dy)
X, Y = np.meshgrid(x_range, y_range)
Z = np.zeros_like(X, dtype=bool)

alpha_range = np.arange(0.01, np.pi - 0.01, d_alpha)

total_points = len(x_range) * len(y_range)
processed = 0

print("Начало расчета. Всего точек для проверки:", total_points)

for i, x0 in enumerate(x_range):
    for j, y0 in enumerate(y_range):
        for alpha in alpha_range:
            if check_trajectory(x0, y0, alpha):
                Z[j, i] = True
                break

        processed += 1
        if processed % 500 == 0:
            print(f"Обработано {processed}/{total_points} точек")

print("Расчет завершен.")

success_count = np.sum(Z)
print(f"Количество успешных точек: {success_count} из {total_points}")

plt.figure(figsize=(10, 6))

plt.pcolormesh(X, Y, Z, cmap='RdYlGn', alpha=0.8, edgecolor='none')

plt.axhline(y=L, color='black', linewidth=2, label='Сетка (Y = 9м)')
plt.axvline(x=0, color='grey', linestyle='--')
plt.axvline(x=W, color='grey', linestyle='--')
plt.axhline(y=0, color='grey', linestyle='--')

plt.title('Область на своей половине, из которой возможен\nперевод мяча на сторону соперника')
plt.xlabel('X (вдоль сетки), м')
plt.ylabel('Y (к сетке), м')
plt.xlim(0, W)
plt.ylim(0, L)
plt.gca().set_aspect('equal', adjustable='box')
plt.grid(True, linestyle=':', alpha=0.7)

import matplotlib.patches as mpatches
green_patch = mpatches.Patch(color='green', label='Попадание возможно')
red_patch = mpatches.Patch(color='red', label='Попадание невозможно')
plt.legend(handles=[green_patch, red_patch, mpatches.Patch(color='black', label='Сетка')])
plt.show()
