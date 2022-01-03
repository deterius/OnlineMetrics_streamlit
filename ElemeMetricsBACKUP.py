from numpy.core.numeric import True_
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import plotly
import plotly.express as px
import openpyxl
from PIL import Image
from openpyxl.reader.excel import load_workbook
from openpyxl.workbook import Workbook



def app():
    
    use_old = True
    
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
        print('Making backup')
        today = pd.to_datetime("today")
        today = today.strftime("%Y-%m-%d")
        
        df_old.to_excel('combineddata/Elemebackup/elemeBackup'+ today +'.xlsx', index=False)
        try:
            print('Reading uploaded file')
            wb_raw = load_workbook(uploaded_file)
            wb1 = wb_raw['data']
            print('creating WB')
            wb = pd.DataFrame(wb1.values)
            #replace header
            new_header = wb.iloc[0]
            wb = wb[1:]
            wb.columns = new_header
        except Exception as e:
            print(e)
            st.write('Wrong File Attached')

    try:
        print('Clean New Data')
        #Clean New data
    
        # chc = wb.columns
        # enc = {chc['日期']:'Date',chc['门店名称']:'Store Name',chc['门店id']:'Store ID',chc['城市名称']:'City',chc['营业时长']:'Operation Time',chc['高峰营业时长']:'Peak Time'
        # ,chc['有效订单']:'Completed Orders',chc['无效订单']:'Failed Orders',chc['收入']:'Net Revenue',chc['营业额']:'Gross Revenue',chc['支出']:'Expenses'
        # ,chc['顾客实付总额']:'Customer Actual Price Payed',chc['单均实付']:'Average Actual Price Payed',chc['单均收入']:'Average Revenue',chc['商品销售额']:'Products Total Price'
        # ,chc['餐盒费']:'Package Revenue',chc['自配送费']:'Self-Delivery Fee',chc['其他营业额']:'Other Revenues',chc['抽佣']:'Comission',chc['活动补贴']:'Promotion Subsidies Total'
        # ,chc['代金券补贴']:'Voucher Subsidies',chc['配送费补贴']:'Delivery Subsidies',chc['智能满减补贴']:'AI Spend-Save Subsidy',chc['智能满减服务费']:'AI Service Fee',chc['基础物流费']:'Basic Logistic Fee'
        # ,chc['其他服务费支出']:'Other Service Fees',chc['商户原因无效订单数']:'Store Canceled Orders',chc['曝光人数']:'Views People',chc['曝光次数']:'Views Count', chc['进店次数']:'Clicks',chc['进店人数']:'Visitors'
        # ,chc['进店转化率']:'Visit Conversion Rate',chc['下单转化率']:'Order Conversion Rate'
        # ,chc['新客下单转化率']:'New Customer Conversion Rate',chc['老客下单转化率']:'Returners Conversion Rate',chc['参与活动数']:'Participating Promotions',chc['活动订单数']:'Promotions Number in orders'
        # ,chc['活动订单占比']:'Promotions per order',chc['满减活动订单数']:'Spend Save Promotion Count',chc['超会活动订单数']:'Super User promotion count',chc['配送活动订单数']:'Delivery promotion count'
        # ,chc['投入产出比']:'Input/Output Ratio',chc['活动总补贴']:'Total Subsidy',chc['饿了么补贴']:'Eleme Subsidy',chc['代理商补贴']:'Third-party subsidy',chc['商家活动成本（含满减活动）']:'Store Subsidy (Total)'
        # ,chc['商家活动成本（不含满减活动）']:'Store Subsidy(Not Incl. Spend Save)',chc['营销力度（含满减活动）']:'Promotion Rate (Total)',chc['营销力度（不含满减活动）']:'Promotion Rate (Not incl. spend save)'
        # ,chc['下单人数']:'Order Count',chc['复购人数']:'Repurchase Count',chc['复购率']:'Repurchase Rate',chc['新客人数']:'New Customer Count',chc['老客人数']:'Returners Count'
        # ,chc['上架商品数']:'Active Product Count',chc['有交易商品数']:'Purchased Products Count',chc['库存不足商品数']:'86 Product Count',chc['新上架商品数']:'New Products Count'
        # ,chc['活动商品数']:'Promotional Product Count',chc['差评订单数']:'Negative Revew Product Count',chc['投诉订单数']:'Complaint Order Count',chc['投诉订单id']:'Complaint Order ID'
        # ,chc['出餐超时订单数']:'Overtime Order Count',chc['出餐超时订单id']:'Overtime Order ID',chc['单均出餐时长']:'Pushed Order Count',chc['拒单数']:'Refused Orders Count'}
        print('Setting renamed columns')
        wb.rename(columns={'日期':'Date','门店名称':'Store Name','门店id':'Store ID','城市名称':'City','营业时长':'Operation Time','高峰营业时长':'Peak Time'
        ,'有效订单':'Completed Orders','无效订单':'Failed Orders','收入':'Net Revenue','营业额':'Gross Revenue','支出':'Expenses'
        ,'顾客实付总额':'Customer Actual Price Payed','单均实付':'Average Actual Price Payed','单均收入':'Average Revenue','商品销售额':'Products Total Price'
        ,'餐盒费':'Package Revenue','自配送费':'Self-Delivery Fee','其他营业额':'Other Revenues','抽佣':'Comission','活动补贴':'Promotion Subsidies Total'
        ,'代金券补贴':'Voucher Subsidies','配送费补贴':'Delivery Subsidies','智能满减补贴':'AI Spend-Save Subsidy','智能满减服务费':'AI Service Fee','基础物流费':'Basic Logistic Fee'
        ,'其他服务费支出':'Other Service Fees','商户原因无效订单数':'Store Canceled Orders','曝光人数':'Views People','曝光次数':'Views Count', '进店次数':'Clicks','进店人数':'Visitors'
        ,'进店转化率':'Visit Conversion Rate','下单转化率':'Order Conversion Rate'
        ,'新客下单转化率':'New Customer Conversion Rate','老客下单转化率':'Returners Conversion Rate','参与活动数':'Participating Promotions','活动订单数':'Promotions Number in orders'
        ,'活动订单占比':'Promotions per order','满减活动订单数':'Spend Save Promotion Count','超会活动订单数':'Super User promotion count','配送活动订单数':'Delivery promotion count'
        ,'投入产出比':'Input/Output Ratio','活动总补贴':'Total Subsidy','饿了么补贴':'Eleme Subsidy','代理商补贴':'Third-party subsidy','商家活动成本（含满减活动）':'Store Subsidy (Total)'
        ,'商家活动成本（不含满减活动）':'Store Subsidy(Not Incl. Spend Save)','营销力度（含满减活动）':'Promotion Rate (Total)','营销力度（不含满减活动）':'Promotion Rate (Not incl. spend save)'
        ,'下单人数':'Order Count','复购人数':'Repurchase Count','复购率':'Repurchase Rate','新客人数':'New Customer Count','老客人数':'Returners Count'
        ,'上架商品数':'Active Product Count','有交易商品数':'Purchased Products Count','库存不足商品数':'86 Product Count','新上架商品数':'New Products Count'
        ,'活动商品数':'Promotional Product Count','差评订单数':'Negative Revew Product Count','投诉订单数':'Complaint Order Count','投诉订单id':'Complaint Order ID'
        ,'出餐超时订单数':'Overtime Order Count','出餐超时订单id':'Overtime Order ID','单均出餐时长':'Pushed Order Count','拒单数':'Refused Orders Count'}, inplace=True)
        

        wb.set_index(wb['Date'], inplace=True)
        wb = wb.drop(labels='Date', axis=1)
        print('Renaming Stores')
        # wb['Store Name'] = wb['Store Name'].replace({'兄弟烤肉Brothers Kebab  烤肉卷(古北家乐福店)': '6 Gubei', '兄弟烤肉Brothers Kebab  烤肉卷(南京西路店)':'5 TS', '兄弟烤肉Brothers Kebab  烤肉卷(淮海西路店)':'7 Magnolia','兄弟烤肉Brothers Kebab  烤肉卷(奉贤路店)': '2 Fengxian', '兄弟烤肉Brothers Kebab  烤肉卷(巨鹿路店)': '8 Julu','Brothers Kebab兄弟烤肉店(香港中路店)':'QD 1','兄弟烤肉Brothers Kebab  烤肉卷(长宁区店)':'4 Zunyi','兄弟烤肉Brothers Kebab  烤肉卷(南泉北路店)':'3 Pudong','兄弟烤肉Brothers Kebab 烤肉卷(长寿路店)':'9 CS','兄弟烤肉Brothers Kebab 烤肉卷(漕溪路店)':'10 CX'})
        wb['Store Name'] = wb['Store Name'].replace({'兄弟烤肉Brothers Kebab  烤肉卷(古北家乐福店)': '6 Gubei', '兄弟烤肉Brothers Kebab  烤肉卷(南京西路店)':'5 TS', '兄弟烤肉Brothers Kebab  烤肉卷(淮海西路店)':'7 Magnolia','兄弟烤肉Brothers Kebab  烤肉卷(奉贤路店)': '2 Fengxian', '兄弟烤肉Brothers Kebab  烤肉卷(巨鹿路店)': '8 Julu','Brothers Kebab兄弟烤肉店(香港中路店)':'QD 1','兄弟烤肉Brothers Kebab  烤肉卷(长宁区店)':'4 Zunyi','兄弟烤肉Brothers Kebab  烤肉卷(南泉北路店)':'3 Pudong','兄弟烤肉Brothers Kebab 烤肉卷(长寿路店)':'9 CS','兄弟烤肉Brothers Kebab 烤肉卷(漕溪路店)':'10 CX'})

        #Add Weeks and Months
        print('Add weeks and months')

        # wb.reset_index(inplace=True)
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
        
        
        #Merge with exisiting data
        #Append
        print('Append new data')
        print(df_old.dtypes)
        
        
        df_raw = df_old.append(wb)

        #duplicates
        df_raw.drop_duplicates(subset=['Date','Store Name','Net Revenue','Gross Revenue'],inplace=True)
        try:
            #replace the old data with the combined data
            print('replace the old data with the combined data')
            df_raw.to_excel('combineddata/ElemeCombined.xlsx', index=False)
            df_old = False
        except Exception as e:
            print(e)
            print('use old df')
            if df_old == True:
                df = df_old
            else:
                df = df_raw
        
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
    st.write(use_old)
    stores = df['Store Name'].unique()
    store_select = st.sidebar.multiselect( "Select Stores", stores)


    #DF For Metrics Data
    df_metrics = df[['Date','Week','Month','Store Name','Net Revenue','Gross Revenue','Store Subsidy (Total)','New Customer Count','Returners Count','New Customer Conversion Rate','Order Conversion Rate','Completed Orders', 'Visitors','Average Actual Price Payed','Negative Revew Product Count','Complaint Order Count','Overtime Order Count']]
    
    #filter stores according to selections
    if len(store_select) == 0:
         pass
    elif len(store_select) > 0:
        df_metrics = df_metrics[df_metrics['Store Name'].isin(store_select)] 
    
    df_metrics.reset_index(inplace=True)
    df_metrics = df_metrics.drop(labels='index', axis=1)

    # Convert Date to a readable format
    df_metrics['Date'] = pd.to_datetime(df_metrics['Date']).dt.date
    

    #Total Revenue
    df['Net Revenue'] = pd.to_numeric(df['Net Revenue'])
    df_total_rev_group = df.groupby([option])['Net Revenue'].sum().sort_index(ascending=False)
    df_total_rev = pd.DataFrame(df_total_rev_group)
    #Plot total revenue
    total_rev_fig = px.line(df_total_rev_group)
    total_rev_fig.update_layout(title_text='Total Revenue', title_x=0.5 )
    total_rev_fig.update_yaxes(title_text = 'Revenue')

    #Total Revenue Per store
    df_rev_store = pd.crosstab(df_metrics[option].sort_values(ascending=False), df_metrics['Store Name'], values=df_metrics['Net Revenue'], aggfunc='sum', ).sort_index(ascending=False)


    #New Customers
    df_nc = pd.crosstab(df_metrics[option], df_metrics['Store Name'], values=df_metrics['New Customer Count'], aggfunc='sum').sort_index(ascending=False)

    #Returning Customers
    df_ret = pd.crosstab(df_metrics[option], df_metrics['Store Name'], values=df_metrics['Returners Count'], aggfunc='sum').sort_index(ascending=False)

    #clicks
    df_visitors = pd.crosstab(df_metrics[option], df_metrics['Store Name'], values=(df_metrics['Visitors']), aggfunc='sum').sort_index(ascending=False)

    #Average spend
    # ERROR: df_average_spend = pd.crosstab(df_metrics[option], df_metrics['Store Name'], values=(df_metrics['Average Actual Price Payed']), aggfunc='mean').sort_index(ascending=False)

    #Negative Reviewed Products
    df_negative_prod = pd.crosstab(df_metrics[option], df_metrics['Store Name'], values=(df_metrics['Negative Revew Product Count']/df_metrics['Completed Orders']), aggfunc='sum').sort_index(ascending=False)

    #Overtime Orders
    df_overtime_order = pd.crosstab(df_metrics[option], df_metrics['Store Name'], values=(df_metrics['Overtime Order Count']/df_metrics['Completed Orders']), aggfunc='sum').sort_index(ascending=False)
    

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
    fig.update_layout(xaxis_rangeslider_visible=True)
    fig.update_yaxes(title_text = 'Revenue')


    #-------------------------
    

    st.title('Eleme Reports 饿了么报表')

    # Last Date on current DF
    last = df['Date'].sort_values(ascending=False).iloc[0:1].dt.strftime('%m/%d/%Y').to_string()
    st.info("Last date ends on: " + last.split(' ')[4])

    st.subheader('Total Revenue 收入')
    tot1, tot2 = st.beta_columns([2,8])
    with tot1:
        st.write(" ")
        st.write(" ") 
        st.write(" ")
        st.write(" ")
        st.write(df_total_rev.style.background_gradient(cmap=hg).format("{:,.0f}"))
    with tot2:
        st.plotly_chart(total_rev_fig, use_container_width=True)

   
    #plot total revenue per store
    st.subheader('Total Eleme Revenue per Store 收入/店')
    st.plotly_chart(fig, use_container_width=True)
    st.subheader('Total Eleme Revenue per Store 收入/店')
    st.write(df_rev_store.style.background_gradient(cmap=hg, axis=0).format("{:,.0f}"))

    st.subheader('New Customer Count 新顾客')
    st.write(df_nc.style.background_gradient(cmap=hg, axis=0).format("{:,.0f}"))

    st.subheader('Returners Count 老顾客')
    st.write(df_ret.style.background_gradient(cmap=hg, axis=0).format("{:,.0f}"))


    st.subheader('Visitors 进店数')
    st.write(df_visitors.style.background_gradient(cmap=rocket, axis=0).format("{:,.0f}"))

    st.subheader('Total Discount Rate 活动补贴')
    st.write(df_disc.style.background_gradient(cmap=rocket, axis=0).format("{:,.2f}"))

    st.subheader('New Customer Order Conversion 新顾客转化率')
    st.write(df_nc_con.style.background_gradient(cmap=hg, axis=0).format("{:,.2f}"))

    st.subheader('Total Conversion Rate （老新顾客）转化率')
    st.write(df_total_conv.style.background_gradient(cmap=hg, axis=0).format("{:,.2f}"))

    st.subheader('Average (Actual) Spend 实付人均消费')
    st.write('Error here')
    # ERROR st.write(df_average_spend.style.background_gradient(cmap=hg, axis=1).format("{:,.0f}"))


    st.subheader('Bad Reviewed Product Count 商品差评')
    st.write(df_negative_prod.style.background_gradient(cmap=hg, axis=1).format("{:,.2f}"))

    st.subheader('Late Orders 超时订单')
    st.write(df_overtime_order.style.background_gradient(cmap=hg, axis=1).format("{:,.2f}"))