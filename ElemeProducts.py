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

    st.title('PRODUCTS')