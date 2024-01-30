# -*- coding:utf-8 -*-
import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns
import pandas as pd


data_path = 'data/'

@st.cache_data
def load_data():
    aisles = pd.read_csv(data_path + 'aisles.csv')
    departments = pd.read_csv(data_path + 'departments.csv')
    product_prior = pd.read_csv(data_path + 'order_products__prior.csv')
    product_train = pd.read_csv(data_path + 'order_products__train.csv')
    orders = pd.read_csv(data_path + 'orders.csv')
    products = pd.read_csv(data_path + 'products.csv')

    return aisles, departments, product_prior, product_train, orders, products

def main():

    aisles, departments, product_prior, product_train, orders, products = load_data()
    
    tab1, tab2 = st.tabs(["order", "products"])

    with tab1:
        st.header("When do people order?")

        fig,ax = plt.subplots()
        sns.histplot(orders['order_hour_of_day'], kde=False, ax = ax)
        st.pyplot(fig)

    with tab2:
        st.header("BestSellers")

        # st.table(product_prior.head(5))
        # st.table(products.head(5))

        order_product = pd.merge(product_prior, products, on = 'product_id', how='left')
        #st.table(order_product.head(5))
        order_product_aisles = pd.merge(order_product, aisles, on = 'aisle_id', how = 'left')
        order_product_aisles_dep = pd.merge(order_product_aisles, departments, on='department_id', how='left')
        # st.table(order_product_aisles_dep.head(3))

        cnt_srs = order_product_aisles_dep['product_name'].value_counts().reset_index().head(20)
        cnt_srs.columns = ['product_name', 'frequency_count']
        st.table(cnt_srs)

if __name__ == "__main__":
    main()
