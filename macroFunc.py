import pandas as pd
import numpy as np
import datetime as time
import math
import os
from eod import EodHistoricalData
import json
import requests
import matplotlib.pyplot as plt
import matplotlib.ticker as matTick 


#set date to 365 days ago
d8 = time.date.today() - time.timedelta(365)
todayDate = time.date.today()

#pulls stock data from api using users key and prefered exhange
def getStockData(key, exchange ='NYSE'):
    #gets stock data from eod api
    """ 
    args are key = api key, exhange = what stock exchange for data
    code returns dataframe
    """
    endPt = f"https://eodhd.com/api/exchange-symbol-list/{exchange}?api_token={key}&fmt=json"
    print ("download data")
    response = requests.get(endPt)
    #check to see if requests works
    if response.status_code != 200:
        print(f"error: cant get data (Status code: {response.status_code})")
        return None
    #convert json to df
    try:
        exData = pd.DataFrame(json.loads(response.text))
        print("complete download")
        return exData
    except json.JSONDecodeError as noWork:
        print(f"error(Error: {noWork})")
        print("response content:", response.text)

#func to get data based on ticker & save to csv file
def getData(key, *ticker, path = 'data_files', date = d8):
    """
    args
    key=api key
    *ticker = list of stock tickers you want
    path = path where csv files saved
    date = date from when u want data

    """
    #if path doesnt exist it creates directory
    base_directory = '/Users/ethanmypan/stockTrade'
    fullPath = os.path.join(base_directory, path)
    print(f"directory at: {fullPath}")
    if not os.path.exists(fullPath):
        try:
            os.makedirs(fullPath)
            print(f"directory '{fullPath} is created")
        except Exception as e:
            print(f"failed to make full path '{fullPath}':{e} ")
            return
    
    skipTick = 0
    skipTickArr = []
    downloadDone = 0
    #intializes the eod with your api
    client = EodHistoricalData(key)
    for i in ticker:
        try:
            print(f"download {i}")
            df = pd.DataFrame(client.get_prices_eod(i, from_= date))
            df.index = pd.DatetimeIndex(df.date)
            df.drop(columns=['date'], inplace=True)
            df.to_csv(f"{fullPath}/{i}.csv")
            downloadDone += 1
        except Exception as e:
            print(f"{i} not found, error: {e} ")
            skipTick +=1
            skipTickArr.append(i)
   #updates
    print("download done")
    print(f"data download for {downloadDone} sec")
    print(f"{skipTick} tickers skipped")

    if skipTickArr:
        print("Tickers skipped".center(30, "="))
        for i in skipTickArr:
            print(i)
#func to get sp500 stocks based on sector
def getSP500(stockCode = True, sector = False):
    sp = pd.read_csv('/Users/ethanmypan/stockTrade/flat-ui__data-Sat Sep 14 2024.csv')
    if sector:
        sp = sp[sp['GICS Sector'] == sector]
    if stockCode:
        return sp ['Symbol'].to_list()
    else:
        return sp

def getCLP(folder = 'data_files', adjustedCLP = False):
    files = [file for file in os.listdir(folder) if not file.startswith('0') and file.endswith('.csv')]
    if not files:
        print(f"No csv files dound")
        return None
    closes = pd.DataFrame()
    print(f"df found")
    for file in files:
        filePath = os.path.join(folder, file)
        print(f"proccesing file{filePath}")
        try:
            if adjustedCLP:
                df = pd.DataFrame(pd.read_csv(filePath, index_col= 'date')['adjusted_close'])
                df.rename(columns={'adjusted_close': file[:-4]}, inplace=True)
            else:
                df = pd.DataFrame(pd.read_csv(filePath, index_col= 'date')['close'])
                df.rename(columns={'close': file[:-4]}, inplace=True)
            print(f"data is loaded")
            if closes.empty:
                closes = df
            else: 
                closes = pd.concat([closes, df], axis =1, join='outer')
        except KeyError as e:
            print(f"missing expected column")
        except FileNotFoundError as e:
            print(f"missing expected file")
        except Exception as e:
            print(f"error")
    print(f"final combined df")
    if not closes.empty:
        outPath = os.path.join(folder, 'closes.csv')    
        print(f"saving data to {outPath}")    
        closes.to_csv(outPath)
    else:
        print("no data saved")
    return closes


def performanceGraph(folder):
    files = [file for file in os.listdir(folder) if not file.startswith('0')]
    fig, ax = plt.subplots(math.ceil(len(files) / 4), 4, figsize =(16,16))
    cnt = 0
    for row in range(math.ceil(len(files)/ 4)):
        for col in range(4):
            try:
                data = pd.read_csv(f"{folder}/{files[cnt]}")['close']
                data = (data/data[0] - 1)*100
                ax[row, col].plot(data, label=files[cnt][:-4])
                ax[row, col].legend()
                ax[row, col].yaxis.set_major_formatter(matTick.PercentFormatter())
                ax[row, col].axhline(0, c ='r', ls ='--')
            except:
                pass
            cnt += 1
    plt.show()
