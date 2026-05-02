import numpy as np
import matplotlib.pyplot as plt

# Параметры модели
a, b = 50, 0.7
c, d = 100, 10
e, f = 0.3, 15
M0 = 200

# 1. Уравнение относительно p
# Левая часть: L_p(p) = p * (1 - b)
# Правая часть: R_p(p) = a + c - d * ((e*p - M0)/f)
# Представим как: Левая_новая(p) = Правая_новая(p)
# F(p) = p * (1 - b + d*e/f)
# G(p) = a + c + d*M0/f

coeff_p = 1 - b + (d * e) / f
const_val = a + c + (d * M0) / f

p_solution = const_val / coeff_p
r_solution = (e * p_solution - M0) / f

print(f"Решение системы: p = {p_solution:.2f}, r = {r_solution:.2f}")

# Создаем массив p для визуализации
p_range = np.linspace(0, 1000, 100)

# Функции для графика F(p) и G(p)
L_p = coeff_p * p_range
R_p = np.full_like(p_range, const_val)

# Построение графика для p
plt.figure(figsize=(14, 6))

plt.subplot(1, 2, 1)
plt.plot(p_range, L_p, label=f'L(p) = p * (1 - b + d*e/f) = p * {coeff_p:.3f}', color='blue')
plt.axhline(y=const_val, label=f'R(p) = const = {const_val:.2f}', color='red', linestyle='--')
plt.scatter([p_solution], [coeff_p * p_solution], color='black', zorder=5)
plt.annotate(f'p* = {p_solution:.2f}', (p_solution, coeff_p * p_solution),
             textcoords="offset points", xytext=(10,-10), ha='left')
plt.title('Уравнение относительно p: L(p) = R(p)')
plt.xlabel('p (ВВП)')
plt.ylabel('Значение')
plt.legend()
plt.grid(True)

# 2. Уравнение относительно r
# Выразим p из IS: p = (a + c - d*r) / (1 - b)
# Подставим в LM: M0 = e * ((a + c - d*r) / (1 - b)) - f * r
# Преобразуем к виду L(r) = R(r):
# L(r) = M0*(1 - b) - e*(a + c)
# R(r) = - (e*d + f*(1 - b)) * r

coeff_r = e * d + f * (1 - b)
left_const = M0 * (1 - b) - e * (a + c)

# Создаем массив r для визуализации
r_range = np.linspace(0, 25, 100)

# Функции для графика L(r) = const и R(r)
L_r = np.full_like(r_range, left_const)
R_r = -coeff_r * r_range

plt.subplot(1, 2, 2)
plt.plot(r_range, R_r, label=f'R(r) = - ({coeff_r:.2f}) * r', color='blue')
plt.axhline(y=left_const, label=f'L(r) = const = {left_const:.2f}', color='red', linestyle='--')
plt.scatter([r_solution], [-coeff_r * r_solution], color='black', zorder=5)
plt.annotate(f'r* = {r_solution:.2f}', (r_solution, -coeff_r * r_solution),
             textcoords="offset points", xytext=(10,10), ha='left')
plt.title('Уравнение относительно r: L(r) = R(r)')
plt.xlabel('r (Ставка процента)')
plt.ylabel('Значение')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
