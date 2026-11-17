import time
import tracemalloc

start = {1: 5, 2: 9, 3: 22, 4: 16, 5: 18, 6: 20}
middle = {1: 4, 2: 9, 3: 13, 4: 15, 5: 16}
finish = {1: 6, 2: 10, 3: 14, 4: 17, 5: 19}

#start = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
#middle = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
#finish = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}

total_trips = 7
#total_trips = 0

stages = [
    ("конечный", finish, list(finish)),
    ("промежуточный", middle, list(middle)),
    ("начальный", start, [n for n in start if n % 2 == 0]),
]

tracemalloc.start()
time_start = time.perf_counter()

dp = {0: (0, [()])}

if total_trips != 0:
    for stage_index, (name, effects, allowed_counts) in enumerate(stages):
        new_dp = {}

        for used_trips, (old_effect, old_plans) in dp.items():
            for count in allowed_counts:
                new_total = used_trips + count

                if new_total > total_trips:
                    continue

                if stage_index == 2 and new_total < total_trips:
                    continue

                remaining_stages = len(stages) - stage_index - 1
                if new_total + remaining_stages > total_trips:
                    continue

                candidate_effect = old_effect + effects[count]
                candidate_plans = [plan + (count,) for plan in old_plans]

                if new_total not in new_dp or candidate_effect > new_dp[new_total][0]:
                    new_dp[new_total] = (candidate_effect, candidate_plans)
                elif candidate_effect == new_dp[new_total][0]:
                    new_dp[new_total][1].extend(candidate_plans)

        dp = new_dp
else:
        dp = {0: (0, [(0, 0, 0)])}

best_effect, best_plans = dp[total_trips]

elapsed_time = time.perf_counter() - time_start
current_memory, peak_memory = tracemalloc.get_traced_memory()
tracemalloc.stop()

print("Максимальный эффект:", best_effect)
print("Оптимальные планы:")
for plan in best_plans:
    print(f"начальный: {plan[0]}, промежуточный: {plan[1]}, конечный: {plan[2]}")

print(f"Время работы алгоритма: {elapsed_time:.6f} с")
print(f"Пиковая дополнительная память: {peak_memory / 1024:.2f} КБ")