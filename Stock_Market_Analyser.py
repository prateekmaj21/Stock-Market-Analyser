import warnings
warnings.filterwarnings('ignore')  # Hide warnings
import datetime as dt
import pandas as pd
pd.core.common.is_list_like = pd.api.types.is_list_like
import pandas_datareader.data as web
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
import streamlit as st


#Importing Libraries done

#title
st.title('Stock Market App')
'---------------------------------------------------------'
#text
st.write("Developed by Prateek Majumder")

image = Image.open(os.path.join('STOCK.png'))
st.image(image)

com = st.text_input("Enter the Stock Code of company","AAPL")

'You Enterted the company code: ', com

st_date= st.text_input("Enter Starting date as YYYY-MM-DD", "2000-01-10")

'You Enterted the starting date: ', st_date

end_date= st.text_input("Enter Ending date as YYYY-MM-DD", "2000-01-20")

'You Enterted the ending date: ', end_date

df = web.DataReader(com, 'yahoo', st_date, end_date)  # Collects data
df.reset_index(inplace=True)
df.set_index("Date", inplace=True)

#title
st.title('Stock Market Data')

'The Complete Stock Data as extracted from Yahoo Finance: '
df

'1. The Stock Open Values over time: '
st.line_chart(df["Open"])

'2. The Stock Close Values over time: '
st.line_chart(df["Close"])

#title
st.title('Moving Averages')
'---------------------------------------------------------'
'Stock Data Based on Moving Averages'
'A moving average (MA) is a stock indicator that is commonly used in technical analysis.'
'The reason for calculating the moving average of a stock is to help smooth out the price data over a specified period of time by creating a constantly updated average price.'
'A simple moving average (SMA) is a calculation that takes the arithmetic mean of a given set of prices over the specific number of days in the past; for example, over the previous 15, 30, 100, or 200 days.'

mov_avg= st.text_input("Enter number of days Moving Average:", "50")

'You Enterted the Moving Average: ', mov_avg


df["mov_avg_close"] = df['Close'].rolling(window=int(mov_avg),min_periods=0).mean()

'1. Plot of Stock Closing Value for '+ mov_avg+ " Days of Moving Average"
'   Actual Closing Value also Present'
st.line_chart(df[["mov_avg_close","Close"]])

df["mov_avg_open"] = df['Open'].rolling(window=int(mov_avg),min_periods=0).mean()

'2. Plot of Stock Open Value for '+ mov_avg+ " Days of Moving Average"
'   Actual Opening Value also Present'
st.line_chart(df[["mov_avg_open","Open"]])



st.title("OHLC Candle Stick Graph")
'------------------------------------------------------------------------------------------'
'Candlestick charts are used by traders to determine possible price movement based on past patterns.'
'Candlesticks are useful when trading as they show four price points (open, close, high, and low) throughout the period of time the trader specifies.'
'Many algorithms are based on the same price information shown in candlestick charts.'
'Trading is often dictated by emotion, which can be read in candlestick charts.'

ohlc_day= st.text_input("Enter number of days for Resampling for OHLC CandleStick Chart", "50")

'You Enterted the Moving Average: ', ohlc_day

# Resample to get open-high-low-close (OHLC) on every n days of data
df_ohlc = df.Close.resample(ohlc_day+'D').ohlc() 
df_volume = df.Volume.resample(ohlc_day+'D').sum()



df_ohlc.reset_index(inplace=True)
df_ohlc.Date = df_ohlc.Date.map(mdates.date2num)



# Create and visualize candlestick charts
plt.figure(figsize=(8,6))

'OHLC Candle Stick Graph for '+ ohlc_day+ " Days"

ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
ax1.xaxis_date()
candlestick_ohlc(ax1, df_ohlc.values, width=2, colorup='g')
plt.xlabel('Time')
plt.ylabel('Stock Candle Sticks')
st.pyplot()

st.title("Note")
'------------------------------------------------------'
'All Stock data from Yahoo Finance'
'Accurately enter the stock code and date'
'Stock Prices in USD'

