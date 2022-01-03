from pandas.core import groupby
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import plotly
import plotly.express as px
import openpyxl
from scipy import stats
import numpy as np


pd.set_option('display.max_columns', None)

hg = sns.light_palette('green', as_cmap=True)

def app():
    df = pd.read_excel('combineddata/FlipCombined.xlsx',  engine='openpyxl')
    df = df.sort_values(by='Date', ascending=False)
    df['Date'] = pd.to_datetime(df['Date']).dt.date


    # ALL TIME REVENUE
    def checkOut_total_revenue(store_name):
        df_curr = df[df['Store Name'] == store_name]
        z = np.abs(stats.zscore(df_curr['Net Revenue']))
        res = np.where(z > 3)
      
        for x in res:
          #    return df_curr.iloc[x,:]
             df_curr.drop(df_curr.iloc[x,:].index, inplace=True)
        
        z2 = np.abs(stats.zscore(df_curr['Net Revenue']))
        res2 = np.where(z2 > 2)

        for x in res2:
          outliers =  df_curr.iloc[x,:]
          return pd.DataFrame(outliers)
    
    # 30 DAYS REVENUE
    def checkOut_total_revenue_last30(store_name):
        
        df_curr = df[df['Store Name'] == store_name]
        df_curr = df_curr.head(30)
        df_curr = df_curr[-30:]
        z = np.abs(stats.zscore(df_curr['Net Revenue']))
        res = np.where(z > 1.8)

        for x in res:
          outliers =  df_curr.iloc[x,:]
          return pd.DataFrame(outliers)

    # 7 DAYS REVENUE
    def checkOut_last7(store_name, plat):
        df_curr = df[df['Store Name'] == store_name]
        df_curr = df_curr.head(7)
        df_curr = df_curr[-30:]
        z = np.abs(stats.zscore(df_curr[plat]))
        res = np.where(z > 1.5)

        for x in res:
          outliers =  df_curr.iloc[x,:]
          return pd.DataFrame(outliers)

     # ALL STORES 7 DAYS REVENUE
    # def checkOut_last7_all(plat):

    #     df.head(7)
    #     z = np.abs(stats.zscore(df[plat]))
    #     res = np.where(z > 1.5)

    #     for x in res:
    #       outliers =  df.iloc[x,:]
    #       return pd.DataFrame(outliers)

    

     # #select stores
    stores = df['Store Name'].unique()
    store_select = st.sidebar.selectbox( "Select Stores", stores)


    # OUTPUT
    st.title('7 Days Average')
    dfjl = df.head(7)
    dfjl = df[df['Store Name'] == store_select]
    dfjl = dfjl.groupby('Store Name')[['Net Revenue', 'Online Revenue','In-Store Revenue', 'Eleme','Meituan' ]].mean()
    st.write(dfjl.style.format("{:,.0f}"))

    # st.title('ALL Stores Last 7 Days Outliers')
    # st.subheader('Total Revenue')
    # week = checkOut_last7_all('Net Revenue')
    # st.write(week[['Date', 'Store Name', 'Net Revenue', 'Online Revenue','In-Store Revenue', 'Eleme','Meituan']].style.set_precision(0))

    st.title('Last 7 Days Outliers')
    st.subheader('Total Revenue')
    week = checkOut_last7(store_select, 'Net Revenue')
    st.write(week[['Date', 'Store Name', 'Net Revenue', 'Online Revenue','In-Store Revenue', 'Eleme','Meituan']].style.set_precision(0))

    col_week1,  col_week2 = st.beta_columns([4,4])  
    with col_week1:
        st.subheader('Online Revenue')
        days7 = checkOut_last7(store_select, 'Online Revenue')
        days7 = days7[['Date', 'Store Name', 'Online Revenue']]
        st.write(days7.style.set_precision(0))

        st.subheader('In Store')
        days7 = checkOut_last7(store_select, 'In-Store Revenue')
        st.write(days7[['Date', 'Store Name', 'In-Store Revenue']].style.set_precision(0))

    with col_week2:
        st.subheader('Eleme')
        days7 = checkOut_last7(store_select, 'Eleme')
        st.write(days7[[ 'Date', 'Store Name', 'Eleme']].style.set_precision(0))

        st.subheader('Meituan')
        days7 = checkOut_last7(store_select, 'Meituan')
        st.write(days7[['Date', 'Store Name', 'Meituan']].style.set_precision(0))

    st.title('30 Days')
    days30 = checkOut_total_revenue_last30(store_select)
    st.write(days30[['Date', 'Store Name', 'Net Revenue', 'Eleme','Meituan','In-Store Revenue']].style.set_precision(0))

    st.title('All Time')
    all_time = checkOut_total_revenue(store_select)
    st.write(all_time[['Date', 'Store Name', 'Net Revenue', 'Eleme','Meituan','In-Store Revenue']].style.set_precision(0))

    
        

    