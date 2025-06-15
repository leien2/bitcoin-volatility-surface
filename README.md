# Bitcoin Volatility Analysis

[![Live Demo](https://img.shields.io/badge/Interactive 3D Demo - Click to Experience-00b4ff?style=for-the-badge&logo=webgl)](https://leien2.github.io/bitcoin-volatility-surface/)



## Project Introduction

The core objective of this project is to establish an automated volatility analysis tool for the Bitcoin options market, providing data support for formulating options trading strategies. It primarily addresses two challenges: first, efficiently and accurately calculating implied volatility from massive heterogeneous data (data processing efficiency); second, interpreting and utilizing the generated volatility surface to aid trading decisions and risk management (trading application value).



1. Get the data from deribit exchange through data_fetcher.py

2. After data cleaning, calculate IV, DTE, and strike price through analyze_options.py

3. plot_vol_surface.py draws the volatility surface



## File Structure

- **Real-time Market Data Acquisition**: Automatically retrieve the latest BTC options market data via the Deribit API
- **Data Cleaning and Structuring**: Convert raw JSON data into structured CSV format for analytical processing
- **Option Parameter Extraction**: Automatically parse key parameters (expiration date, strike price, etc.) from option names
- **Implied Volatility Calculation**: Extract implied volatility information using market prices of options
- **Volatility Surface Construction**: Utilize 3D visualization to intuitively display volatility structures across strike prices and expirations
- **Volatility Anomaly Identification**: Rapidly detect market characteristics such as volatility skew and smile