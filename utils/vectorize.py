import streamlit as st
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

@st.cache_data
def vectorize_combined_to_cosine_mat(data):
    count_vect = CountVectorizer(encoding='utf-8')
    vectors = count_vect.fit_transform(data['combined'].values.astype('U'))
    cosine_sim_mat = cosine_similarity(vectors)
    return cosine_sim_mat
