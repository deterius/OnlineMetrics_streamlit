from pandas.core import groupby
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import plotly
import plotly.express as px
import openpyxl

# helper functions
from helper_functions import *


pd.set_option('display.max_columns', None)

hg = sns.light_palette('green', as_cmap=True)


def app():

    #Color pallets for crosstabs
    hg = sns.light_palette('green', as_cmap=True)
    rocket = sns.color_palette("rocket_r", as_cmap=True)

    #------------------------
    


    #-------UPLOAD OLD DATA ----------
    # df_old = pd.read_excel('combineddata/FlipCombined.xlsx',  engine='openpyxl')    
    df_old = pd.read_parquet('combineddata/FlipCombined.parquet')

    # df_old = df_old.drop(df_old.columns[0], axis=1)

    #-------UPLOAD FILE -------
    h1, h2 = st.beta_columns([1,1])
    with h1:
        st.subheader('Upload New FlipOS Data')
        st.write('Upload Flip OS data, make sure to get the old financial report and select all headers.')
    with h2:
        uploaded_file = st.file_uploader(label='Upload FlipOS Excel Data', type=['csv','xlsx'])

    global wb
    if uploaded_file is not None:
        #create backup of old file
        print('1. Creating backup')
        today = pd.to_datetime("today")
        today = today.strftime("%Y-%m-%d")
        df_old.to_parquet('combineddata/flipbackup/Flip'+ today +'Backup.parquet')
        # df_old.to_excel('combineddata/flipbackup/Flip'+ today +'Backup.xlsx')
        try:
            wb = pd.read_excel(uploaded_file, engine='openpyxl')
            
        except Exception as e:
            print(e)
            st.write('Wrong File Attached')
    try:
        #fix headers
        print('2. Fixing headers')
     
        new_header = wb.iloc[1]
        wb = wb[1:]
        wb.columns = new_header
        wb = wb.drop(wb.index[[0,1]])
        

    
        #Convert to numeric
        print('Converting to numeric')
        num_cols = ['门店编号']
        wb[num_cols] = wb[num_cols].apply(pd.to_numeric, errors='ignore')
        
        #rename columns
        print('3. Renaming')
        chc = wb.columns
        print(chc)
        enc = {'日期':'Date','门店名':'Store Name','门店编号':'Store ID','门店区域':'City','订单数':'Order Count','应收营业额':'Gross Revenue','实收营业额':'Net Revenue','实收净额':'Net Income','出杯数':'出杯数', '客人数':'Customer Count','有效单数':'Completed Orders','客单价':'Average Spend',
        '现金支付':'Cash Pay','刷卡支付':'Card Pay','微信支付':'WeChat Pay','微信扫码支付':'WeChat Scan Pay','小程序支付':'Mini-App Pay','支付宝支付':'Alipay','会员卡支付':'Member Pay','会员卡支付净额':'Net Member Pay','会员卡支付赠额':'Member Bonus','食派士':'Sherpas','老板消费':'Boss Consumed','礼品抵扣券':'Gift Voucher', '礼品抵扣券实收':'Gift Voucher Net Revenue','礼品兑换券':'Voucher Exchange','礼品兑换券实收':'Voucher Exchange Net Revenue',
        '礼金卡':'Cash Voucher','报损':'Loss','领用':'领用','饿了么外卖':'Eleme','饿了么外卖佣金':'Eleme Comission','饿了么外卖平台加价':'Eleme Fees','美团外卖':'Meituan','美团外卖佣金':'Meituan Comission','抹零':'Wiped to zero','打折':'Total Discount','赠送':'Total Free','挂账':'Hold Order','退款':'Returns','发票':'Fapiao','充值':'ReCharge','外卖佣金':'Delivery Comission','配送费':'Delivery Fee','在线活动预售':'在线活动预售','在线活动核销':'在线活动核销 '}
        wb = wb.rename(columns=enc)
        
        
        
        #Add Weeks and Months
        wb['Date'] = pd.to_datetime(wb['Date'])
        wb['Week'] = wb['Date'].dt.isocalendar().week
        wb['Month'] = wb['Date'].dt.month
        #Replace 53 week with week 0
        print('4.1 Replace week 53')
        wb['Week'] = wb['Week'].replace([53],[0])
        #move Weeks and Month to the front of the df
        print('5. Moving week/month columns')
        sec_col = wb.pop('Month')
        first_col = wb.pop('Week')
        wb.insert(0, 'Month', sec_col )
        wb.insert(0, 'Week', first_col)
        #Rename Stores
        print('6. Renaming Stores')
        wb['Store Name'] = wb['Store Name'].replace({'Brothers Kebab兄弟烤肉店（古北家乐福店GB）': '6 Gubei', 'Brothers Kebab兄弟烤肉店（南京西路店TS）':'5 TS', 'Brothers Kebab兄弟烤肉店（淮海西路店MG）':'7 Magnolia','Brothers Kebab兄弟烤肉店（奉贤路店FX）': '2 Fengxian', 'Brothers Kebab兄弟烤肉店（巨鹿路店JL）': '8 Julu','Brothers Kebab 兄弟烤肉店（青岛店QD1）':'QD 1','Brothers Kebab兄弟烤肉店（长宁区店ZY）':'4 Zunyi','Brothers Kebab兄弟烤肉店（南泉北路店PD）':'3 Pudong','Brothers Kebab 兄弟烤肉店（长寿路店CS）':'9 CS','Brothers Kebab 兄弟烤肉店（漕溪路店CX）':'10 CX'})
        #Add online and instore revenue columns
        print('6.1 Add online and instore revenue columns')
        wb['Online Revenue'] = wb['Sherpas']+ wb['Eleme'] + wb['Meituan'] + wb['Mini-App Pay']
        wb['In-Store Revenue'] = wb['Net Revenue'] - wb['Online Revenue'] - wb['Net Member Pay']
        print('DONE: Add online and instore revenue columns')

        #Merge with exisiting data
        #Append
        print('7. Merging with old df')
        df_raw = df_old.append(wb)

        #duplicates
        print('4. Dropping Duplicates')
        df_raw.drop_duplicates(subset=['Date','Store Name','Net Revenue','Gross Revenue'],inplace=True)
    except Exception as e:
        print(e)

    try:
        df = df_raw
        #replace the old data with the combined data
        # df.to_excel('combineddata/flipCombined.xlsx')
        df.to_parquet('combineddata/flipCombined.parquet')
    except Exception as e:
        print(e)
        df = df_old


    # ------------------------
    # MAIN BACKEND

    #Select Date format
    option = st.sidebar.selectbox(
    'Select report time format',
        ('Week', 'Month', 'Date'))
    
    # #select stores
    stores = df['Store Name'].unique()
    store_select = st.sidebar.multiselect( "Select Stores", stores)
    
    # Sets rolling window for SMA functions
    rolling_window = rolling_window_func(option)
    

    #DF For Metrics Data
    df_metrics = df[['Date','Week','Month','Store Name','Net Revenue','Gross Revenue','Online Revenue','In-Store Revenue','Eleme','Meituan','Sherpas','Mini-App Pay','Customer Count','Completed Orders']]
    
    #filter stores according to selections
    if len(store_select) == 0:
         pass
    elif len(store_select) > 0:
        df_metrics = df_metrics[df_metrics['Store Name'].isin(store_select)] 
    
    df_metrics.reset_index(inplace=True)

    # Convert Date to a readable format
    df_metrics['Date'] = pd.to_datetime(df_metrics['Date']).dt.date

    #Total Revenue + (SMA Revenue)
    
    df_total_rev_group = total_revenue(df_metrics,option)
    df_total_rev = pd.DataFrame(df_total_rev_group)
    
   # define SMA line
    df_total_rev['SMA'] = df_total_rev.loc[:,'Net Revenue'].rolling(window=rolling_window).mean()

    # Add Plot
    tot_rev = plotter_func(df_total_rev, 'Total Revenue (all stores) - 收入(所有店）', 'Revenue')

    #Total Revenue per shop
    df_rev_store = revenue_per_shop(df_metrics,option,'Store Name', 'Net Revenue')
    # Add Plot
    fig_rev_channels = complex_plot(df_rev_store, 'Total Revenue Per Shop 收入/店', 'Revenue 收入','Date 日期')

    #SMA per store
    df_sma_store = sma_per_store(df_metrics,option,'Store Name','Net Revenue',rolling_window)
    sma_store_fig = plotter_func(df_sma_store, 'SMA Per Store Average', 'SMA Revenue')

    #Online vs offline
    df_channels = df_metrics[[option,'Online Revenue','In-Store Revenue','Net Revenue' ]]
    df_channels = df_channels.groupby(option).sum()
    df_channels.sort_values(by=[option], inplace=True, ascending=False)
    #SMA Online vs offline
    df_sma_channels = sma_per_col(df_channels, rolling_window)
    fig_channels = complex_plot(df_sma_channels, 'SMA - In-Store vs Online （堂吃-上线）', 'Revenue 收入','Date 日期')
    

  
    #Total per platform
    df_platform = df_metrics[[option,'Eleme','Meituan','Sherpas','Mini-App Pay' ]]
    df_platform = df_platform.groupby(option).sum()
    df_platform.sort_values(by=[option], inplace=True, ascending=False)
    #SMA Total per platform
    df_sma_platform = sma_per_col(df_platform, rolling_window)
    fig_sma_platform = complex_plot(df_sma_platform, 'Platfroms SMA','Revenue','Date')
  

    #Total Customers
    df_orders = df_metrics[[option,'Completed Orders']]
    df_orders = df_orders.groupby(option).sum()
    df_orders.sort_values(by=[option], inplace=True, ascending=False)

     #-------------------------
     # MAIN DISPLAY
     #-------------------------

     #Define Columns
    col1,  col2 = st.beta_columns([4,4])
        # Last Date on current DF

    last = df['Date'].sort_values(ascending=False).iloc[0:1].dt.strftime('%m/%d/%Y').to_string()

    with col1:
        st.title('Reports 报表')
        st.write('Period format:', option)
        st.write("Last date ends on: " + last.split(' ')[4])
   
    st.subheader('Total Revenue Per Shop 各店收入')
    st.plotly_chart(tot_rev, use_container_width=True)
    st.write(sma_store_fig)
    st.write(df_rev_store.style.background_gradient(cmap=hg, axis=0).format("{:,.0f}"))
    
    bcol1, bcol2 = st.beta_columns([4,4])
    with bcol2:
        st.plotly_chart(fig_channels, use_container_width=True)
    with bcol1:
        st.write('')
        st.write('')
        st.write('')
        st.subheader('Revenue Online/In Store 收入 上线/堂吃')
        st.write(df_channels.style.background_gradient(cmap=hg, axis=0).format("{:,.0f}"))

    plat1, plat2 =st.beta_columns([4,4])
    with plat1:
        st.write('')
        st.write('')
        st.write('')
        st.subheader('Revenue by Online Platform 上线平台收入')
        st.write(df_platform.style.background_gradient(cmap=hg, axis=0).format("{:,.0f}"))        
    with plat2:
        st.write(fig_sma_platform)


    st.write(df_orders.style.background_gradient(cmap=hg, axis=0).format("{:,.0f}"))