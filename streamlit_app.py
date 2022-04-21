import streamlit as st
import pandas as pd
import altair as alt
from pandas_datareader import data

energy_source = pd.DataFrame({
    "EnergyType": ["Electricity", "Gasoline", "Natural Gas", "Electricity", "Gasoline", "Natural Gas", "Electricity", "Gasoline", "Natural Gas"],
    "Price ($)":  [150, 100, 30, 130, 80, 70, 170, 83, 70],
    "Date": ["2022-1-23", "2022-1-30", "2022-1-5", "2022-2-21", "2022-2-1", "2022-2-1", "2022-3-1", "2022-3-1", "2022-3-1"]
})

altair_custom_axis_labels = 'Altair with Custom Axis Labels'
simple_line_chart = 'Altair Simple Line Chart'
complex_line_chart = 'Altair Complex Line Chart'
line_chart_title = 'Altair Line Chart Title'


option = st.selectbox('Streamlit Line Chart Tutorial', (complex_line_chart,simple_line_chart, altair_custom_axis_labels,line_chart_title))

def get_stock_df(symbol,start,end):
   source = 'yahoo'
   df = data.DataReader(
      symbol, start=start, end=end, data_source=source
   )
   return df

def get_stock_combined(symbols,start,end):
   dfs = []
   for symbol in symbols.keys():
      df = get_stock_df(symbol,start,end)
      df['Symbol'] = symbol
      df['SymbolFullName'] = symbols[symbol]
      dfs.append(df)
   df_combined = pd.concat(dfs, axis=0)
   df_combined['date'] = df_combined.index.values
   return df_combined


def get_stock_title(stocks):
   title = ""
   idx = 0
   
   for i in stocks.keys():
      title = title + stocks[i] 
  
      if idx <=  len(stocks.keys()) - 1: 
         title = title + " & "
      idx = idx + 1
      
   return title


if option == altair_custom_axis_labels:
    line_chart = alt.Chart(energy_source).mark_line().encode(
        y=  alt.Y('Price ($)', title='Close Price($)'),
        x=  alt.X( 'month(Date)', title='Month')
    ).configure_axis(
        titleFontSize=14,
        labelFontSize=12
    )
    st.altair_chart(line_chart, use_container_width=True)
elif option == simple_line_chart:
   line_chart = alt.Chart(energy_source).mark_line().encode(
        y='Price ($)',
        x='month(Date)'
    )
   st.altair_chart(line_chart, use_container_width=True)
elif option == line_chart_title:
 
    line_chart = alt.Chart(energy_source).mark_line().encode(
        y=  alt.Y('Price ($)', title='Close Price($)'),
        x=  alt.X( 'month(Date)', title='Month')
    ).properties(
        height=400, width=700,
        title="Energy Bill"
    ).configure_title(
        fontSize=16
    )
    st.altair_chart(line_chart, use_container_width=True)

    
   
elif option == complex_line_chart:
    stocks = {"LIT":"Lithium","USO":"United States Oil ETF","UNG":"Natural Gas Fund","USL":"US 12 Month Natural Gas Fund (UNL)"}      
    stock_title = get_stock_title(stocks)
    start = '2021-06-01'
    end = '2022-08-01'

    df_combined = get_stock_combined(stocks,start,end)
    base = alt.Chart(df_combined)

    line = base.mark_line().encode(
        alt.X("date", title="Date"),
        alt.Y("Close", title="Closing Price", scale=alt.Scale(zero=False)),
        color='SymbolFullName'
    ).properties(
        height=400, width=700,
        title=stock_title
    ).configure_title(
        fontSize=12
    ).configure_axis(
        titleFontSize=14,
        labelFontSize=12
    )
    line 


#print(line_chart.to_json()