import numpy as np
import sympy as sp


def solve_lagrange_numerically(f,constraints,variables,starts=500,search_range=(-5, 5),tolerance=1e-8,seed=None):
    variables = tuple(variables)
    constraints = tuple(constraints)

    multipliers = tuple(sp.symbols(f"lambda:{len(constraints)}", real=True))
    unknowns = variables + multipliers

    L = f + sum(lam * constraint for lam, constraint in zip(multipliers, constraints))

    equations = [sp.diff(L, var) for var in variables] + list(constraints)
    jacobian = sp.Matrix(equations).jacobian(unknowns)

    equation_function = sp.lambdify(unknowns,equations,modules="numpy")
    jacobian_function = sp.lambdify(unknowns,jacobian,modules="numpy")

    rng = np.random.default_rng(seed)
    found = []

    for _ in range(starts):
        point = rng.uniform(search_range[0],search_range[1],size=len(unknowns))

        for _ in range(100):
            values = np.asarray(equation_function(*point),dtype=float).ravel()
            residual_norm = np.linalg.norm(values, ord=np.inf)
            jac = np.asarray(jacobian_function(*point),dtype=float)
            step = np.linalg.solve(jac, -values)

            scale = 1.0
            for _ in range(20):
                candidate = point + scale * step
                candidate_values = np.asarray(equation_function(*candidate),dtype=float).ravel()
                if (np.all(np.isfinite(candidate_values)) and np.linalg.norm(candidate_values, ord=np.inf) < residual_norm):
                    point = candidate
                    break
                scale *= 0.5

        residual = np.asarray(equation_function(*point)).ravel()

        if (np.all(np.isfinite(point))and np.all(np.isfinite(residual))and np.linalg.norm(residual, ord=np.inf) < tolerance):
            if any(np.linalg.norm(point - existing, ord=np.inf) < 1e-6for existing in found):
                continue
            found.append(point)

    return L, equations, unknowns, found


if __name__ == "__main__":
    x, y = sp.symbols("x y", real=True)

    f = x * y
    variables = [x, y]
    constraints = [x**2 + y**2 - 2]

    L, equations, unknowns, solutions = solve_lagrange_numerically(f=f,constraints=constraints,variables=variables,seed=8)

    print("L =", L)
    print("\nСистема:")
    for equation in equations:
        print(f"{equation} = 0")

    print("\nНайденные решения:")
    for index, solution in enumerate(solutions, start=1):
        point = {variable: float(value)for variable, value in zip(variables, solution)}
        rounded_solution = {str(symbol): round(float(value), 3)for symbol, value in zip(unknowns, solution)}
        objective_value = float(sp.N(f.subs(point)))
        constraint_residuals = [float(sp.N(constraint.subs(point)))for constraint in constraints]

        print(f"\nРешение {index}:")
        print("  Корень:", rounded_solution)
        print(f"  f в корне: {objective_value:.2f}")
        if constraint_residuals:
            print("  Невязки ограничений:")
            for constraint_index, residual in enumerate(constraint_residuals,start=1):
                print(f"    g{constraint_index} = {residual:.3f}")