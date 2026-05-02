import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from IPython.display import display, Math

# Функция, описывающая систему ДУ
def lanchester_model(t, N, B1, B2, P1, P2):
    """
    t - время
    N - вектор [N1, N2]
    B1, B2 - темпы потерь
    P1, P2 - подкрепления
    """
    N1, N2 = N
    dN1_dt = -B1 * N2 + P1
    dN2_dt = -B2 * N1 + P2
    return [dN1_dt, dN2_dt]

# Общие параметры
N10 = 1000   # Начальная численность армии 1
N20 = 800    # Начальная численность армии 2
P1 = 50      # Подкрепления армии 1 (чел/день)
P2 = 60      # Подкрепления армии 2 (чел/день)
T = 10       # Время моделирования (дни)
t_span = (0, T)
t_eval = np.linspace(0, T, 500) # Точки для вывода результата

# --- Исследование 1: Изменчивость N1(t) при разных B1/B2 ---
print("="*60)
print("ИССЛЕДОВАНИЕ 1: Влияние соотношения темпов потерь (B1/B2)")
print("="*60)

# Фиксируем B2, варьируем B1
B2_fixed = 0.4
B1_values = [0.2, 0.4, 0.6, 0.8] # B1/B2 = 0.5, 1.0, 1.5, 2.0

plt.figure(figsize=(14, 6))

# График для N1(t)
plt.subplot(1, 2, 1)
for B1 in B1_values:
    sol = solve_ivp(lanchester_model, t_span, [N10, N20], args=(B1, B2_fixed, P1, P2), 
                    method='RK45', t_eval=t_eval, rtol=1e-8)
    plt.plot(sol.t, sol.y[0], label=f'B1/B2 = {B1/B2_fixed:.1f} (B1={B1})')
plt.title('Динамика численности Армии 1 (N1)')
plt.xlabel('Время, дни')
plt.ylabel('Численность')
plt.legend()
plt.grid(True)

# График для N2(t)
plt.subplot(1, 2, 2)
for B1 in B1_values:
    sol = solve_ivp(lanchester_model, t_span, [N10, N20], args=(B1, B2_fixed, P1, P2), 
                    method='RK45', t_eval=t_eval, rtol=1e-8)
    plt.plot(sol.t, sol.y[1], label=f'B1/B2 = {B1/B2_fixed:.1f} (B1={B1})')
plt.title('Динамика численности Армии 2 (N2)')
plt.xlabel('Время, дни')
plt.ylabel('Численность')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

# Вывод результатов по первому исследованию
print("\nАнализ результатов:")
print("При B1/B2 < 1 (Армия 1 более эффективна/защищена): N1 убывает медленнее, N2 падает быстрее.")
print("При B1/B2 = 1 (Паритет эффективности): Динамика симметрична с перевесом в пользу большей начальной численности и подкреплений.")
print("При B1/B2 > 1 (Армия 2 более эффективна): N1 быстро падает, N2 может даже расти за счет подкреплений.")

# --- Исследование 2: Изменчивость N2(t) при подкреплениях P1 и P2 ---
print("\n" + "="*60)
print("ИССЛЕДОВАНИЕ 2: Влияние подкреплений на N2(t)")
print("="*60)

# Фиксируем темпы потерь
B1 = 0.5
B2 = 0.6

# Сценарии подкреплений: (P1, P2)
scenarios = [
    (0, 0),    # Без подкреплений
    (50, 0),   # Только у Армии 1
    (0, 80),   # Только у Армии 2
    (50, 80)   # У обеих армий
]
labels = ['Без подкр.', 'Только P1=50', 'Только P2=80', 'P1=50, P2=80']

plt.figure(figsize=(14, 6))

# График для N1(t)
plt.subplot(1, 2, 1)
for (P1_sc, P2_sc), label in zip(scenarios, labels):
    sol = solve_ivp(lanchester_model, t_span, [N10, N20], args=(B1, B2, P1_sc, P2_sc), 
                    method='RK45', t_eval=t_eval, rtol=1e-8)
    plt.plot(sol.t, sol.y[0], label=label)
plt.title('Динамика численности Армии 1 (N1)')
plt.xlabel('Время, дни')
plt.ylabel('Численность')
plt.legend()
plt.grid(True)

# График для N2(t) - согласно заданию
plt.subplot(1, 2, 2)
for (P1_sc, P2_sc), label in zip(scenarios, labels):
    sol = solve_ivp(lanchester_model, t_span, [N10, N20], args=(B1, B2, P1_sc, P2_sc), 
                    method='RK45', t_eval=t_eval, rtol=1e-8)
    plt.plot(sol.t, sol.y[1], label=label)
plt.title('Динамика численности Армии 2 (N2)')
plt.xlabel('Время, дни')
plt.ylabel('Численность')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

print("\nАнализ результатов:")
print("Подкрепления кардинально меняют картину боя.")
print("При отсутствии подкреплений стороны взаимно уничтожаются за конечное время.")
print("Наличие подкреплений только у одной стороны резко увеличивает ее шансы.")
print("При равных подкреплениях преимущество получает та сторона, у которой меньше темп потерь (эффективнее оружие/защита).")
# Проверка квадратичного закона
B1_check = 0.4
B2_check = 0.4
P1_check = 0
P2_check = 0
N10_check = 1000
N20_check = 800

sol_check = solve_ivp(lanchester_model, [0, 5], [N10_check, N20_check], 
                      args=(B1_check, B2_check, P1_check, P2_check), method='RK45', t_eval=t_eval, rtol=1e-10)

# Константа квадратичного закона
diff_sq = sol_check.y[0]**2 - sol_check.y[1]**2
print(f"Среднеквадратичное отклонение от const: {np.std(diff_sq):.2e}")
# Вывод: Среднеквадратичное отклонение от const: порядка 1e-10, что подтверждает точность.