#func to get stock based on type
def getFinType(exData, type = "Common Stock"):
     stockCode = exData[exData.Type == type]
     return stockCode.Code.to_list()
def returnClosingPrice(folder, fileName):
    try:
        date = pd.read_csv(f"{folder}/{fileName}", index_col=['date'])


    except Exception as e:
        print(f"error: {e}")
    return np.log(date).diff().dropna()
def getCorrelation(data):
    return data.corr()
def correlationGraph(stockClose, relative=False):
    if stockClose.endswith('.csv'):
        stockClose = pd.read_csv(stockClose, index_col=['date'])
    else:
        stockClose = pd.read_excel(stockClose, index_col=['date'])
    if relative:
        change = stockClose/ stockClose.iloc[0] - 1
        change.plot()
        plt.axhline(0, c ='r', ls = '--')
        plt.grid(axis ='y')
        plt.show()
    else:
        stockClose.plot()
        plt.grid(axis='y')
        plt.show()
def getDividend(key, exchange='US', date = time.date.today()):
    client = EodHistoricalData(key)
    data = pd.DataFrame(client.get_bulk_markets(exchange=exchange, date=date,type_='dividends'))
    return data
def getReportedEarning(key):
    client = EodHistoricalData(key)
    earningDF = pd.DataFrame(client.get_calendar_earnings())
    symbols = []

    for row in range(len(earningDF)):
        if earningDF.earnings.iloc[row]['code'].endswith('US'):
            symbols.append(earningDF.earnings[row]['code'][:-3])
    print("There are {len(symbols)} companies reporting stock prices this week")
    return symbols

def getReturnData(*ticker, date=d8, adjustedCLP=False, key):
    client = EodHistoricalData(key)
    tempDF = pd.DataFrame()
    for i in ticker:
        try:
            if adjustedCLP:
                tempDF[i] = pd.DataFrame(client.get_prices_eod(i, from_=date))['adjusted_close']
            else:
                tempDF[i] =  pd.DataFrame(client.get_prices_eod(i, from_=date))['close']
        except Exception as e:
            print(f"{i} error: {e}")
    data = tempDF
    currData = np.log(data).diff().dropna()
    dataPCT = data.pct_change()

    with pd.ExcelWriter('returns.xlsx', date_format='yyyy-mm-dd') as writer:
        data.to_excel(writer, sheet_name='closes')
        currData.to_excel(writer, sheet_name='returns')
        dataPCT.to_excel(writer, sheet_name='pct change')
    print(f"data retrieved")
    return data, currData, dataPCT
def stockScreener(symbols, key):
    high = {}
    
    apiCall = f"https://eodhistoricaldata.com/eod-bulk-last-day/US?api_token={key}&fmt=json"
    data = pd.DataFrame(requests.get(apiCall).json())
    data.reset_index(drop=True)
    client = EodHistoricalData(key)
    for ticker in symbols:
        try:
            high[ticker] = client.get_fundamental_equity(f"{ticker}.US")['Technicals']['52WeekHigh']
            print(f"getting {ticker}")
        except:
            print(f"{ticker}not available")
    mask = data.code.isin(symbols)
    prices = data[['code','close']][mask]
    high = pd.Series(high, name='high')
    prices=prices.merge(high, right_on=high.index, left_on='code')
    prices['ratio']=prices['close'] / prices['high']
    return prices


def main():
    key = open('/Users/ethanmypan/stockTrade/notApiKey.txt').read().strip()
    #tickers = "AAPL AMZN GOOG NVDA".split()
   # returns = getReturnData(*tickers, key = key)
   # print(returns[0])
    #performanceGraph('energy')
    #print(getReportedEarning(key))
   # print(getDividend(key))
   # data = getStockData(key)
    #if data is not None:
        #print("Stock Data:")
        #print(data)
        #print(data.columns)
    sp = getSP500()[:10]
    print(stockScreener(sp, key))


        #commonStockCode = getFinType(data, type = "Common Stock")
        #print(commonStockCode)
       # sp500CodesEnergy = getSP500(stockCode=True, sector= 'Energy')
       # print(sp500Codes)
       # getData(key, "AAPL","GOOG", path='mine')
       # getCLP(folder='mine', adjustedCLP=False)
        #print(returnClosingPrice('mine', 'closes.csv'))
        #print(getCorrelation(returnClosingPrice('mine', 'closes.csv')))
        #correlationGraph(stockClose='mine/closes.csv', relative=True)



if __name__ == '__main__':
    main()