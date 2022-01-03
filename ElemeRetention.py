import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import plotly
import plotly.express as px
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 12})
import openpyxl
from PIL import Image

def app():
    df = pd.read_csv('cohortsdata/flipElemeOrdersMerged.csv')
    #Select Store
    filter_stores = st.sidebar.checkbox('Filter Stores')
    df = df[df['门店名称'] != 'QD 1']
    

    

    #filter df with store
    if filter_stores:
        sorted_stores = sorted(df['门店名称'].unique())
        selected_stores = st.sidebar.radio(label='Store', options=sorted_stores)
        df = df[df['门店名称'] == selected_stores]
    #replace week 53
    df['Week'] = df['Week'].replace({53:0})

    #--- cohorts WEEKS
    df['InvoiceWeek'] = df['Week']
    grouping = df.groupby('Address')['InvoiceWeek']

    df['CohortWeek'] = grouping.transform('min')
    weeks_diff =df['InvoiceWeek'] - df['CohortWeek'] 
    df['CohortIndex'] =  weeks_diff

    grouping2 = df.groupby(['CohortWeek','CohortIndex'])
    cohort_data = grouping2['Address'].apply(pd.Series.nunique).reset_index()
    cohort_counts = cohort_data.pivot(index='CohortWeek',columns='CohortIndex', values='Address')
    cohort_sizes = cohort_counts.iloc[:,0]

    retention = cohort_counts.divide(cohort_sizes, axis=0)

    #----- plot WEEKS
    ret = plt.figure(figsize=(18,14))
    plt.rcParams['font.size'] = '8'
    plt.title('Retention Rates (Weeks)', fontsize = 20)
    sns.heatmap(data=retention, annot=True, fmt='.0%', vmin=0.0, vmax=0.3, cmap='BuGn')
    plt.xlabel('Duration (Weeks) from 1st purchase', fontsize = 20)
    plt.ylabel('Weeks of 1st purchase', fontsize = 20)
    plt.show()

    #--- cohorts MONTHS
    df['InvoiceMonth'] = df['Month']
    grouping_m = df.groupby('Address')['InvoiceMonth']

    df['CohortMonth'] = grouping_m.transform('min')
    months_diff =df['InvoiceMonth'] - df['CohortMonth'] 
    df['CohortIndex'] =  months_diff

    grouping_m2 = df.groupby(['CohortMonth','CohortIndex'])
    cohort_data_m = grouping_m2['Address'].apply(pd.Series.nunique).reset_index()
    cohort_counts_m = cohort_data_m.pivot(index='CohortMonth',columns='CohortIndex', values='Address')
    cohort_sizes_m = cohort_counts_m.iloc[:,0]

    retention_m = cohort_counts_m.divide(cohort_sizes_m, axis=0)

    #----- plot MONTH
    # Last Date on current DF
    df['Date'] = pd.to_datetime(df['Date'])
    last = df['Date'].sort_values(ascending=False).iloc[0:1].dt.strftime('%m/%d/%Y').to_string()
    st.info("Last date ends on: " + last.split(' ')[4])
    st.title('Eleme Retention Rates')
    ret_m = plt.figure(figsize=(12,8))
    plt.title('Retention Rates (MONTHS)', fontsize = 12)
    sns.heatmap(data=retention_m, annot=True, fmt='.0%', vmin=0.0, vmax=0.5, cmap="flare")
    plt.xlabel('Duration (MONTHS) from 1st purchase', fontsize = 12)
    plt.ylabel('Months of 1st purchase', fontsize = 12)
    plt.show()

    st.pyplot(ret_m)
    st.pyplot(ret)
