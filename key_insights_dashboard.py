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
    
    # product category and market
    market=st.sidebar.selectbox('Pick your Market',orders['Market'].unique())
    category = st.sidebar.multiselect('Pick your category',orders['Category'].unique())
    
    #filtering the dashboard using the Market and product category
    if market and category:  # Both market and category are selected
        filtered_data = orders[(orders["Market"].isin([market])) & (orders["Category"].isin(category))]
    elif market:  # Only market is selected
        filtered_data = orders[orders["Market"].isin([market])]
    elif category:  # Only category is selected
        # Retrieve subcategories belonging to the selected category
        subcategories = orders[orders["Category"].isin(category)]["Sub-Category"].unique().tolist()
        # Filter based on both category and its subcategories
        filtered_data = orders[(orders["Category"].isin(category)) | (orders["Sub-Category"].isin(subcategories))]
    else:
        filtered_data = orders.copy()  # Show all data if no selections are made



