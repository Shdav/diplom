import streamlit as st

def set_query(product_id, q, page, category, manufacturer, is_available, rating):
    active_query_params = {}
    if product_id is not None:
        active_query_params['product_id'] = product_id
    if q is not None and q != '':
        active_query_params['q'] = q
    if page > 1:
        active_query_params['page'] = page
    if category is not []:
        active_query_params['category'] = category
    if manufacturer is not []:
        active_query_params['manufacturer'] = manufacturer
    if is_available == True:
        active_query_params['is_available'] = is_available
    if int(rating) > 0:
        active_query_params['rating'] = rating

    st.experimental_set_query_params(**active_query_params)
