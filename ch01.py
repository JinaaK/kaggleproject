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
    
    tab1, tab2, tab3 = st.tabs(["order", "products", "category"])

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

        cnt_srs = order_product_aisles_dep['product_name'].value_counts().reset_index().head(20)
        cnt_srs.columns = ['product_name', 'frequency_count']
        st.table(cnt_srs)

    with tab3:
        st.header("BestSellers by department")

        result = order_product_aisles_dep.groupby(['department', 'product_name']).size().reset_index(name='frequency_count')
        result = result.sort_values(['department', 'frequency_count'], ascending=[True, False])

        
        option = st.selectbox('Which department?', departments['department'] )
        st.write(option)


        if option:
            df = result.loc[result['department'] == option, :]
            st.table(df.reset_index(drop=True))

        else:
            st.write("Please select a department.")
            




        



    

if __name__ == "__main__":
    main()
