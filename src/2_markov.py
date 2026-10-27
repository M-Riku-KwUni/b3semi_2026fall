import math
import os
import random
import sys

from scatfig import ScatFig


def rand_exp(lam):
    """発生率 lam の指数分布に従う到着間隔を生成する。"""
    u = random.random()
    return -math.log(1 - u) / lam


def main():
    if len(sys.argv) not in (3, 4):
        print("Usage: python 2_markov.py lam t_end [figure.png]")
        sys.exit(1)

    lam = float(sys.argv[1])
    t_end = int(sys.argv[2])
    T = 1.0

    if not math.isfinite(lam) or lam <= 0:
        raise ValueError("lam must be a positive finite number")
    if t_end < T:
        raise ValueError("t_end must be at least 1")

    # 観測時間を T ごとの区間に分け、各区間の到着数を数える
    n_intervals = int(t_end // T)
    counts = [0] * n_intervals

    ta = 0.0
    while True:
        ta += rand_exp(lam)
        if ta >= n_intervals * T:
            break
        interval = int(ta // T)
        counts[interval] += 1

    # F(k): k 回到着した区間の相対度数
    k_max = max(counts)
    freq = [0] * (k_max + 1)
    for k in counts:
        freq[k] += 1
    F = [n / n_intervals for n in freq]

    # P(k): 平均 lam*T のポアソン分布
    mean = lam * T
    P = [math.exp(-mean)]
    for k in range(k_max):
        P.append(P[k] * mean / (k + 1))

    k_data = list(range(k_max + 1))
    fig = ScatFig()
    fig.add_data(k_data, F, "F(k): Simulation")
    fig.add_data(k_data, P, "P(k): Poisson distribution")
    fig.set_xlabel("Number of events k")
    fig.set_ylabel("Probability")

    if len(sys.argv) == 4:
        fig_filename = sys.argv[3]
        output_dir = os.path.dirname(fig_filename)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
    else:
        output_dir = os.path.join(
            os.path.dirname(__file__), "..", "report", "figure", "02"
        )
        os.makedirs(output_dir, exist_ok=True)
        fig_filename = os.path.join(
            output_dir, f"lambda_{lam:g}_t_end_{t_end}.png"
        )

    fig.save_fig(fig_filename)

    print(f"lambda = {lam}, t_end = {t_end}, T = {T}")
    print("k  F(k)      P(k)")
    for k, observed, theoretical in zip(k_data, F, P):
        print(f"{k:2d} {observed:8.4f} {theoretical:8.4f}")
    print(f"Figure saved: {fig_filename}")


if __name__ == "__main__":
    main()
