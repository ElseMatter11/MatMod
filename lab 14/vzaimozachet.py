import numpy as np
import matplotlib.pyplot as plt

# Установка seed для воспроизводимости результатов
np.random.seed(42)

# Количество предприятий
n = 15

# --- 1. Генерация случайной матрицы взаимодолгов ---
# Случайные целые числа от 0 до 100
D = np.random.randint(0, 101, size=(n, n))
# Обнуление диагонали (самим себе не должны)
np.fill_diagonal(D, 0)

print("Матрица долгов D (до взаимозачета):")
print(D)

# --- 2. Проведение взаимозачета ---
D_clear = D.copy().astype(float)  # рабочая матрица

for i in range(n):
    for j in range(i+1, n):
        # Взаимный зачет для пары (i, j)
        min_val = min(D_clear[i, j], D_clear[j, i])
        D_clear[i, j] -= min_val
        D_clear[j, i] -= min_val

print("\nМатрица остаточных долгов D' (после взаимозачета):")
# Округляем для красоты вывода
print(np.round(D_clear, 2))

# --- 3. Расчет сальдо ---
# S_i = сумма того, что должны i (столбец) - сумма того, что должен i сам (строка)
S = np.sum(D_clear, axis=0) - np.sum(D_clear, axis=1)

print("\nИтоговые сальдо предприятий (положительное = должны предприятию):")
for i, s in enumerate(S):
    print(f"Предприятие {i+1}: {s:+.2f}")

print(f"\nСумма всех сальдо (должна быть 0): {np.sum(S):.10f}")

# --- 4. Визуализация ---
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Тепловая карта до взаимозачета
im1 = axes[0].imshow(D, cmap='Reds', interpolation='nearest')
axes[0].set_title('Матрица долгов до взаимозачета')
axes[0].set_xlabel('Кредитор (j)')
axes[0].set_ylabel('Должник (i)')
plt.colorbar(im1, ax=axes[0], fraction=0.046)

# Тепловая карта после взаимозачета
im2 = axes[1].imshow(D_clear, cmap='Greens', interpolation='nearest')
axes[1].set_title('Матрица долгов после взаимозачета')
axes[1].set_xlabel('Кредитор (j)')
axes[1].set_ylabel('Должник (i)')
plt.colorbar(im2, ax=axes[1], fraction=0.046)

# Сальдо
colors = ['green' if s >= 0 else 'red' for s in S]
axes[2].bar(range(1, n+1), S, color=colors)
axes[2].set_title('Итоговое сальдо предприятий')
axes[2].set_xlabel('Номер предприятия')
axes[2].set_ylabel('Сальдо')
axes[2].axhline(y=0, color='black', linewidth=0.5)
axes[2].grid(axis='y', alpha=0.3)

# Подпись значений на столбцах
for i, s in enumerate(S):
    axes[2].text(i+1, s + np.sign(s)*0.5, f'{s:.0f}', ha='center', va='bottom' if s>=0 else 'top')

plt.tight_layout()
plt.show()

# --- 5. Сравнительный анализ ---
total_before = np.sum(D)
total_after = np.sum(D_clear)
reduction = total_before - total_after
print(f"\nСуммарный долг до взаимозачета: {total_before:.0f}")
print(f"Суммарный долг после взаимозачета: {total_after:.0f}")
print(f"Сокращение объема долгов: {reduction:.0f} ({reduction/total_before*100:.1f}%)")
