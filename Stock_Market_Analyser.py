import warnings
warnings.filterwarnings('ignore')  # Hide warnings
# Import necessary libraries for Prophet
from prophet import Prophet
import datetime as dt
import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from PIL import Image
import os
import streamlit as st

import mplfinance as mpf
import matplotlib.dates as mdates

# Importing Libraries done

# Title
st.title('Stock Market App')
'---------------------------------------------------------'
# Text
st.write("Developed by Prateek Majumder")

image = Image.open('STOCK.png')
st.image(image)


st.write("period accepts values like '1d', '5d', '1wk', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', and 'max'.")
com = st.text_input("Enter the Stock Code of company", "TCS")
'You Entered the company code: ', com

per = st.text_input("Enter The stock data history period:", "1mo")
'You Entered the Period: ', per

# Fetch data using yfinance
df = yf.download(com, period=str(per))

# Flatten the multi-index into single-level columns
df.columns = df.columns.droplevel(1)

# Reset index and set date as index
df.reset_index(inplace=True)
df.set_index("Date", inplace=True)  # Ensure DatetimeIndex is set

# Assuming the 'Date' column is in the index
st_date = df.index.min()
end_date = df.index.max()

# Print the start and end dates
st.write(f"Start Date: {start_date}")
st.write(f"End Date: {end_date}")

# Title
st.title('Stock Market Data')

'The Complete Stock Data as extracted from Yahoo Finance: '
st.write(df)

'1. The Stock Open Values over time: '
st.line_chart(df["Open"])

'2. The Stock Close Values over time: '
st.line_chart(df["Close"])

# Title
st.title('Moving Averages')
'---------------------------------------------------------'
'Stock Data Based on Moving Averages'
'A moving average (MA) is a stock indicator that is commonly used in technical analysis.'
'The reason for calculating the moving average of a stock is to help smooth out the price data over a specified period of time by creating a constantly updated average price.'
'A simple moving average (SMA) is a calculation that takes the arithmetic mean of a given set of prices over the specific number of days in the past; for example, over the previous 15, 30, 100, or 200 days.'

mov_avg = st.text_input("Enter number of days Moving Average:", "5")
'You Entered the Moving Average: ', mov_avg

df["mov_avg_close"] = df['Close'].rolling(window=int(mov_avg), min_periods=0).mean()
st.write(df)
'1. Plot of Stock Closing Value for ' + mov_avg + " Days of Moving Average"
' Actual Closing Value also Present'
required_columns = ["mov_avg_close", "Close"]
if not all(col in df.columns for col in required_columns):
    st.error("Missing required columns in the DataFrame: 'mov_avg_close' or 'Close'.")
else:
    st.line_chart(df[required_columns])


df["mov_avg_open"] = df['Open'].rolling(window=int(mov_avg), min_periods=0).mean()

'2. Plot of Stock Open Value for ' + mov_avg + " Days of Moving Average"
' Actual Opening Value also Present'
st.line_chart(df[["mov_avg_open", "Open"]])

# OHLC Candlestick Graph
st.title("OHLC Candlestick Graph")
'------------------------------------------------------------------------------------------'
'Candlestick charts are used by traders to determine possible price movement based on past patterns.'
'Candlesticks are useful when trading as they show four price points (open, close, high, and low) throughout the period of time the trader specifies.'
'Many algorithms are based on the same price information shown in candlestick charts.'
'Trading is often dictated by emotion, which can be read in candlestick charts.'

ohlc_day = st.text_input("Enter number of days for Resampling for OHLC Candlestick Chart", "5")
'You Entered the number of days for resampling: ', ohlc_day

# Resample to get open-high-low-close (OHLC) on every n days of data
df_ohlc = df.resample(ohlc_day + 'D').agg({'Open': 'first',
                                           'High': 'max',
                                           'Low': 'min',
                                           'Close': 'last',
                                           'Volume': 'sum'})

df_ohlc.dropna(inplace=True)

# Create and visualize candlestick charts
plt.figure(figsize=(8, 6))
mpf.plot(df_ohlc, type='candle', style='charles', volume=True)
plt.xlabel('Time')
plt.ylabel('Stock Candlesticks')
st.pyplot()





# Basic Statistics
st.title('Basic Statistics')
'---------------------------------------------------------'
'Calculating some statistical data like percentile, mean and std of the numerical values.'
st.write("Summary Statistics of Stock Prices")
st.write(df.describe())

# Correlation Matrix
st.title('Correlation Matrix')
'---------------------------------------------------------'
'Displays a heatmap of the correlation between different stock price metrics.'
corr_matrix = df.corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
st.pyplot()

