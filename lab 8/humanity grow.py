import numpy as np
import matplotlib.pyplot as plt

"""
Параметры модели (для мирового народонаселения)
"""
K = 11.0         # предельная численность, млрд чел
N0 = 0.6         # начальная численность (примерно 1700 г.), млрд чел
r_default = 0.025  # удельная скорость прироста, 1/год

"""
Аналитическое решение логистического уравнения
"""
def logistic(t, r, K, N0):
    return K / (1 + (K / N0 - 1) * np.exp(-r * t))

"""
Время достижения половины предельной численности
"""
def t_half(r, K, N0):
    return (1.0 / r) * np.log(K / N0 - 1.0)

"""
Раздел 1: Кривая роста населения
"""
t_range = np.linspace(0, 500, 500)

N_default = logistic(t_range, r_default, K, N0)

plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.plot(t_range, N_default, 'b-', linewidth=2, label='N(t)')
plt.axhline(y=K, color='red', linestyle='--', alpha=0.7, label=f'Предел K = {K} млрд')
plt.axhline(y=K/2, color='green', linestyle=':', alpha=0.7, label=f'K/2 = {K/2} млрд')

t_half_default = t_half(r_default, K, N0)
plt.axvline(x=t_half_default, color='green', linestyle=':', alpha=0.5)

plt.plot(t_half_default, K/2, 'go', markersize=8, label=f't1/2 ≈ {t_half_default:.1f} лет')

plt.xlabel('Время t, годы')
plt.ylabel('Численность N, млрд чел.')
plt.title('Логистическая модель роста народонаселения мира')
plt.legend()
plt.grid(True, alpha=0.3)

"""
Раздел 2: Зависимость t1/2 от r
"""
r_range = np.linspace(0.005, 0.1, 200)
t_half_values = t_half(r_range, K, N0)

plt.subplot(1, 2, 2)
plt.plot(r_range, t_half_values, 'r-', linewidth=2)
plt.xlabel('Коэффициент прироста r, 1/год')
plt.ylabel('Время t1/2, годы')
plt.title('Зависимость времени достижения K/2\nот коэффициента прироста r')
plt.grid(True, alpha=0.3)

r_historical = [0.008, 0.015, 0.025, 0.035]
t_half_historical = t_half(np.array(r_historical), K, N0)
plt.scatter(r_historical, t_half_historical, c='blue', s=60, zorder=5)
for i, (r_val, t_val) in enumerate(zip(r_historical, t_half_historical)):
    plt.annotate(f'r={r_val:.3f}\nt={t_val:.1f}', 
                 (r_val, t_val), 
                 textcoords="offset points", 
                 xytext=(10, -15), 
                 fontsize=8)

plt.tight_layout()
plt.show()

"""
Вывод численных результатов
"""
print("========== ЛОГИСТИЧЕСКАЯ МОДЕЛЬ РОСТА НАРОДОНАСЕЛЕНИЯ ==========")
print(f"Параметры модели:")
print(f"  Предельная численность K = {K} млрд чел.")
print(f"  Начальная численность N0 = {N0} млрд чел. (около 1700 г.)")
print(f"  Коэффициент прироста r = {r_default} 1/год")
print(f"\nРезультаты:")
print(f"  Время достижения K/2: t1/2 = {t_half_default:.1f} лет")
print(f"  Год достижения K/2 (от 1700 г.): примерно {1700 + t_half_default:.0f} г.")
print(f"  Максимальная скорость роста (при N=K/2): dN/dt_max = {r_default * K / 4:.3f} млрд чел/год")

print("\nЗависимость t1/2 от r:")
for r_test in [0.01, 0.02, 0.03, 0.05, 0.10]:
    t_test = t_half(r_test, K, N0)
    print(f"  r = {r_test:.3f} 1/год  -->  t1/2 = {t_test:.1f} лет")

print("\nВывод: t1/2 обратно пропорционально r. Формула: t1/2 = (1/r) * ln(K/N0 - 1)")

"""
Дополнительно: сравнение методов для разных N0
"""
plt.figure(figsize=(8, 5))
r_fixed = 0.025
N0_values = [0.1, 0.3, 0.6, 1.0, 2.0]
for N0_i in N0_values:
    N_t = logistic(t_range, r_fixed, K, N0_i)
    plt.plot(t_range, N_t, label=f'N0 = {N0_i} млрд')

plt.axhline(y=K, color='black', linestyle='--', alpha=0.5, label=f'K = {K}')
plt.xlabel('Время t, годы')
plt.ylabel('Численность N, млрд чел.')
plt.title('Влияние начальной численности N0\nна динамику роста (r = {:.3f})'.format(r_fixed))
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
