import pandas as pd

def eleme_cleaner(df_raw):
    print('Clean New Data')
    #Clean New data

    chc = df_raw.columns
    print('Setting Renaming columns')
    enc = {chc[0]:'Date',chc[1]:'Store Name',chc[2]:'Store ID',chc[3]:'City',chc[4]:'Operation Time',chc[5]:'Peak Time'
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
    print('Setting renamed columns')
    df_raw = df_raw.rename(columns=enc)
    # rename stores
    df_raw['Store Name'] = df_raw['Store Name'].replace({'兄弟烤肉Brothers Kebab  烤肉卷(古北家乐福店)': '6 Gubei', '兄弟烤肉Brothers Kebab  烤肉卷(南京西路店)':'5 TS', '兄弟烤肉Brothers Kebab  烤肉卷(淮海西路店)':'7 Magnolia','兄弟烤肉Brothers Kebab  烤肉卷(奉贤路店)': '2 Fengxian', '兄弟烤肉Brothers Kebab  烤肉卷(巨鹿路店)': '8 Julu','Brothers Kebab兄弟烤肉店(香港中路店)':'QD 1','兄弟烤肉Brothers Kebab  烤肉卷(长宁区店)':'4 Zunyi','兄弟烤肉Brothers Kebab  烤肉卷(南泉北路店)':'3 Pudong','兄弟烤肉Brothers Kebab 烤肉卷(长寿路店)':'9 CS','兄弟烤肉Brothers Kebab 烤肉卷(漕溪路店)':'10 CX'})
    #Add Weeks and Months
    print('Add weeks and months')

    # wb.reset_index(inplace=True)
    df_raw['Date'] = pd.to_datetime(df_raw['Date'])
    df_raw['Week'] = df_raw['Date'].dt.isocalendar().week
    df_raw['Month'] = df_raw['Date'].dt.month
    #Replace 53 week with week 0
    df_raw['Week'] = df_raw['Week'].replace([53],[0])

    #move Weeks and Month to the front of the df
    sec_col = df_raw.pop('Month')
    first_col = df_raw.pop('Week')
    df_raw.insert(0, 'Month', sec_col )
    df_raw.insert(0, 'Week', first_col)

    # Convert Date to a readable format
    df_raw['Date'] = pd.to_datetime(df_raw['Date']).dt.date

    return df_raw



def merger(uploaded, existing_df):
    #Merge with exisiting data
    print('Append new data')
    uploaded = existing_df.append(uploaded)
    #duplicates
    uploaded.drop_duplicates(subset=['Date','Store Name','Net Revenue','Gross Revenue'],inplace=True)
    return uploaded