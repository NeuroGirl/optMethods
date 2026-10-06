funct = [int(x) for x in input("Введите коэффициенты целевой функции через пробел: ").split()]
limits = []
i = True
print("Введите коэффициенты огрничений через пробел, знак(<=, >=, =) и коэффциент справа (для окончания ввода нажмите Enter)")
while i:
    limit = input("Введите ограничения: ")
    if limit == '':
        i = False
    else:
        limits.append(limit)
direct = input("Введите max или min для задачи максимизации или минимизации соответственно: ")

limits_canon = []
b_col = []
alt = 0
art = 0
signs = []

for lim in range(len(limits)):
    limit = limits[lim].split()
    b = float(limit[-1])
    sign = limit[-2]
    signs.append(sign)
    if b < 0:
        b = -b
        coefs = [-x for x in coefs]
        if sign == "<=":
            sign = ">="
        elif sign == ">=":
            sign = "<="
    coefs = [float(x) for x in limit[:-2]]
    if sign not in ["=", ">=", "<="]:
        print("Знак в равенстве/неравенстве должен быть один из: =, >=, <=")
        exit(2)
    else:
        if sign == "=":
            limits_canon.append(coefs)
            b_col.append(b)
        elif sign == "<=":
            limits_canon.append(coefs + alt * [0] + [1])
            alt += 1
            b_col.append(b)
        else:
            limits_canon.append(coefs + alt * [0] + [-1])
            alt += 1
            b_col.append(b)

for limit in limits_canon:
        if len(limit) != len(max(limits_canon, key=len)):
            limit += [0] * (len(max(limits_canon, key=len)) - len(limit))
for i in range(len(limits_canon)):
            limits_canon[i] += art*[0] + [1]
            art += 1
for limit in limits_canon:
            if len(limit) != len(max(limits_canon, key=len)):
                limit += [0] * (len(max(limits_canon, key=len)) - len(limit))

n_original = len(funct)
funct = funct + [0] * (len(limits_canon[0]) - len(funct))

basis = 0
def simplex_method(funct, limits_canon, b_col, q, direction, basis):
    n = len(limits_canon[0])
    m = len(limits_canon)

    simplex_table = [
        [0.0 for _ in range(n + 1)]
        for _ in range(m + 1)
    ]

    for j in range(n):
        if direction == "max":
            simplex_table[0][j] = -funct[j]
        else:
            simplex_table[0][j] = funct[j]
    simplex_table[0][-1] = q

    for i in range(m):
        for j in range(n):
            simplex_table[i + 1][j] = limits_canon[i][j]
        simplex_table[i + 1][-1] = b_col[i]

    if basis is None:
        basis = [n + i for i in range(m)]
    else:
        basis = basis.copy()

    zeros_exist =  not all(x >= 0 for x in simplex_table[0][:-1])
    z = 0
    while zeros_exist:
        col, min_val  = -1, 1e18
        for i in range(n):
            if simplex_table[0][i] < min_val:
                min_val = simplex_table[0][i]
                col = i
        if col == -1:
            print("Нет свободного столбца, симплекс метод невозможно применить для решения задачи")
            exit(2)

        key_row, min_ratio = -1, 1e10
        for i in range(m):
            if simplex_table[i + 1][col] > 0:
                ratio = simplex_table[i + 1][-1] / simplex_table[i+ 1][col]
                if 0 <= ratio < min_ratio:
                    min_ratio, key_row = ratio, i + 1

        if key_row == -1:
            print("Неограниченные решения, симплекс метод невозможно применить для решения задачи")
            exit(2)

        pivot = simplex_table[key_row][col]
        for i in range(n + 1):
            simplex_table[key_row][i] = simplex_table[key_row][i] / pivot

        for i in range(m + 1):
            if i != key_row:
                div = simplex_table[i][col]
                for j in range(n + 1):
                    simplex_table[i][j] = simplex_table[i][j] - div * simplex_table[key_row][j]

        basis[key_row - 1] = col
        z = simplex_table[0][-1]
        zeros_exist = not all(x >= 0 for x in simplex_table[0][:-1])

    ans = [0] * n
    for i in range(m):
        if basis[i] < n:
            ans[basis[i]] = simplex_table[i + 1][-1]

    return z, ans, simplex_table, basis

funct_temp = [0] * len(funct)
g_constant = 0.0 

for i in range(len(limits_canon)):
    lim = limits_canon[i]
    g_constant += b_col[i]

    for j in range(len(funct)-art):
        funct_temp[j] -= lim[j]

temp_z, temp_ans, temp_simplex_table, basis = simplex_method(funct_temp, limits_canon, b_col, -g_constant, 'min', None)

fin_limits_canon = []
fin_b_col = []
for row in temp_simplex_table[1:]:
    fin_limits_canon.append(row[:-1])
    fin_b_col.append(row[-1])
z, ans, simplex_table, basis_new = simplex_method(funct, fin_limits_canon, fin_b_col, temp_z, direct, basis)

if direct == "max":
    print(f"max z = {z:.2f}")
else:
    print(f"min z = {-z:.2f}")
print(f"ans = {[round(x, 2) for x in ans]}")