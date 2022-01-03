import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import openpyxl
from PIL import Image
from openpyxl.reader.excel import load_workbook
from openpyxl.workbook import Workbook

# Import functions
from helper_func import *

st.title('Eleme Cleaner')

df_old = pd.read_csv('data/df_old.csv', encoding='gb2312')
global df
#-------UPLOAD FILE and covert to CSV -------
st.subheader('Upload New Eleme Data')
uploaded_file = st.file_uploader(label='Eleme: XLSX file', type=['csv','xlsx'])

if uploaded_file is not None:
    df_uploaded = pd.read_excel(uploaded_file)
    # check the len of uploaded file, if wrong throw error
    if len(df_uploaded.columns) == 63:
        #clean the uploaded file
        df_cleaned = eleme_cleaner(df_uploaded)
        today = pd.to_datetime("today")
        today = today.strftime("%Y-%m-%d")
        df_cleaned.to_csv('data/uploaded-eleme-'+ today +'.csv', index=False, header=True, encoding='gb2312')

        df = merger(df_cleaned, df_old)
    else:
        st.warning('Wrong file attached')
        

# Backup old df and replace with the new merged one
if df is not None:
    today = pd.to_datetime("today")
    today = today.strftime("%Y-%m-%d")
    df_old.to_csv('data/backups/eleme_df_backup-'+ today +'.csv', index=False, header=True, encoding='gb2312')
    df.to_csv('data/df_old.csv', index=False, header=True, encoding='gb2312')


st.write(df_old)
st.write(df)