import ElemeMetrics
import MeituanMetrics
import ElemeProducts
import Home
import Frequency
import streamlit as st
from multiapp import MultiApp

from PIL import Image

im = Image.open("img/favicon.ico")

st.set_page_config(
        page_title="Brothers Kebab Dashboard",
        page_icon='🦈',
        layout="wide",
    )

app = MultiApp()


password = st.sidebar.text_input('Password', type='password')
if st.sidebar.checkbox('Login'):
    if (password == 'BK2021'):
        app.add_app("Overview", Home.app)
        app.add_app("Eleme", ElemeMetrics.app)
        app.add_app("Meituan", MeituanMetrics.app)
        app.add_app('Eleme Products', ElemeProducts.app)
        app.add_app('Revenue Frequency', Frequency.app)
        st.title('Brothers Kebab')
        app.run()   
        
    else:
        st.warning('Username/Password Error')




# app.add_app("Overview", Home.app)
# app.add_app("Eleme", ElemeMetrics.app)
# app.add_app("Meituan", MeituanMetrics.app)
# app.run()

   


