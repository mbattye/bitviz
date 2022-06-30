#Bitcoin Price Ticker

# Import required libraries
import yfinance as yf
import pandas as pd
import hvplot.pandas
import panel as pn
pn.extension('plotly')
import plotly.express as px
import plotly.graph_objects as go

# Get stock data
# BTC-USD_data = yf.Ticker("BTC-USD").history(period='1d', start='2018-1-1', end='2021-6-1')
BTCGBP_data = yf.Ticker("BTC-GBP").history(period='1d', start='2018-1-1', end='2022-6-1')

# Visualize data frame top rows
# print(BTCGBP_data.head())

# Select 'Close' column only
BTCGBP = BTCGBP_data[["Close"]].copy()

# Add a daily return column
BTCGBP["Daily_Return"] = BTCGBP["Close"].pct_change()

# Add a simple moving average column of window of 10 days
BTCGBP["SMA10"] = BTCGBP["Close"].rolling(window=10).mean()

# Add a simple moving average column of window of 50 days
BTCGBP["SMA50"] = BTCGBP["Close"].rolling(window=50).mean()

# Add a simple moving average column of window of 100 days
BTCGBP["SMA100"] = BTCGBP["Close"].rolling(window=100).mean()

# Visualize data frame top rows
# print(BTCGBP.head())

# Create an hvplot table for the stock data
BTCGBP_df_table = BTCGBP.hvplot.table(width=1000)

# Create an hvplot line plot for the closing price
BTCGBP_closing_price_plot = BTCGBP.drop(columns="Daily_Return").hvplot.line(title="BTC-GBP Closing Price & Simple Moving Average", ylabel="GBP", height=500, width=1000)

# Create an hvplot line plot for the daily return
BTCGBP_daily_retrun_plot = BTCGBP["Daily_Return"].hvplot.line(title="BTC-GBP Daily Returns", ylabel="Daily Return", height=500, width=1000)

# Create an hvplot bar plot for the daily volume
BTCGBP_trading_volume_barplot = BTCGBP_data["Volume"].hvplot.bar(title="BTC-GBP Trading Volume", ylabel="Volume", height=500, width=1000).opts(alpha=0.2, xaxis=None)

# Create a candlestick plot for the stock data
BTCGBP_candlestick = go.Figure(data=[go.Candlestick(x=BTCGBP_data.index,
                    open=BTCGBP_data['Open'],
                    high=BTCGBP_data['High'],
                    low=BTCGBP_data['Low'],
                    close=BTCGBP_data['Close'])])
BTCGBP_candlestick.update_layout(height=800, width=1000, title='BTC-GBP Candlestick')

# Create a title for the dashboard
title = pn.pane.Markdown(
    """
# Bitcoin Analysis Dashboard
""",
width=1000,
)

# Create a welcome message for the dashboard
welcome = pn.pane.Markdown(
    """
This dashboard presents a visual analysis of Bitcoin price (ticker: "BTC-GBP") from January 2020 to October 2021.
You can navigate through the tabs below and interact with the plots to explore more details about the BTC price.
"""
)

# Define the ditinct tabs for the dashboard with their corresponding plots
tabs = pn.Tabs(
    ("Historical Data", pn.Column(BTCGBP_df_table)),
    ("Candlestick Plot", pn.Column(BTCGBP_candlestick)),
    ("Closing Price and Volume", pn.Column(BTCGBP_closing_price_plot, BTCGBP_trading_volume_barplot)),
    ("Daily Returns", pn.Column(BTCGBP_daily_retrun_plot)),
)

# Build dashboard
dashboard = pn.Column(pn.Column(title, welcome), tabs, width=1000)

# Visualize dashboard
dashboard.servable()