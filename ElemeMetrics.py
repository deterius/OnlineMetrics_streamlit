import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import plotly
import plotly.express as px
import openpyxl
from PIL import Image



def app():
    #Color pallets for crosstabs
    hg = sns.light_palette('green', as_cmap=True)
    rocket = sns.color_palette("rocket_r", as_cmap=True)

    #------------------------
    #Define Columns
    col1, buffer, col3 = st.beta_columns([4,1,4])

    #-------UPLOAD OLD DATA ----------
    df_old = pd.read_excel('combineddata/ElemeCombined.xlsx',  engine='openpyxl')

    #-------UPLOAD FILE -------
    st.subheader('Upload New Eleme Data')
    uploaded_file = st.file_uploader(label='Eleme: XLSX file', type=['csv','xlsx'])


    global wb
    if uploaded_file is not None:
        #create backup of old file
        today = pd.to_datetime("today")
        today = today.strftime("%Y-%m-%d")
        df_old.to_excel('combineddata/Elemebackup/eleme'+today+'.xlsx')
        try:
            wb = pd.read_excel(uploaded_file, engine='openpyxl')
        except Exception as e:
            print(e)
            st.write('Wrong File Attached')

    try:
        #Clean New data
        wb.iloc[:,0] = pd.to_datetime(wb.iloc[:,0]).dt.date
        chc = wb.columns
        enc = {chc[0]:'Date',chc[1]:'Store Name',chc[2]:'Store ID',chc[3]:'City',chc[4]:'Operation Time',chc[5]:'Peake Time'
        ,chc[6]:'Completed Orders',chc[7]:'Failed Orders',chc[8]:'Net Revenue',chc[9]:'Gross Revenue',chc[10]:'Expenses'
        ,chc[11]:'Customer Actual Price Payed',chc[12]:'Average Actual Price Payed',chc[13]:'Average Revenue',chc[14]:'Products Total Price'
        ,chc[15]:'Package Revenue',chc[16]:'Self-Delivery Fee',chc[17]:'Other Revenues',chc[18]:'Comission',chc[19]:'Promotion Subsidies Total'
        ,chc[20]:'Voucher Subsidies',chc[21]:'Delivery Subsidies',chc[22]:'AI Spend-Save Subsidy',chc[23]:'AI Service Fee',chc[24]:'Basic Logistic Fee'
        ,chc[25]:'Other Service Fees',chc[26]:'Store Canceled Orders',chc[27]:'Clicks',chc[28]:'Visitors',chc[29]:'Order Conversion Rate'
        ,chc[30]:'New Customer Conversion Rate',chc[31]:'Returners Conversion Rate',chc[32]:'Participating Promotions',chc[33]:'Promotions Number in orders'
        ,chc[34]:'Promotions per order',chc[35]:'Spend Save Promotion Count',chc[36]:'Super User promotion count',chc[37]:'Delivery promotion count'
        ,chc[38]:'Input/Output Ratio',chc[39]:'Total Subsidy',chc[40]:'Eleme Subsidy',chc[41]:'Third-party subsidy',chc[42]:'Store Subsidy (Total)'
        ,chc[43]:'Store Subsidy(Not Incl. Spend Save)',chc[44]:'Promotion Rate (Total)',chc[45]:'Promotion Rate (Not incl. spend save)'
        ,chc[46]:'Order Count',chc[47]:'Repurchase Count',chc[48]:'Repurchase Rate',chc[49]:'New Customer Count',chc[50]:'Returners Count'
        ,chc[51]:'Active Product Count',chc[52]:'Purchased Products Count',chc[53]:'86 Product Count',chc[54]:'New Products Count'
        ,chc[55]:'Promotional Product Count',chc[56]:'Negative Revew Product Count',chc[57]:'Complaint Order Count',chc[58]:'Complaint Order ID'
        ,chc[59]:'Overtime Order Count',chc[60]:'Overtime Order ID',chc[61]:'Pushed Order Count',chc[62]:'Refused Orders Count'}
        wb = wb.rename(columns=enc)
        wb.set_index(wb['Date'], inplace=True)
        wb = wb.drop(labels='Date', axis=1)
        wb['Store Name'] = wb['Store Name'].replace({'兄弟烤肉Brothers Kebab  烤肉卷(古北家乐福店)': '6 Gubei', '兄弟烤肉Brothers Kebab  烤肉卷(南京西路店)':'5 TS', '兄弟烤肉Brothers Kebab  烤肉卷(淮海西路店)':'7 Magnolia','兄弟烤肉Brothers Kebab  烤肉卷(奉贤路店)': '2 Fengxian', '兄弟烤肉Brothers Kebab  烤肉卷(巨鹿路店)': '8 Julu','Brothers Kebab兄弟烤肉店(香港中路店)':'QD 1','兄弟烤肉Brothers Kebab  烤肉卷(长宁区店)':'4 Zunyi','兄弟烤肉Brothers Kebab  烤肉卷(南泉北路店)':'3 Pudong','兄弟烤肉Brothers Kebab 烤肉卷(长寿路店)':'9 CS','兄弟烤肉Brothers Kebab 烤肉卷(漕溪路店)':'10 CX'})

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

        #duplicates
        df_raw.drop_duplicates(subset=['Date','Store Name','Net Revenue','Gross Revenue'],inplace=True)
    except Exception as e:
        print(e)


    try:
        df = df_raw
        #replace the old data with the combined data
        df.to_excel('combineddata/ElemeCombined.xlsx')
    except Exception as e:
        print(e)
        df = df_old

    


    # ------------------------
    # MAIN BODY

    #Select Date format
   
    option = st.sidebar.selectbox(
    'Select report time format',
        ('Week', 'Month', 'Date'))
    st.write('Period Type:', option)

    # #select stores
    stores = df['Store Name'].unique()
    store_select = st.sidebar.multiselect( "Select Stores", stores)


    #DF For Metrics Data
    df_metrics = df[['Date','Week','Month','Store Name','Net Revenue','Gross Revenue','Store Subsidy (Total)','New Customer Count','Returners Count','New Customer Conversion Rate','Order Conversion Rate','Completed Orders']]
    
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


    #New Customers
    df_nc = pd.crosstab(df_metrics[option], df_metrics['Store Name'], values=df_metrics['New Customer Count'], aggfunc='sum').sort_index(ascending=False)

    #Returning Customers
    df_ret = pd.crosstab(df_metrics[option], df_metrics['Store Name'], values=df_metrics['Returners Count'], aggfunc='sum').sort_index(ascending=False)

    #Returning Customers Rate (Returners / Total Customers)
    df_ret_rate = df_metrics[['Date','Week','Month','Store Name','Completed Orders','Returners Count','New Customer Count']]
    df_ret_rate['Returners Rate'] = df_ret_rate['Returners Count'] / (df_ret_rate['Returners Count'] + df_ret_rate['New Customer Count'])
    df_ret_rate = pd.crosstab(df_ret_rate[option], df_ret_rate['Store Name'], values=df_ret_rate['Returners Rate'], aggfunc='mean').sort_index(ascending=False)
    
    #New Customers Rate (Returners / Total Customers)
    df_nc_rate = df_metrics[['Date','Week','Month','Store Name','Completed Orders','Returners Count','New Customer Count']]
    df_nc_rate['Returners Rate'] = df_nc_rate['New Customer Count'] / (df_nc_rate['Returners Count'] + df_nc_rate['New Customer Count'])
    df_nc_rate = pd.crosstab(df_nc_rate[option], df_nc_rate['Store Name'], values=df_nc_rate['Returners Rate'], aggfunc='mean').sort_index(ascending=False)
    
    #Total discount
    df_disc = df_metrics[['Date','Week','Month','Store Name','Gross Revenue','Store Subsidy (Total)']]
    df_disc['Discount'] = df_disc['Store Subsidy (Total)'] / df_disc['Gross Revenue']
    df_disc = pd.crosstab(df_disc[option], df_disc['Store Name'], values=df_disc['Discount'], aggfunc='mean').sort_index(ascending=False)

    #New Customer Order Conversion
    df_nc_con = pd.crosstab(df_metrics[option], df_metrics['Store Name'], values=df_metrics['New Customer Conversion Rate'], aggfunc='mean').sort_index(ascending=False)

    df_total_conv = pd.crosstab(df_metrics[option], df_metrics['Store Name'], values=df_metrics['Order Conversion Rate'], aggfunc='mean').sort_index(ascending=False)


    # Plot lines
    dflines= pd.crosstab(df_metrics[option], df_metrics['Store Name'], values=df_metrics['Net Revenue'], aggfunc='sum')
    fig = px.line(dflines)
    fig.update_layout(title_text='Revenue per store', title_x=0.5, xaxis_rangeslider_visible=True)
    fig.update_yaxes(title_text = 'Revenue')

