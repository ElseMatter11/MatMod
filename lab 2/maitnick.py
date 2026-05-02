import numpy as np
import matplotlib.pyplot as plt

"""
Параметры установки (примерные, можно менять для исследования)
"""
m = 0.01      # масса пули, кг (10 г)
M = 2.0       # масса маятника, кг
l = 1.5       # длина нити, м
g = 9.81      # ускорение свободного падения, м/с^2

"""
Раздел 1 и 2: Расчет скорости пули двумя методами
Предположим, что измеренный угол отклонения alpha_max известен.
"""
alpha_max_deg = 15.0  # угол отклонения в градусах
alpha_max_rad = np.radians(alpha_max_deg)

h = l * (1 - np.cos(alpha_max_rad))

U = np.sqrt(2 * g * h)

V0_method_1 = (m + M) / m * U

V0_method_2 = np.sqrt(2 * g * l * (1 - np.cos(alpha_max_rad)) * (m + M) / m)

print("Результаты для заданного угла отклонения {:.1f}°:".format(alpha_max_deg))
print("Высота подъема маятника h = {:.4f} м".format(h))
print("Скорость системы после удара U = {:.2f} м/с".format(U))
print("Метод 1 (импульс + энергия): V0 = {:.2f} м/с".format(V0_method_1))
print("Метод 2 (только энергия пули): V0 = {:.2f} м/с".format(V0_method_2))
print("Отношение V0(1) / V0(2) = {:.2f}".format(V0_method_1 / V0_method_2))

"""
Раздел 3: Исследование зависимости угла отклонения от скорости пули
"""
V0_range = np.linspace(50, 500, 200)

U_range = (m / (m + M)) * V0_range

cos_alpha_range = 1 - U_range**2 / (2 * g * l)

valid_indices = cos_alpha_range >= -1.0
V0_valid = V0_range[valid_indices]
cos_alpha_valid = cos_alpha_range[valid_indices]
alpha_max_rad_valid = np.arccos(cos_alpha_valid)
alpha_max_deg_valid = np.degrees(alpha_max_rad_valid)

plt.figure(figsize=(10, 6))
plt.plot(V0_valid, alpha_max_deg_valid, 'b-', linewidth=2)
plt.axhline(y=90, color='r', linestyle='--', label='Граница применимости (90°)')
plt.title('Зависимость угла отклонения маятника от скорости пули')
plt.xlabel('Начальная скорость пули V0, м/с')
plt.ylabel('Максимальный угол отклонения α, градусы')
plt.grid(True, alpha=0.3)
plt.legend()
plt.show()

"""
Раздел 4: Приближение малых углов
"""
alpha_deg = np.linspace(0, 30, 100)
alpha_rad = np.radians(alpha_deg)

sin_alpha = np.sin(alpha_rad)
tan_alpha = np.tan(alpha_rad)

error_sin = np.abs((sin_alpha - alpha_rad) / sin_alpha) * 100
error_tan = np.abs((tan_alpha - alpha_rad) / tan_alpha) * 100

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(alpha_deg, alpha_rad, 'k--', label='α (рад)')
plt.plot(alpha_deg, sin_alpha, 'b-', label='sin(α)')
plt.plot(alpha_deg, tan_alpha, 'r-', label='tan(α)')
plt.title('Сравнение функций малого угла')
plt.xlabel('Угол α, градусы')
plt.ylabel('Значение функции')
plt.legend()
plt.grid(True, alpha=0.3)

plt.subplot(1, 2, 2)
plt.plot(alpha_deg, error_sin, 'b-', label='Погрешность sin(α)≈α')
plt.plot(alpha_deg, error_tan, 'r-', label='Погрешность tan(α)≈α')
plt.title('Относительная погрешность приближения, %')
plt.xlabel('Угол α, градусы')
plt.ylabel('Погрешность, %')
plt.legend()
plt.grid(True, alpha=0.3)
plt.axhline(y=1.0, color='grey', linestyle=':', label='1% погрешность')
plt.tight_layout()
plt.show()

print("\nОтвет на дополнительный вопрос:")
print("Приближение sin(α)≈α и tan(α)≈α выполняется с погрешностью менее 1% при углах менее ~14° (0.24 рад).")
print("Для баллистического маятника это справедливо при достаточно большой массе M,")
print("когда скорость U мала, и, следовательно, угол отклонения не превышает этих значений.")
