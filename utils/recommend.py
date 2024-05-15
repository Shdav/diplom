import streamlit as st
import numpy as np

@st.cache_data
def recommend(toys, toy, similarity):
    weight_similarity=0.8
    weight_price=0.1
    weight_reviews=0.1

    if toy in toys['product_name'].values:
        toy_index = toys[toys['product_name'] == toy].index[0]
        distances = similarity[toy_index]

        # Invert distances to similarity scores and normalize them
        max_similarity = max(distances)
        normalized_similarity = [d / max_similarity for d in distances]

        # Calculate scaled scores for price and number of reviews
        max_price = toys['price'].max()
        scaled_prices = 1 - (toys['price'] / max_price).values  # Convert Series to numpy array

        max_reviews = toys['number_of_reviews'].max()
        scaled_reviews = (toys['number_of_reviews'] / max_reviews).values  # Convert Series to numpy array

        # Combine similarity scores and feature scores with weights
        if len(normalized_similarity) == len(scaled_prices) == len(scaled_reviews):
            combined_scores = (weight_similarity * np.array(normalized_similarity) +
                               weight_price * np.array(scaled_prices) +
                               weight_reviews * np.array(scaled_reviews))
        else:
            return "Lengths of arrays are not consistent"

        # Find indices of top similar toys
        toy_list = sorted(list(enumerate(combined_scores)), reverse=True, key=lambda x: x[1])[0:15]

        similar_toys_indices = [index for index, _ in toy_list]
        print(toy_list)
        return similar_toys_indices
    else:
        return "Toy not found in the dataset"
