import ElemeMetrics
import MeituanMetrics
import Overview
import Frequency
import ElemeRetention
import Outliers
import streamlit as st
from multiapp import MultiApp

from PIL import Image




#Page config
im = Image.open("img/favicon-32x32.png")
logo = Image.open('img/brotherskebab.png')
st.set_page_config(
        page_title="Brothers Kebab Dashboard",
        page_icon=im,
        layout="wide",
    )



app = MultiApp()

st.sidebar.image(logo)
password = st.sidebar.text_input('Password', type='password')
if st.sidebar.checkbox('Login'):
    if (password == 'BK2021'):
        app.add_app("All - Overview", Overview.app)
        app.add_app("Eleme", ElemeMetrics.app)
        app.add_app("Retention Rates", ElemeRetention.app)
        app.add_app("Meituan", MeituanMetrics.app)
        app.add_app('Revenue Frequency', Frequency.app)
        app.add_app('Outliers', Outliers.app)
        st.title('Brothers Kebab')
        app.run()   
        
    else:
        st.warning('Username/Password Error')




# app.add_app("Overview", Home.app)
# app.add_app("Eleme", ElemeMetrics.app)
# app.add_app("Meituan", MeituanMetrics.app)
# app.run()

   


