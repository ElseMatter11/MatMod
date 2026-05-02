import numpy as np
import matplotlib.pyplot as plt

"""
Общие координаты (пример)
"""
x_S, y_S = 0.0, 5.0   # Источник
x_D, y_D = 8.0, 3.0   # Приемник (для отражения)

"""
Функция для расчета x_hit при отражении
"""
def x_hit_reflection(theta, x_S, y_S, y_D):
    return x_S + (y_S + y_D) * np.tan(theta)

"""
Функция для расчета x_hit при преломлении
"""
def x_hit_refraction(theta1, x_S, y_S, y_D, n1, n2):
    x_P = x_S + y_S * np.tan(theta1)
    sin_theta2 = (n1 / n2) * np.sin(theta1)
    theta2 = np.arcsin(sin_theta2)
    return x_P + (-y_D) * np.tan(theta2)

"""
Численное решение уравнения x_hit(theta) = x_D методом бисекции
"""
def find_optimal_angle(func, x_target, bracket, tol=1e-8):
    a, b = bracket
    f_a = func(a) - x_target
    f_b = func(b) - x_target
    if f_a * f_b > 0:
        return None  # Корня в интервале нет
    while (b - a) / 2 > tol:
        c = (a + b) / 2
        f_c = func(c) - x_target
        if f_c == 0.0:
            return c
        if f_a * f_c < 0:
            b = c
            f_b = f_c
        else:
            a = c
            f_a = f_c
    return (a + b) / 2

"""
Задача 1: Закон отражения
"""
print("========== ЗАКОН ОТРАЖЕНИЯ ==========")

theta_opt_ref = find_optimal_angle(
    lambda th: x_hit_reflection(th, x_S, y_S, y_D),
    x_D,
    (0.0, np.pi/2 - 1e-4)
)

theta_opt_ref_analytical = np.arctan((x_D - x_S) / (y_S + y_D))

print("Численный оптимальный угол (град): {:.4f}".format(np.degrees(theta_opt_ref)))
print("Аналитический оптимальный угол (град): {:.4f}".format(np.degrees(theta_opt_ref_analytical)))
print("Совпадение: {:.6e}".format(abs(theta_opt_ref - theta_opt_ref_analytical)))

print("\nИсследование точности попадания:")
delta_theta_deg = np.linspace(-10, 10, 200)
delta_theta = np.radians(delta_theta_deg)
theta_varied = theta_opt_ref + delta_theta
x_hit_varied = x_hit_reflection(theta_varied, x_S, y_S, y_D)
deviation = x_hit_varied - x_D

plt.figure(figsize=(8, 5))
plt.plot(delta_theta_deg, deviation, 'b-')
plt.axhline(0, color='grey', linestyle='--')
plt.axvline(0, color='grey', linestyle='--')
plt.xlabel('Δθ от оптимального, градусы')
plt.ylabel('Отклонение x_hit - x_D, м')
plt.title('Закон отражения: точность попадания')
plt.grid(True, alpha=0.3)
plt.show()

"""
Задача 2: Закон преломления
"""
print("\n========== ЗАКОН ПРЕЛОМЛЕНИЯ ==========")

n1, n2 = 1.0, 1.5
y_D_refr = -3.0

theta_crit = np.arcsin(n2 / n1) if n1 > n2 else np.pi/2

theta_opt_refr = find_optimal_angle(
    lambda th: x_hit_refraction(th, x_S, y_S, y_D_refr, n1, n2),
    x_D,
    (1e-6, theta_crit - 1e-6)
)

if theta_opt_refr is None:
    print("При данных параметрах луч не попадает в приемник (возможно, полное внутреннее отражение).")
else:
    print("Оптимальный угол падения (град): {:.4f}".format(np.degrees(theta_opt_refr)))
    x_hit_opt = x_hit_refraction(theta_opt_refr, x_S, y_S, y_D_refr, n1, n2)
    print("x_hit при оптимальном угле: {:.6f} (цель = {:.2f})".format(x_hit_opt, x_D))

    print("\nИсследование точности попадания:")
    delta_theta1_deg = np.linspace(-5, 5, 200)
    delta_theta1 = np.radians(delta_theta1_deg)
    theta1_varied = theta_opt_refr + delta_theta1

    valid = theta1_varied < theta_crit
    deviation_refr = np.full_like(delta_theta1_deg, np.nan)
    x_hit_refr_varied = np.full_like(delta_theta1_deg, np.nan)

    for i, th in enumerate(theta1_varied):
        if valid[i]:
            x_hit_refr_varied[i] = x_hit_refraction(th, x_S, y_S, y_D_refr, n1, n2)
            deviation_refr[i] = x_hit_refr_varied[i] - x_D

    plt.figure(figsize=(8, 5))
    plt.plot(delta_theta1_deg, deviation_refr, 'r-')
    plt.axhline(0, color='grey', linestyle='--')
    plt.axvline(0, color='grey', linestyle='--')
    plt.xlabel('Δθ1 от оптимального, градусы')
    plt.ylabel('Отклонение x_hit - x_D, м')
    plt.title('Закон преломления: точность попадания')
    plt.grid(True, alpha=0.3)
    plt.show()

    if not np.all(valid):
        print("Предупреждение: часть углов выходит за критический угол ПВО.")

print("\nИсследование завершено.")
