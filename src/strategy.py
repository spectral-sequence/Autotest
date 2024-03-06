# strategy.py
from backtesting import Strategy
from bollinger_bands import calculate_bollinger_bands

class PriceActionStrategy(Strategy):
    params = (
        ('bb_window', 20),
        ('bb_std_num', 2),
    )

    def init(self):
        self.upper_band, self.middle_band, self.lower_band = self.I(
            calculate_bollinger_bands, self.data.Close, self.params.bb_window, self.params.bb_std_num)

    def next(self):
        if not self.position and self.data.Close[-1] < self.lower_band[-1]:
            self.buy()
        elif self.position and self.data.Close[-1] > self.upper_band[-1]:
            self.position.close()