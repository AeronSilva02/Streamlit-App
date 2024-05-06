import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

#reading csv files
orders=pd.read_csv('orders_cleaned.csv')
rules=pd.read_csv('association_rules.csv')

st.title('Key Insights Dashboard')
col1,col2=st.columns((2))
#Adding dashboard filter
st.sidebar.title("Dashboard Filters")



#making tabs
Order_details, association_rules=st.tabs(['Order Details','Market Basket Analysis Association Rules'])
with Order_details:
    st.header("Order Details")
    st.write(orders)
    #date picker
    orders['Order Date']=pd.to_datetime(orders['Order Date'])
    start_date=pd.to_datetime(orders['Order Date']).min()
    end_date=pd.to_datetime(orders['Order Date']).max()

    start=pd.to_datetime(st.sidebar.date_input('Pick start date',start_date))
    end=pd.to_datetime(st.sidebar.date_input('Pick end date',end_date))
    orders=orders[(orders['Order Date']>= start) & (orders['Order Date']<=end)].copy()
