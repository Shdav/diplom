import streamlit as st
from utils import load_data, set_query
from product import product_page
import math

def catalog_page():
    toys = load_data('./toys.csv')
    query_params = st.experimental_get_query_params()
    product_id = query_params.get('product_id', [None])[0]
    search_query = query_params.get('q', [''])[0]
    category_query = query_params.get('category', [])
    manufacturer_query = query_params.get('manufacturer', [])
    page = int(query_params.get('page', [1])[0])
    is_available_query = bool(query_params.get('is_available', [False])[0])
    rating_query = int(query_params.get('rating', [3])[0])
    set_query(product_id, search_query, page, category_query, manufacturer_query, is_available_query, rating_query)

    if product_id:
        product_page()
        return

    st.header('Каталог')
    search = st.sidebar.text_input("Название", value=search_query)

    if search != search_query:
        set_query(product_id, search, 1, category_query, manufacturer_query, is_available_query, rating_query)
        st.experimental_rerun()

    search_toys = toys.copy()

    if category_query != []:
        category = st.sidebar.multiselect(label='Категория', options=list(set(search_toys['amazon_category_and_sub_category'].unique()) | set(category_query)), default=category_query)
    else:
        category = st.sidebar.multiselect(label='Категория', options=search_toys['amazon_category_and_sub_category'].unique())

    if category != category_query:
        set_query(product_id, search_query, 1, category, manufacturer_query, is_available_query, rating_query)
        st.experimental_rerun()

    if manufacturer_query != []:
        manufacturer = st.sidebar.multiselect(label='Производитель', options=list(set(search_toys['manufacturer'].unique()) | set(manufacturer_query)), default=manufacturer_query)
    else:
        manufacturer = st.sidebar.multiselect(label='Производитель', options=search_toys['manufacturer'].unique())
    if manufacturer != manufacturer_query :
        set_query(product_id, search_query, 1, category_query, manufacturer, is_available_query, rating_query)
        st.experimental_rerun()

    def on_change(is_available_value):
        set_query(product_id, search_query, 1, category_query, manufacturer, not is_available_value, rating_query)
    is_available = st.sidebar.checkbox(label='В наличии', value=is_available_query, on_change=on_change, args=(is_available_query,))

    rating = st.sidebar.radio('Рейтинг', options=['5', '4', '3'], index=min(max(5 - rating_query, 0), 2))
    if int(rating) != rating_query:
        set_query(product_id, search_query, 1, category_query, manufacturer_query, is_available, rating)
        st.experimental_rerun()

    if search_query:
        search_toys = search_toys[search_toys['product_name'].str.contains(search_query, case=False)]
    if category_query != []:
        search_toys = search_toys[search_toys['amazon_category_and_sub_category'].isin(category_query)]
    if manufacturer_query != []:
        search_toys = search_toys[search_toys['manufacturer'].isin(manufacturer_query)]
    if is_available_query == True:
        search_toys = search_toys[search_toys['number_available_in_stock'] > 0]
    if rating_query:
        search_toys = search_toys[search_toys['average_review_rating'] >= int(rating_query)]

    total_toys = search_toys.shape[0]
    st.write(f'Страница {min(page, math.ceil(total_toys/10))} из {math.ceil(total_toys/10)}')
    clear = st.sidebar.button('Очистить')
    if clear:
        st.experimental_set_query_params()
        st.experimental_rerun()

    if not search_toys.empty:
        for index, row in search_toys.iloc[(page-1)*10:page*10].iterrows():
            with st.container():
                st.write(row['product_name'])
                st.write(f"£{row['price']}")
                if st.button('Подробнее', key=row['id']):
                    st.write(str(row['id']))
                    set_query(str(row['id']), search_query, page, category_query, manufacturer_query, is_available, rating_query)
                    st.experimental_rerun()

        if page > 1:
            prev_button = st.button('Предыдущая страница')
            if prev_button:
                set_query(product_id, search_query, page-1, category_query, manufacturer_query, is_available, rating_query)
                st.experimental_rerun()

        if total_toys > page * 10:
            next_button = st.button("Следующая страница")
            if next_button:
                set_query(product_id, search_query, page+1, category_query, manufacturer_query, is_available, rating_query)
                st.experimental_rerun()
    else:
        st.write('Товары по вашему запросу не найдены')

if __name__ == "__main__":
    catalog_page()