#     # line_fig = px.line(multiplayer_df, x='date', y='statPoints', color='name')
# line_fig.update_layout(title_text='test', title_x=0.5, xaxis_rangeslider_visible=True, legend=dict(x=-.5, y=-2))
# line_fig.update_yaxes(title_text='Cumulative Points')

    #-------------------------
    

    st.title('Eleme Reports')

    # Last Date on current DF
    last = df['Date'].sort_values(ascending=False).iloc[0:1].dt.strftime('%m/%d/%Y').to_string()
    st.info("Last date ends on: " + last.split(' ')[4])


   
    #plot lines - 
    
    st.plotly_chart(fig, use_container_width=True)

 
    st.subheader('Total Eleme Revenue')
    st.write(df_rev_store.style.background_gradient(cmap=hg, axis=0).format("{:,.0f}"))

    st.subheader('New Customer Count')
    st.write(df_nc.style.background_gradient(cmap=hg, axis=0).format("{:,.0f}"))

    st.subheader('Returners Count')
    st.write(df_ret.style.background_gradient(cmap=hg, axis=0).format("{:,.0f}"))

    st.subheader('New Customers Rate (NC/Total Customers)')
    st.write(df_nc_rate.style.background_gradient(cmap=rocket, axis=0).format("{:,.2f}"))

    st.subheader('Returners Rate (Returners/Total Customers)')
    st.write(df_ret_rate.style.background_gradient(cmap=rocket, axis=0).format("{:,.2f}"))


    st.subheader('Total Discount Rate')
    st.write(df_disc.style.background_gradient(cmap=rocket, axis=0).format("{:,.2f}"))

    st.subheader('New Customer Order Conversion')
    st.write(df_nc_con.style.background_gradient(cmap=hg, axis=0).format("{:,.2f}"))

    st.subheader('Total Conversion Rate')
    st.write(df_total_conv.style.background_gradient(cmap=hg, axis=0).format("{:,.2f}"))