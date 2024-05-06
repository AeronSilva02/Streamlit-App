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
    if market and category:  
        filtered_data = orders[(orders["Market"].isin([market])) & (orders["Category"].isin(category))]
    elif market:  
        filtered_data = orders[orders["Market"].isin([market])]
    elif category:  
        # Retrieve subcategories belonging to the selected category
        subcategories = orders[orders["Category"].isin(category)]["Sub-Category"].unique().tolist()
        # Filter based on both category and its subcategories
        filtered_data = orders[(orders["Category"].isin(category)) | (orders["Sub-Category"].isin(subcategories))]
    else:
        filtered_data = orders.copy() 

    #Charts for the Orders dataset
   
    #Sales by sub category
    st.subheader('Sales by Sub Category')
    grp=filtered_data.groupby(by=['Sub-Category'],as_index=False)['Sales'].sum()
    fig1=px.bar(grp,x='Sub-Category',y='Sales', height=600,width=700)
        
    st.plotly_chart(fig1)

    
    #Sales by ship mode
    st.subheader ('Sales by ship mode')
    fig2=px.box(filtered_data,x='Ship Mode', y='Sales',height=400,width=600)
    st.plotly_chart(fig2)


    #Profit by market
    st.subheader('Profit by Country')
    grp=filtered_data.groupby(by=['Country'],as_index=False)['Profit'].sum()
    fig3=px.bar(grp,x="Country",y="Profit")
    st.plotly_chart(fig3)





