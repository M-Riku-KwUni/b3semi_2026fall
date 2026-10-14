import math
import matplotlib.pyplot as plt


class ScatFig:

    '''
    散布図を作成するクラス

    Attribute
    ----------
    _fig : 散布図のオブジェクト
    _axes : 軸オブジェクト

    _n_data (int) : 散布図に描画するデータ数
    _draw_line (bool) : 線を描画するかどうか(デフォルト: 線を描画)

    '''
    def __init__(self):

        # figure オブジェクトの取得
        self._fig, self._axes = plt.subplots(1, 1, tight_layout = True)

        self._n_data = 0
        self.with_line()

    def add_data(self, x_data: list[float], y_data: list[float], name: str = "") :
        # 図にデータを追加

        # # marker の生成
        marker = "-" if self._draw_line else ""

        symbols = ['o', 'x', '*', 'v', '^']
        kind_symbol = self._n_data % len(symbols)

        marker += symbols[kind_symbol]

        # # オブジェクトにデータを追加
        self._axes.plot(x_data, y_data, marker,  label = name, clip_on=False)

        self._n_data += 1

    def set_xlabel(self, x_label: str):
        # x 軸のラベルを設定
        self._axes.set_xlabel(x_label)

    def set_ylabel(self, y_label: str):
        # y 軸のラベルを設定
        self._axes.set_ylabel(y_label)

    def set_xscale(self, scale: str = 'linear'):
        # x 軸のスケール(linear/log)を設定
        self._axes.set_xscale(scale)

    def set_yscale(self, scale: str = 'linear'):
        # y 軸のスケール(linear/log)を設定
        self._axes.set_yscale(scale)

    def without_line(self):
        # 線を描画しない
        self._draw_line = False

    def with_line(self):
        # 線を描画する
        self._draw_line = True

    def set_xlim(self, x_min: float, x_max: float):
        # x 軸の範囲を設定
        self._axes.set_xlim(x_min, x_max)

    def set_ylim(self, y_min: float, y_max: float):
        # y 軸の範囲を設定
        self._axes.set_ylim(y_min, y_max)

    def save_fig(self, fig_filename: str):
        # 図を保存
        self._axes.legend()
        self._fig.savefig(fig_filename)


def main():
    # 描画するデータの生成
    x_min = 1
    x_max = 100

    x = [i for i in range(x_min, x_max+1) ]
    y1 = [i for i in range(x_min, x_max+1)]                   # y1 = x
    y2 = [i*i for i in range(x_min, x_max+1)]                 # y2 = x^2
    y3 = [math.exp(i/10) for i in range(x_min, x_max+1)]      # y3 = exp(x/10)

    fig = ScatFig()  # 散布図のオブジェクト作成

    # 図にデータを追加
    fig.add_data(x, y1, 'linear')
    fig.add_data(x, y2, 'square')
    fig.add_data(x, y3, 'exponential')

    # 図を設定
    fig.set_xlim(x_min, x_max)
    fig.set_xlabel('$x$')                                           # x 軸のラベルを描画
    fig.set_ylabel('$y_1 = x$ or $y_2 = x^2$ or $y_3 = e^{x/10}$')  # y 軸のラベルを描画

    fig.set_xscale('log')        # x 軸を対数目盛に変更
    fig.set_yscale('log')        # y 軸を対数目盛に変更

    # 図を保存
    fig.save_fig('../report/figure/sample.png')


if __name__ == '__main__':
    main()
