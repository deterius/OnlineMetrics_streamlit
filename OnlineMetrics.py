import ElemeMetrics
import MeituanMetrics
import Home
import streamlit as st
from multiapp import MultiApp

st.set_page_config(layout="wide")

app = MultiApp()

app.add_app("Home", Home.app)
app.add_app("Eleme", ElemeMetrics.app)
app.add_app("Meituan", MeituanMetrics.app)
app.run()