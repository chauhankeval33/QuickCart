"""QuickCart tools - home page. Run from the starter_repo folder:  streamlit run app/app.py"""
import streamlit as st

st.set_page_config(page_title="QuickCart tools", page_icon="🛒")
st.title("QuickCart tools")
st.write("Pick a page in the left sidebar:")
st.markdown(
    "1. **Delivery estimator**: predicted delivery minutes for a new order.\n"
    "2. **Churn scorer**: upload customers, get churn probabilities and the top 10% riskiest.\n"
    "3. **Ticket triage**: paste a complaint, get category, sentiment, urgency and summary.")
