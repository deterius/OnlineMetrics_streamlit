import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import plotly
import plotly.express as px
import openpyxl


def app():
    hg = sns.light_palette('green', as_cmap=True)
    rocket = sns.color_palette("rocket_r", as_cmap=True)

    #-------UPLOAD OLD DATA ----------
    df_old = pd.read_excel('combineddata/MeituanCombined.xlsx',  engine='openpyxl')


    #-------SIDE BAR -------
    st.subheader('Upload New Meituan Data')
    uploaded_file = st.file_uploader(label='Meituan: CSV file', type=['csv','xlsx'])
    global wb
    if uploaded_file is not None:
        try:
            wb = pd.read_csv(uploaded_file, encoding='gb2312')
        except:
            st.write('Wrong File Attached!')



    try:
        #Clean New data
        wb.iloc[:,0] = pd.to_datetime(wb.iloc[:,0]).dt.date
        
        wb.head()
        chc = wb.columns

        chc
        enc = {chc[0]:'Date',chc[1]:'Store Name',chc[2]:'Store ID',chc[3]:'City',chc[4]:'Net Revenue',
        chc[5]:'Original Price of Products',
        chc[6]:'Package Revenue',
        chc[7]:'Delivery Fee',
        chc[8]:'Expenses',
        chc[9]:'Store Subsidy (Total)',
        chc[10]:'MT Service Fee', 
        chc[11]:'Charity Donations',
        chc[12]:'Other Fees',
        chc[13]:'Gross Revenue',
        chc[14]:'Client Full Price',  
        chc[15]:'Completed Orders',
        chc[16]:'Average Basket Size (Full Price)',
        chc[17]:'Promotion Subsidies',  
        chc[18]:'Meituan Subsidies',
        chc[19]:'Views Count',
        chc[20]:'Click Count',
        chc[21]:'Order Count',
        chc[22]:'Click Conversion Rate',
        chc[23]:'Order Conversion Rate',
        chc[24]:'New Views',
        chc[25]:'New Clicks',
        chc[26]:'New Orders',
        chc[27]:'New Click Conversion',
        chc[28]:'New Order Conversion',
        chc[29]:'Return Views',
        chc[30]:'Return Clicks',
        chc[31]:'Return Orders',
        chc[32]:'Return Click Conversion',
        chc[33]:'Return Order Conversion',
        chc[34]:'Canceled Orders',
        chc[35]:'Store Canceled Orders',
        chc[36]:'Store Cancel Order Rate',
        chc[37]:'Late Delivery Orders',
        chc[38]:'Late Delivery Order Rate'}
        wb = wb.rename(columns=enc)
        wb.set_index(wb['Date'], inplace=True)
        wb = wb.drop(labels='Date', axis=1)

        cn_stores = wb['Store Name'].unique()
        wb['Store Name'] = wb['Store Name'].replace(cn_stores,['2 Fengxian','delete_store','4 Zunyi','3 Pudong','5 TS','6 Gubei','7 Magnolia','8 Julu','QD 1','9 CS','10 CX'])
        

        #Add Weeks and Months
        wb.reset_index(inplace=True)
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
        wb.head()

        #Merge with exisiting data
        #Append

        df_raw = df_old.append(wb)
        print(df_raw.columns.duplicated().any())

        #duplicates
        df_raw.drop_duplicates(subset=['Date','Store Name','Net Revenue'],inplace=True)

        
    except Exception as e:
        print(e)

    try:
        df = df_raw
        #replace the old data with the combined data
        df.to_excel('combineddata/MeituanCombined.xlsx')
    except Exception as e:
        print(e)
        df = df_old
    
    #Drop Extra Store
        df = df[df["Store Name"]!= 'delete_store']

    # ------------------------
    # Weekly Store revenue


    #Select Date format
    option = st.sidebar.selectbox(
       'Select report time format',
        ('Week', 'Date'))
        
    st.write('You selected:', option)
    

    #DF For Metrics Data
    df_metrics = df[['Date','Week','Month','Store Name','Net Revenue','Gross Revenue','Store Subsidy (Total)','New Order Conversion','Return Orders','Order Conversion Rate','New Orders']]
    df_metrics.reset_index(inplace=True)
    
    # Convert Date to a readable format
    df_metrics['Date'] = pd.to_datetime(df_metrics['Date']).dt.date

    #Total Revenue
    df_rev_store = pd.crosstab(df_metrics[option].sort_values(ascending=False), df_metrics['Store Name'], values=df_metrics['Net Revenue'], aggfunc='sum', ).sort_index(ascending=False)


    #New Customers
    df_nc = pd.crosstab(df_metrics[option], df_metrics['Store Name'], values=df_metrics['New Orders'], aggfunc='sum').sort_index(ascending=False)

    #Returning Customers
    df_ret = pd.crosstab(df_metrics[option], df_metrics['Store Name'], values=df_metrics['Return Orders'], aggfunc='sum').sort_index(ascending=False)

    #Total discount
    df_disc = df_metrics[['Date','Week','Store Name','Gross Revenue','Store Subsidy (Total)']]
    df_disc['Discount'] = df_disc['Store Subsidy (Total)'] / df_disc['Gross Revenue']
    df_disc = pd.crosstab(df_disc[option], df_disc['Store Name'], values=df_disc['Discount'], aggfunc='mean').sort_index(ascending=False)

    #New Customer Order Conversion
    df_nc_con = pd.crosstab(df_metrics[option], df_metrics['Store Name'], values=df_metrics['New Order Conversion'], aggfunc='mean').sort_index(ascending=False)

    df_total_conv = pd.crosstab(df_metrics[option], df_metrics['Store Name'], values=df_metrics['Order Conversion Rate'], aggfunc='mean').sort_index(ascending=False)


    # Plot lines
    dflines= pd.crosstab(df_metrics[option], df_metrics['Store Name'], values=df_metrics['Net Revenue'], aggfunc='sum')
    fig = px.line(dflines)
    fig.update_layout(title_text='Revenue per store', title_x=0.5, xaxis_rangeslider_visible=True, )
    fig.update_yaxes(title_text = 'Revenue')


    #-------------------------
    st.title('Meituan Reports')
    # Last Date on current DF
    last = df['Date'].sort_values(ascending=False).iloc[0:1].dt.strftime('%m/%d/%Y').to_string()
    st.write("Last date ends on: " + last.split(' ')[4])

    #plot lines - 
    st.plotly_chart(fig)
    st.subheader('Weekly Revenue')
    st.write(df_rev_store.style.background_gradient(cmap=hg).format("{:,.0f}"))


    st.subheader('New Customer Count')
    st.write(df_nc.style.background_gradient(cmap=hg).format("{:,.0f}"))

    st.subheader('Returners Count')
    st.write(df_ret.style.background_gradient(cmap=hg).format("{:,.0f}"))

    st.subheader('Total Discount Rate')
    st.write(df_disc.style.background_gradient(cmap=rocket).format("{:,.2f}"))

    st.subheader('New Customer Order Conversion')
    st.write(df_nc_con.style.background_gradient(cmap=hg).format("{:,.2f}"))

    st.subheader('Total Conversion Rate')
    st.write(df_total_conv.style.background_gradient(cmap=hg).format("{:,.2f}"))