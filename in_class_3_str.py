import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick # optional may be helpful for plotting percentage
import numpy as np
import pandas as pd
import seaborn as sb # optional to set plot theme
sb.set_theme() # optional to set plot theme
import yfinance as yf

DEFAULT_START = dt.date.isoformat(dt.date.today() - dt.timedelta(365))
DEFAULT_END = dt.date.isoformat(dt.date.today())

class Stock:
    def __init__(self, symbol, start=DEFAULT_START, end=DEFAULT_END):
        self.symbol = symbol
        self.start = start
        self.end = end
        self.data = self.get_data()


    def get_data(self):
        """method that downloads data and stores in a DataFrame
           uncomment the code below wich should be the final two lines 
           of your method"""
        data = yf.download(self.symbol, start=self.start, end=self.end) #download historical price data based on user defined stock symbol and starting date and end date in ISO format
       # print (type(data)) #stored in a pandas DataFrame - <class 'pandas.core.frame.DataFrame'>
        data.reset_index(inplace=True) #because date is acting as key right now
        data['Date'] = pd.to_datetime(data['Date']) #converted to a pandas Datetime object
        #print (data.head())
        data.set_index('Date', inplace=True) #index should be set to the date
        self.calc_returns(data)
        self.data = data
        #return data
        #pass

    
    def calc_returns(self, df):
        """method that adds change and return columns to data"""
        df['change column'] = df['Close'].diff() #difference between the close to close price relative to the previous day’s close
        df['instant_return'] = np.log(df['Close']).diff().round(4) #daily instantaneous rate of return
        #print (df.head())
        self.plot_return_dist(df)
        self.plot_performance(df)
        #pass

    
    def plot_return_dist(self,df):
        """method that plots instantaneous returns as histogram"""
        plt.figure(figsize=(12, 8))
        sb.histplot(df['instant_return'].dropna(), bins=100, kde=True) #kde - adds line
        plt.xlabel(f"Instantaneous Returns for {self.symbol}")
        plt.ylabel("Freq")
        plt.show()
        #print("No data fetched")
        #pass


    def plot_performance(self,df):
        """method that plots stock object performance as percent """
        plt.figure(figsize=(12, 8))
        ((df['Close'] / df['Close'].iloc[0]) - 1).plot() # prepared the trend of closing value over the period in percentage change
        plt.title(f'Stock Performance for {self.symbol}')
        plt.xlabel('Date')
        plt.ylabel('% Change')
        plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1.0)) #converted y axis to percentages
        plt.show()
        #pass
                  



def main():
    # uncomment (remove pass) code below to test
     test = Stock(symbol='AAPL') # optionally test custom data range
     print(test.data)
     #test.plot_performance()
     #test.plot_return_dist()
    #pass

if __name__ == '__main__':
    main() 