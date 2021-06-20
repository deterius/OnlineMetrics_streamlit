import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import plotly
import plotly.express as px
import openpyxl
from pandas.api.types import CategoricalDtype
from openpyxl.reader.excel import load_workbook
from openpyxl.workbook import Workbook



pd.set_option('display.max_columns', None)
hg = sns.light_palette('green', as_cmap=True)
rocket = sns.color_palette("rocket_r", as_cmap=True)


# @st.cache(suppress_st_warning=True) 

def app():


    
# -------------- Import and process
    df = pd.read_excel('combineddata/Flip_order_data/ALLorders.xlsx', engine='openpyxl')
    df=df.rename(columns={'门店':'Store Name','营业日期':'Date','下单时间':'Time','订单金额':'Revenue','支付方式':'Channel'})
    df['Channel'] = df['Channel'].replace({'饿了么外卖':'Eleme','美团外卖':'Meituan', '现金':'Cash', '支付宝':'Alipay', '微信':'WeChat', '食派士':'Sherpas', '刷卡':'Card', '微信小程序支付':'Mini App', '会员卡支付':'Member Pay','礼金卡':'Cash Voucher', '老板消费':'Employee/Boss'})
    df['Date'] = pd.to_datetime(df['Date'])
    df['Time'] = pd.to_datetime(df['Time'])
    df['Time']= df['Time'].dt.hour
    df['Day'] = df['Date'].dt.day_name()

   
    #Add numbers to day for sorting
    df['Day'] = df['Day'].replace({'Monday': '1 Monday', 'Tuesday':'2 Tuesday','Wednesday':'3 Wednesday','Thursday':'4 Thursday','Friday':'5 Friday','Saturday':'6 Saturday','Sunday':'7 Sunday'})


    #Rename Stores
    df['Store Name'] = df['Store Name'].replace({'Brothers Kebab兄弟烤肉店（古北家乐福店GB）': '6 Gubei', 'Brothers Kebab兄弟烤肉店（南京西路店TS）':'5 TS', 'Brothers Kebab兄弟烤肉店（淮海西路店MG）':'7 Magnolia','Brothers Kebab兄弟烤肉店（奉贤路店FX）': '2 Fengxian', 'Brothers Kebab兄弟烤肉店（巨鹿路店JL）': '8 Julu','Brothers Kebab 兄弟烤肉店（青岛店QD1）':'QD 1','Brothers Kebab兄弟烤肉店（长宁区店ZY）':'4 Zunyi','Brothers Kebab兄弟烤肉店（南泉北路店PD）':'3 Pudong','Brothers Kebab 兄弟烤肉店（长寿路店CS）':'9 CS','Brothers Kebab 兄弟烤肉店（漕溪路店CX）':'10 CX'})

    df.to_excel('combineddata/Flip_order_data/FlipOrders_combined.xlsx')
#---------------------------------------

    # -----------SET OPTIONS-----------
    freq = df[['Store Name','Time','Day','Revenue','Channel']]
    # freq = freq[freq['Store Name'] == 'Brothers Kebab 兄弟烤肉店（青岛店QD1）']
    # freq = freq[freq['Channel'] == 'Eleme' ]
    # freq = freq[freq['Day'] == 'Saturday' ]

    # cats = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    # freq['Day'] = pd.Categorical(freq['Day'], categories=cats, ordered=True)
    # freq = freq.sort_values('Day')
    # ---------------------------------

    #---------------- SIDEBAR -------------

    last = df['Date'].sort_values(ascending=False).iloc[0:1].dt.strftime('%m/%d/%Y').to_string()
    first = df['Date'].sort_values(ascending=True).iloc[0:1].dt.strftime('%m/%d/%Y').to_string()

    st.info("Dates start on: " + first.split(' ')[4]+ ". End on: " + last.split(' ')[4])

    # Sidebar - channel selection
    sorted_channels = sorted(freq['Channel'].unique())
    selected_channels = st.sidebar.multiselect(label='Revenue Channel', options=sorted_channels)

    if len(selected_channels) == 0:
         pass
    elif len(sorted_channels) != 0:
        freq = freq[freq['Channel'].isin(selected_channels)]
    
    # Sidebar - Day selection
    sorted_days = sorted(freq['Day'].unique())
    selected_days = st.sidebar.multiselect(label='Day', options=sorted_days)

    if len(selected_days) == 0:
         pass
    elif len(selected_days) > 0:
        freq = freq[freq['Day'].isin(selected_days)] 
        
     
        


    #-------------- SET DATA TABLES ----
    daily_rev = pd.crosstab(freq['Store Name'],freq['Day'], values=freq['Revenue'], aggfunc='count').apply(lambda r: (r/r.sum())*100, axis=1).style.background_gradient(cmap=hg, axis=1).format("{:,.0f}%")
    hourly_rev = pd.crosstab(freq['Store Name'],freq['Time'], values=freq['Revenue'], aggfunc='count').apply(lambda r: (r/r.sum())*100, axis=1).style.background_gradient(cmap=hg, axis=1).format("{:,.0f}%")
    total_hourly_rev = pd.crosstab(freq['Store Name'],freq['Time'], values=freq['Revenue'], aggfunc='count').style.background_gradient(cmap=hg, axis=1).format("{:,.0f}")
    #-----------------------------------



    # # ------------- DISPLAY PAGE---------
    st.title('Frequency')

    st.subheader('Revenue per day')
    st.write(daily_rev)

    st.subheader('Hourly Revenue')
    st.write(hourly_rev)

    st.subheader('Total # of orders')
    st.write(total_hourly_rev)
