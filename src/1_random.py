import sys
import random
import math
import os

from scatfig import ScatFig


def rand_exp(lam):
    u = random.random()
    x = -math.log(1 - u) / lam

    return x


def rand_uni(a, b):
    u = random.random()
    x = (b - a) * u + a

    return x


def rand_par(x0, alpha):
    u = random.random()
    x = x0 * (1 - u) ** (-1 / alpha)

    return x


def main():

    if len(sys.argv) != 3:
        print("Usage: python rand.py N kind")
        return

    N = int(sys.argv[1])
    kind = sys.argv[2]

    lam = 0.5
    a = 3
    b = 7
    x0 = 1
    alpha = 2

    rnd_list = [0.0] * N

    for i in range(N):
        if kind == "exp":
            rnd = rand_exp(lam)
        elif kind == "uni":
            rnd = rand_uni(a, b)
        elif kind == "par":
            rnd = rand_par(x0, alpha)

        print(rnd)
        rnd_list[i] = rnd

    x_data = [0.0] * N
    y_data = [0.0] * N

    for i, xi in enumerate(sorted(rnd_list)):
        x_data[i] = xi
        y_data[i] = 1 - i / N

    fig = ScatFig()
    fig.add_data(x_data, y_data, kind)
    fig.set_xlabel("x")
    fig.set_ylabel("CCDF")
    
    if kind == "exp":
        fig.set_yscale("log")
    elif kind == "par":
        fig.set_xscale("log")
        fig.set_yscale("log")
    

    output_dir = "../report/figure/01"
    os.makedirs(output_dir, exist_ok=True)

    fig.save_fig(os.path.join(output_dir, kind + ".png"))


if __name__ == "__main__":
    main()