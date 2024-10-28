from eod import EodHistoricalData
import numpy as np
import os
import pandas as pd
import seaborn as sb
import datetime as time
import matplotlib.pyplot as plt
import matplotlib.ticker as mTick
sb.set_theme()
defDate = time.date.isoformat(time.date.today() -time.timedelta(365))


class stock:
    def __init__(self, symbol, key, date=defDate, folder=None):
        self.symbol = symbol
        self.key = key
        self.date = date
        self.folder = folder
        self.data = self.getData()

    

    def getData(self):
        tempData = [filename[:-4] 
        for filename in os.listdir(self.folder) if not filename.startswith('0')]
        if self.symbol in tempData:
            data = pd.read_csv(f"{self.folder}/{self.symbol}.csv", index_col='date').round(2)
        else:
            client = EodHistoricalData(self.key)
            data = pd.DataFrame(client.get_prices_eod(self.symbol,from_=self.date)).round(2)
            data.index=pd.DatetimeIndex(data.date).date
            #data.index= pd.DatetimeIndex(data['date'])
            data.drop(columns=['date'], inplace=True)
            self.dataVolatility(data)
        return data
    
    def dataVolatility(self, df):
        df['returns'] = np.log(df.close).diff().round(4)
        df['volatility'] = df.returns.rolling(21).std().round(4)
        df['change'] = df['close'].diff()
        df['hi_low_spread'] = ((df['high'] - df['low']) / df['open']).round(2)
        df['expChange'] = (df.volatility * df.close.shift(1)).round(2)
        df['magnitude'] = (df.change / df.expChange).round(2)
        df['absMagnitude'] = np.abs(df.magnitude)
        df.dropna(inplace=True)
    def plotReturnDist(self):
        start = self.data.index[0]
        end = self.data.index[-1]
        plt.hist(self.data['returns'], bins=20,edgecolor = 'w')
        plt.suptitle(f"Dist of returns for {self.symbol}", fontsize =14)
        plt.title(f"from{start} to {end}", fontsize=12)
        plt.show()
    def volatilityPlot(self):
        start = self.data.index[0]
        end = self.data.index[-1]
        plt.scatter(self.data['returns'], self.data['absMagnitude'])
        plt.axhline(0,c='r', ls='--')
        plt.axvline(0,c='r', ls='--')
        plt.suptitle(f"volatility of returns for {self.symbol}", fontsize =14)
        plt.title(f"from{start} to {end}", fontsize=12)
        plt.show()
def main():
    apiKey = open('YourApiKeyPath').read().strip()
    test = stock(symbol='AAPL', key= apiKey)
    #print(test.data)
   # test.plotReturnDist()
    test.volatilityPlot()

if __name__ == '__main__':
    main()