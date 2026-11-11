import math
import os
import random
import sys

from scatfig import ScatFig


def rand_exp(rate):
    """平均 1/rate の指数分布に従う時間を生成する。"""
    u = random.random()
    return -math.log(1 - u) / rate


def rand_service_time(mu, distribution):
    """平均 1/mu のサービス時間を指定した分布から生成する。"""
    if distribution == "M":
        return rand_exp(mu)

    if distribution == "D":
        return 1 / mu

    if distribution == "U":
        return random.uniform(0, 2 / mu)

    if distribution == "P":
        # パレート分布の平均を 1/mu にする（alpha > 2）。
        alpha = 2.1
        x_min = (alpha - 1) / (alpha * mu)
        return random.paretovariate(alpha) * x_min

    raise ValueError("Unknown service-time distribution")


def simulate_mmss(lam, mu, servers, endtime, distribution):
    """M/M/S/S または M/G/S/S のシミュレーションを行う。"""
    ta = 0.0
    td = [0.0] * servers
    ncus = 0
    nloss = 0

    while True:
        # 次の客の到着時刻を求める
        ta += rand_exp(lam)
        if ta >= endtime:
            break

        ncus += 1

        # 到着時刻より前に利用終了しているサーバを探す
        free_server = None
        for s in range(servers):
            if td[s] < ta:
                free_server = s
                break

        if free_server is None:
            # 空いているサーバがないため、客は帰る
            nloss += 1
        else:
            # 空いているサーバに客を入れ、利用終了時刻を更新
            service_time = rand_service_time(mu, distribution)
            td[free_server] = ta + service_time

    if ncus == 0:
        raise ValueError("No customers arrived. Increase endtime.")

    return nloss / ncus, ncus, nloss


def erlang_b(servers, a):
    """アーランB式を漸化式で計算する。"""
    p = 1.0
    for s in range(1, servers + 1):
        p = a * p / (s + a * p)
    return p


def main():
    if len(sys.argv) not in (3, 4):
        print("Usage: python 3_mmss.py S endtime [figure.png]")
        sys.exit(1)

    servers = int(sys.argv[1])
    endtime = int(sys.argv[2])

    if servers <= 0:
        raise ValueError("S must be a positive integer")
    if endtime <= 0:
        raise ValueError("endtime must be a positive integer")

    # mu=1 とし、a=lambda/mu が 1 から 10 まで変化する条件で比較する
    mu = 1.0
    a_values = list(range(1, 11))

    results = {
        "M/M/S/S simulation": [],
        "Erlang B": [],
        "M/D/S/S (unit)": [],
        "M/U/S/S (uniform)": [],
        "M/P/S/S (Pareto)": [],
    }

    for a in a_values:
        lam = a * mu

        loss_mm, _, _ = simulate_mmss(
            lam, mu, servers, endtime, "M"
        )
        loss_d, _, _ = simulate_mmss(
            lam, mu, servers, endtime, "D"
        )
        loss_u, _, _ = simulate_mmss(
            lam, mu, servers, endtime, "U"
        )
        loss_p, _, _ = simulate_mmss(
            lam, mu, servers, endtime, "P"
        )

        results["M/M/S/S simulation"].append(loss_mm)
        results["Erlang B"].append(erlang_b(servers, a))
        results["M/D/S/S (unit)"].append(loss_d)
        results["M/U/S/S (uniform)"].append(loss_u)
        results["M/P/S/S (Pareto)"].append(loss_p)

    # ロス率をアーランB式と比較し、グラフにする
    fig = ScatFig()
    for name, loss_rates in results.items():
        fig.add_data(a_values, loss_rates, name)

    fig.set_xlabel("a = lambda / mu")
    fig.set_ylabel("Loss rate")
    fig.set_yscale("log")

    if len(sys.argv) == 4:
        fig_filename = sys.argv[3]
        output_dir = os.path.dirname(fig_filename)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
    else:
        output_dir = os.path.join(
            os.path.dirname(__file__), "..", "report", "figure", "03"
        )
        os.makedirs(output_dir, exist_ok=True)
        fig_filename = os.path.join(
            output_dir, f"mmss_S{servers}_t_end_{endtime}.png"
        )

    fig.save_fig(fig_filename)

    print(f"S = {servers}, endtime = {endtime}, mu = {mu}")
    print("a       M/M/S/S    Erlang B    M/D/S/S    M/U/S/S    M/P/S/S")
    for i, a in enumerate(a_values):
        print(
            f"{a:2d} "
            f"{results['M/M/S/S simulation'][i]:10.6f} "
            f"{results['Erlang B'][i]:10.6f} "
            f"{results['M/D/S/S (unit)'][i]:10.6f} "
            f"{results['M/U/S/S (uniform)'][i]:10.6f} "
            f"{results['M/P/S/S (Pareto)'][i]:10.6f}"
        )

    print(f"Figure saved: {fig_filename}")


if __name__ == "__main__":
    main()
