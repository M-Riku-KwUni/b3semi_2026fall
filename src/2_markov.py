import math
import random
import os

import matplotlib.pyplot as plt


def rand_exp(lam):
    """平均発生率 lam の指数分布に従う到着間隔を生成する。"""
    u = random.random()
    return -math.log(1 - u) / lam


def simulate_poisson(lam, T):
    """時間 T の間に発生するイベント数をシミュレーションする。"""
    t = 0.0
    count = 0

    while True:
        t += rand_exp(lam)
        if t > T:
            break
        count += 1

    return count


def poisson_probability(k, lam, T):
    """ポアソン分布 P(X=k) を計算する。"""
    p = math.exp(-lam * T)
    for i in range(1, k + 1):
        p *= lam * T / i
    return p


def main():
    T = 1.0
    N = 10000
    lambdas = [2, 5, 10]
    output_dir = "../report/figure/02"
    os.makedirs(output_dir, exist_ok=True)

    for lam in lambdas:
        counts = [simulate_poisson(lam, T) for _ in range(N)]
        max_k = max(counts)
        x_data = list(range(max_k + 1))

        observed = [counts.count(k) / N for k in x_data]
        theoretical = [poisson_probability(k, lam, T) for k in x_data]

        plt.figure()
        plt.plot(x_data, observed, "o", label="Simulation")
        plt.plot(x_data, theoretical, "x-", label="Poisson distribution")
        plt.xlabel("Number of events k")
        plt.ylabel("Probability")
        plt.title(f"Poisson process (lambda={lam}, T={T}, N={N})")
        plt.xticks(x_data)
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f"lambda_{lam}.png"))
        plt.close()

        print(f"lambda = {lam}")
        print("k  observed  theoretical")
        for k, obs, theo in zip(x_data, observed, theoretical):
            print(f"{k:2d} {obs:8.4f} {theo:11.4f}")
        print()


if __name__ == "__main__":
    main()