# Bollinger Bands
st.title('Bollinger Bands')
'---------------------------------------------------------'
'Visualizes Bollinger Bands for the stock, which are used to measure price volatility.'
bollinger_window = st.text_input("Enter number of days for Bollinger Bands:", "20")
'You Entered the Bollinger Bands Window: ', bollinger_window

df['MA20'] = df['Close'].rolling(window=int(bollinger_window)).mean()
df['BB_upper'] = df['MA20'] + 2*df['Close'].rolling(window=int(bollinger_window)).std()
df['BB_lower'] = df['MA20'] - 2*df['Close'].rolling(window=int(bollinger_window)).std()

st.line_chart(df[['Close', 'BB_upper', 'BB_lower']])

# Volume Analysis
st.title('Volume Analysis')
'---------------------------------------------------------'
'Shows the trading volume over time.'

st.line_chart(df['Volume'])

# RSI Calculation
st.title('Relative Strength Index (RSI)')
'---------------------------------------------------------'
'Displays the RSI indicator to assess overbought or oversold conditions.'

rsi_window = st.text_input("Enter number of days for RSI Calculation:", "14")
'You Entered the RSI Window: ', rsi_window

delta = df['Close'].diff()
gain = (delta.where(delta > 0, 0)).rolling(window=int(rsi_window)).mean()
loss = (-delta.where(delta < 0, 0)).rolling(window=int(rsi_window)).mean()

rs = gain / loss
df['RSI'] = 100 - (100 / (1 + rs))

st.line_chart(df['RSI'])

# MACD Calculation
st.title('MACD (Moving Average Convergence Divergence)')
'---------------------------------------------------------'
'Visualizes MACD and Signal Line for identifying potential buy or sell signals.'

df['EMA12'] = df['Close'].ewm(span=12, adjust=False).mean()
df['EMA26'] = df['Close'].ewm(span=26, adjust=False).mean()
df['MACD'] = df['EMA12'] - df['EMA26']
df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()

st.line_chart(df[['MACD', 'Signal_Line']])

# Return Analysis
st.title('Return Analysis')
'---------------------------------------------------------'
'Analyzes daily returns and cumulative returns.'

df['Daily_Return'] = df['Close'].pct_change()
df['Cumulative_Return'] = (1 + df['Daily_Return']).cumprod()

st.line_chart(df['Daily_Return'])
st.line_chart(df['Cumulative_Return'])

# Risk Metrics
st.title('Risk Metrics')
'---------------------------------------------------------'
'Calculations of the Sharpe Ratio and Beta for risk assessment.'


st.write("Sharpe Ratio:")
risk_free_rate = 0.01
sharpe_ratio = (df['Daily_Return'].mean() - risk_free_rate) / df['Daily_Return'].std()
st.write(sharpe_ratio)

st.write("Beta:")
market_data = yf.download('^GSPC', start=st_date, end=end_date)
market_data['Market_Return'] = market_data['Close'].pct_change()
covariance = df['Daily_Return'].cov(market_data['Market_Return'])
beta = covariance / market_data['Market_Return'].var()
st.write(beta)


# Stock Prediction using Prophet
st.title('Stock Price Prediction using Prophet')

prediction_days = st.text_input("Enter number of days to predict:",'15')
prediction_days = int(prediction_days)
# Filter data for training
train_df = df.loc[st_date:end_date].reset_index()

# Prophet expects two columns: ds (date) and y (value)
train_df = train_df[['Date', 'Close']].rename(columns={'Date': 'ds', 'Close': 'y'})

# Initialize and fit the Prophet model
model = Prophet()
model.fit(train_df)

# Create a dataframe to hold future dates for prediction
future = model.make_future_dataframe(periods=prediction_days, freq='B')

# Make predictions
forecast = model.predict(future)

# Show the predicted data
st.write('Forecast Data:')
st.write(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']])

# Plot the predictions
st.write("Forecast Plot:")
fig1 = model.plot(forecast)
st.pyplot(fig1)


# Show forecast components
st.write("Forecast Components:")
fig2 = model.plot_components(forecast)
st.pyplot(fig2)


# Plot only trend
st.write("Stock Price Trend:")
fig_trend, ax_trend = plt.subplots(figsize=(10, 6))
ax_trend.plot(forecast['ds'], forecast['trend'], label="Trend")
ax_trend.set_title('Stock Price Trend')
ax_trend.set_xlabel('Date')
ax_trend.set_ylabel('Price')
ax_trend.legend()
st.pyplot(fig_trend)


st.title("Note")
'------------------------------------------------------'
'All Stock data from Yahoo Finance'
'Accurately enter the stock code and date'
'Stock Prices in USD'
