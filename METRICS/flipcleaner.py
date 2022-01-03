import streamlit as st 
import pandas as pd
import numpy as np
import openpyxl

# to schedule new data
import time
import schedule

from flipLogin import Flip_Login_Fin_report

pd.set_option('display.max_columns', None)

df_old = pd.read_csv('data/flip/FlipCombined.csv', index_col=1)

st.write(df_old)

result = st.button('Click')
if result:
    Flip_Login_Fin_report()

st.write('up')

