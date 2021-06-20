import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import plotly
import plotly.express as px
import openpyxl


pd.set_option('display.max_columns', None)

hg = sns.light_palette('green', as_cmap=True)


def app():

    #Color pallets for crosstabs
    hg = sns.light_palette('green', as_cmap=True)
    rocket = sns.color_palette("rocket_r", as_cmap=True)

    #------------------------
    


    #-------UPLOAD OLD DATA ----------
    df_old = pd.read_excel('/Users/simeonbourim/ML/OnlineMetrics/combineddata/flipCombined.xlsx',  engine='openpyxl')
    df_old = df_old.drop(df_old.columns[0], axis=1)

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
        today = pd.to_datetime("today")
        today = today.strftime("%Y-%m-%d")
        df_old.to_excel('/Users/simeonbourim/ML/OnlineMetrics/combineddata/flipbackup/FlipBackup'+today+'.xlsx')
        try:
            wb = pd.read_excel(uploaded_file, engine='openpyxl')
            
        except Exception as e:
            print(e)
            st.write('Wrong File Attached')
    try:
        #fix headers
        new_header = wb.iloc[1]
        wb = wb[1:]
        wb.columns = new_header
        wb = wb.drop(wb.index[[0,1]])
        #rename columns
        chc = wb.columns
        enc = {chc[0]:'Date',chc[1]:'Store Name',chc[2]:'Store ID',chc[3]:'City',chc[4]:'Order Count',chc[5]:'Gross Revenue',chc[6]:'Net Revenue',chc[7]:'Net Income',chc[8]:'出杯数', chc[9]:'Customer Count',chc[10]:'Completed Orders',chc[11]:'Average Spend',
        chc[12]:'Cash Pay',chc[13]:'Card Pay',chc[14]:'WeChat Pay',chc[15]:'WeChat Scan Pay',chc[16]:'Mini-App Pay',chc[17]:'Alipay',chc[18]:'Member Pay',chc[19]:'Net Member Pay',chc[20]:'Member Bonus',chc[21]:'Sherpas',chc[22]:'Boss Consumed',chc[23]:'Gift Voucher', chc[24]:'Gift Voucher Net Revenue',chc[25]:'Vocher Exchange',chc[26]:'Voucher Exchange Net Revenue',
        chc[27]:'Cash Voucher',chc[28]:'Loss',chc[29]:'领用',chc[30]:'Eleme',chc[31]:'Eleme Comission',chc[32]:'Eleme Fees',chc[33]:'Eleme Delivery Fee',chc[34]:'Meituan',chc[35]:'Meituan Comission',chc[36]:'Mietuan Delivery Fee',chc[37]:'Wiped to zero',chc[38]:'Total Discount',chc[39]:'Total Free',chc[40]:'Hold Order',chc[41]:'Returns',chc[42]:'Fapiao',chc[43]:'ReCharge',chc[44]:'Delivery Comission',chc[45]:'Delivery Fee',chc[46]:'在线活动预售',chc[47]:'在线活动核销 '}
        wb = wb.rename(columns=enc)
        #Add Weeks and Months
        wb['Date'] = pd.to_datetime(wb['Date'])
        wb['Week'] = wb['Date'].dt.isocalendar().week
        wb['Month'] = wb['Date'].dt.month
        #Replace 53 week with week 0
        wb['Week'] = wb['Week'].replace([53],[0])
        #move Weeks and Month to the front of the df
        sec_col = wb.pop('Month')
        first_col = wb.pop('Week')
        wb.insert(0, 'Month', sec_col )
        wb.insert(0, 'Week', first_col)
        #Rename Stores
        wb['Store Name'] = wb['Store Name'].replace({'Brothers Kebab兄弟烤肉店（古北家乐福店GB）': '6 Gubei', 'Brothers Kebab兄弟烤肉店（南京西路店TS）':'5 TS', 'Brothers Kebab兄弟烤肉店（淮海西路店MG）':'7 Magnolia','Brothers Kebab兄弟烤肉店（奉贤路店FX）': '2 Fengxian', 'Brothers Kebab兄弟烤肉店（巨鹿路店JL）': '8 Julu','Brothers Kebab 兄弟烤肉店（青岛店QD1）':'QD 1','Brothers Kebab兄弟烤肉店（长宁区店ZY）':'4 Zunyi','Brothers Kebab兄弟烤肉店（南泉北路店PD）':'3 Pudong','Brothers Kebab 兄弟烤肉店（长寿路店CS）':'9 CS','Brothers Kebab 兄弟烤肉店（漕溪路店CX）':'10 CX'})
        #Add online and instore revenue columns
        wb['Online Revenue'] = wb['Sherpas']+ wb['Eleme'] + wb['Meituan'] + wb['Mini-App Pay']
        wb['In-Store Revenue'] = wb['Net Revenue'] - wb['Online Revenue']
        
        #Merge with exisiting data
        #Append
        df_raw = df_old.append(wb)

        #duplicates
        df_raw.drop_duplicates(subset=['Date','Store Name','Net Revenue','Gross Revenue'],inplace=True)
    except Exception as e:
        print(e)

    try:
        df = df_raw
        #replace the old data with the combined data
        df.to_excel('combineddata/flipCombined.xlsx')
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
    
    

    #DF For Metrics Data
    df_metrics = df[['Date','Week','Month','Store Name','Net Revenue','Gross Revenue','Online Revenue','In-Store Revenue','Eleme','Meituan','Sherpas','Mini-App Pay']]
    
    #filter stores according to selections
    if len(store_select) == 0:
         pass
    elif len(store_select) > 0:
        df_metrics = df_metrics[df_metrics['Store Name'].isin(store_select)] 
    
    df_metrics.reset_index(inplace=True)

    # Convert Date to a readable format
    df_metrics['Date'] = pd.to_datetime(df_metrics['Date']).dt.date

    #Total Revenue
    df_rev_store = pd.crosstab(df_metrics[option].sort_values(ascending=False), df_metrics['Store Name'], values=df_metrics['Net Revenue'], aggfunc='sum', ).sort_index(ascending=False)
    df_rev_store.sort_values(by=[option], inplace=True, ascending=False)

    #Online vs offline
    df_channels = df_metrics[[option,'Online Revenue','In-Store Revenue','Net Revenue']]
    df_channels = df_channels.groupby(option).sum()
    df_channels.sort_values(by=[option], inplace=True, ascending=False)

    #Plot Chart Channels
    fig_channels = px.line(df_channels)
    fig_channels.update_layout(title_text='In-Store vs Online', title_x=0.5, xaxis_rangeslider_visible=True, legend=dict(x=0,y=1,traceorder='normal',
    bgcolor = 'rgba(255,255,255,.5)',
    font=dict(size=10,)))
    fig_channels.update_yaxes(title_text = 'Revenue')


    #Total per platform
    df_platform = df_metrics[[option,'Eleme','Meituan','Sherpas','Mini-App Pay' ]]
    df_platform = df_platform.groupby(option).sum()
    df_platform.sort_values(by=[option], inplace=True, ascending=False)

    #Plot Chart Channels
    fig_platform = px.line(df_platform)
    fig_platform.update_layout(title_text='Eleme, Meituan, Sherpas and Mini-App', title_x=0.5, xaxis_rangeslider_visible=True, legend=dict(x=0,y=1,traceorder='normal',
    bgcolor = 'rgba(255,255,255,.5)',
    font=dict(size=10,)))
    fig_platform.update_yaxes(title_text = 'Revenue')

     #-------------------------
     # MAIN DISPLAY
     #-------------------------

     #Define Columns
    col1,  col2 = st.beta_columns([4,4])
        # Last Date on current DF

    last = df['Date'].sort_values(ascending=False).iloc[0:1].dt.strftime('%m/%d/%Y').to_string()

    with col1:
        st.title('Reports')
        st.write('Period format:', option)
        st.write("Last date ends on: " + last.split(' ')[4])
   
    st.subheader('Total Revenue Per Shop')
    st.write(df_rev_store.style.background_gradient(cmap=hg, axis=0).format("{:,.0f}"))
    
    bcol1, bcol2 = st.beta_columns([4,4])
    with bcol2:
        st.plotly_chart(fig_channels, use_container_width=True)
    with bcol1:
        st.write('')
        st.write('')
        st.write('')
        st.subheader('Revenue Online/In Store')
        st.write(df_channels.style.background_gradient(cmap=hg, axis=0).format("{:,.0f}"))

    plat1, plat2 =st.beta_columns([4,4])
    with plat1:
        st.write('')
        st.write('')
        st.write('')
        st.subheader('Revenue by Online Platform')
        st.write(df_platform.style.background_gradient(cmap=hg, axis=0).format("{:,.0f}"))        
    with plat2:
        st.plotly_chart(fig_platform, use_container_width=True)


    