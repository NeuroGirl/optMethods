import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ALLOWED_FUNCS = {"sin": np.sin,"cos": np.cos,"log": np.log,"exp": np.exp,"sqrt": np.sqrt,"pi": np.pi,"tg": np.tanh,"ctg": lambda x: 1/np.tanh(x),"abs": np.abs}

func = input("Введите f(x) = ").strip().replace('^', '**')
a, b, eps = map(float, input("Введите а b eps через пробел: ").split())
f = lambda x: eval(compile(func, "<string>", "eval"), ALLOWED_FUNCS, {'x': x})

n = 1000
x_s = np.linspace(a, b, n)
y_s = np.asarray(f(x_s))
dx = abs(b - a) / (n + 1)
L = abs(np.gradient(y_s).max()/dx)
L += 0.1*L + 1e-9 #Задаем запас 10% + минимальная поправка 

num = 0
x_borders = [a, b]
y_borders = [f(a), f(b)]
f_min = min(y_borders)
x_min = x_borders[np.argmin(y_borders)]
history = []
t_start = time.time()
while num < n:
    num += 1
    xs, ys = [], []
    for i in np.argsort(x_borders):
        xs.append(x_borders[i])
        ys.append(y_borders[i])
    x_borders, y_borders = xs, ys

    candidates = []
    for i in range(1, len(x_borders)):
        xi, xj = x_borders[i - 1], x_borders[i]
        fi, fj = y_borders[i - 1], y_borders[i]
        x_star = 0.5 * (xi + xj) - (fi - fj) / (2 * L)
        x_star = min(max(x_star, xi), xj)
        m_val = max([yi - L * abs(xi - x_star) for xi, yi in zip(x_borders, y_borders)])
        candidates.append((m_val, x_star, i - 1))

    lower_bound = min([c[0] for c in candidates])
    gap = f_min - lower_bound
    history.append((num, f_min, lower_bound, gap))
    if abs(gap) <= eps:
        break

    m_val, x_new, idx = min(candidates)
    y_new = f(x_new)
    x_borders += [x_new]
    y_borders += [y_new]
    if y_new < f_min:
        f_min, x_min = y_new, x_new

t_elapsed = time.time() - t_start

stat = {'x_borders': np.array(x_borders),'y_borders': np.array(y_borders),'x_min': x_min, 'f_min': f_min, 'iterations': num, 'time': t_elapsed, 'L': L,}

x_dense = np.linspace(a, b, 1000)
y_dense = np.asarray(f(x_dense), dtype=float)
xi_samples = stat["x_borders"]
yi_samples = stat["y_borders"]
envelope = np.max([yi_samples[i] - stat["L"] * np.abs(x_dense - xi_samples[i]) for i in range(len(xi_samples))],axis=0)
plt.plot(x_dense, y_dense, label="f(x)")
plt.plot(x_dense, envelope, color="green", label="ломаная", linestyle="--")
plt.scatter(xi_samples, yi_samples, color="green", label="пробы")
plt.scatter([stat["x_min"]],
            [stat["f_min"]],
            color="red", marker="x", s=75, label="минимум")
plt.title("Метод Пиавского–Шуберта\n" + func +f"\nx = {stat['x_min']}, "f"f(x) = {stat['f_min']}, ")
plt.xlabel("x")
plt.ylabel("f(x)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("result.png")

print(f"Найденный минимум: x = {stat['x_min']}, f = {stat['f_min']}")
print(f"Итерации: {stat['iterations']}, Время: {stat['time']} s")
print("result.png — график")