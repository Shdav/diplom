import streamlit as st
from utils import load_data, vectorize_combined_to_cosine_mat, recommend, set_query
from random import randint

def product_page():
    query_params = st.experimental_get_query_params()
    product_id = query_params.get('product_id', [None])[0]
    search_query = query_params.get('q', [''])[0]
    category_query = query_params.get('category', [])
    manufacturer_query = query_params.get('manufacturer', [])
    page = int(query_params.get('page', [1])[0])
    is_available_query = bool(query_params.get('is_available', [False])[0])
    rating_query = int(query_params.get('rating', [3])[0])
    toys = load_data('./toys.csv')
    selected_toy = toys[toys['id'] == int(product_id)].iloc[0]

    if selected_toy is not None:
        similarity = vectorize_combined_to_cosine_mat(toys)
        recommended_toys = recommend(toys, selected_toy['product_name'], similarity)
        if st.button('Назад', key='back'):
            set_query(None, search_query, page, category_query, manufacturer_query, is_available_query, rating_query)
            st.experimental_rerun()
        st.header(selected_toy['product_name'])
        st.subheader('Описание')
        st.write(selected_toy['description'])

        st.subheader('Категория')
        st.write(selected_toy['amazon_category_and_sub_category'])

        st.subheader('Производитель')
        st.write(selected_toy['manufacturer'])

        st.subheader('Цена')
        st.write(f"£{selected_toy['price']}")

        st.subheader('Доступное количество на складе')
        st.write(selected_toy['number_available_in_stock'])

        st.subheader('Количество отзывов')
        st.write(selected_toy['number_of_reviews'])

        st.subheader('Количество вопросов')
        st.write(selected_toy['number_of_answered_questions'])

        st.subheader('Средний рейтинг отзывов')
        st.write(selected_toy['average_review_rating'])

        with st.expander('Похожие товары', expanded=False):
            for id in recommended_toys:
                product_name = toys.loc[toys['id'] == id, 'product_name'].values[0] if toys['id'].eq(id).any() else None
                if product_name is not None:
                    if st.button(product_name, key=id):
                        set_query(id, search_query, page, category_query, manufacturer_query, is_available_query, rating_query)
                        st.rerun()
    else:
        st.write('Товар не найден')

if __name__ == "__main__":
    product_page()