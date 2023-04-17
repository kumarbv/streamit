import yfinance as yf
import pandas as pd
import streamlit as st
import nseLibrary as nl
import datetime

# Set page title
st.set_page_config(page_title='Stock Analysis App')

# Set page header
st.header('Stock Analysis App')

with st.sidebar:
    choice = st.selectbox("Pick Nifty Stock Group", nl.returnGroupList())

# get yesterday's date
yesterday = datetime.date.today() - datetime.timedelta(days=1)
yesterday_date = yesterday.strftime('%Y-%m-%d')

# get date 1 month before yesterday's date
one_month_ago = yesterday - datetime.timedelta(days=30)
one_month_ago_date = one_month_ago.strftime('%Y-%m-%d')

# get date 1 week before yesterday's date
one_week_ago = yesterday - datetime.timedelta(days=7)
one_week_ago_date = one_week_ago.strftime('%Y-%m-%d')

# get date 3 months before yesterday's date
three_months_ago = yesterday - datetime.timedelta(days=90)
three_months_ago_date = three_months_ago.strftime('%Y-%m-%d')

# get date 1 year before yesterday's date
one_year_ago = yesterday - datetime.timedelta(days=365)
one_year_ago_date = one_year_ago.strftime('%Y-%m-%d')

# get date 3 years before yesterday's date
three_years_ago = yesterday - datetime.timedelta(days=3*365)
three_years_ago_date = three_years_ago.strftime('%Y-%m-%d')

# print the dates
print('Yesterday\'s date: ', yesterday_date)
print('Date 1 week before yesterday\'s date: ', one_week_ago_date)
print('Date 1 month before yesterday\'s date: ', one_month_ago_date)
print('Date 3 months before yesterday\'s date: ', three_months_ago_date)
print('Date 1 year before yesterday\'s date: ', one_year_ago_date)
print('Date 3 years before yesterday\'s date: ', three_years_ago_date)

# Begin and end dates
end_dates = [one_week_ago_date, one_month_ago_date, three_months_ago_date, one_year_ago_date, three_years_ago_date]

stocks = nl.getStocks(choice)
# stocks = nl.getStocksOldWay(choice)

for i in range(0,5):
    begin_date = end_dates[i];
    end_date = yesterday;
    if i == 0:
        st.write("### 1 Week Performance")
    elif i == 1:
        st.write("### 1 Month Performance")
    elif i == 2:
        st.write("### 3 Month Performance")
    elif i == 3:
        st.write("### 1 Year Performance")
    else:
        st.write("### 3 Year Performance")
    data = yf.download(stocks, start=begin_date, end=end_date)['Adj Close']

    # Calculate the returns for each stock
    beginning_prices = data.iloc[0]
    end_prices = data.iloc[-1]
    returns = ((end_prices - beginning_prices) / beginning_prices) * 100

    # Split the returns into gainers and losers
    gainers = returns.sort_values(ascending=False).head(5)
    # losers = returns.sort_values().head(5)[::-1]  # Reverse the order of the losers
    losers = returns.sort_values().head(5)  # Reverse the order of the losers - [::-1] removed
    # Create DataFrames for the gainers and losers
    gainer_df = pd.DataFrame({'Stock': gainers.index, 'Return': gainers.values})
    loser_df = pd.DataFrame({'Stock': losers.index, 'Return': losers.values})

    # Print the results
    col1, col2 = st.columns(2)
    with col1:
        st.write('### Top Gainers:')
        st.bar_chart(gainer_df.set_index('Stock'))
        # st.dataframe(gainer_df)
    with col2:
        st.write('### Top Losers:')
        # st.dataframe(loser_df)
        st.bar_chart(loser_df.set_index('Stock'))
