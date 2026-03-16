import streamlit as st
import pickle

# Load model and vectorizer
model = pickle.load(open("model.pkl","rb"))
vectorizer = pickle.load(open("vectorizer.pkl","rb"))

# Page title
st.set_page_config(page_title="IMDb Sentiment Analyzer", page_icon="🎬")

st.title("🎬 IMDb Movie Review Sentiment Analyzer")

st.write("Enter a movie review and the model will predict whether it is Positive or Negative.")

# Text input
review = st.text_area("Enter Movie Review")

# Prediction button
if st.button("Analyze Sentiment"):

    if review.strip() == "":
        st.warning("Please enter a review.")
    else:
        # Transform text
        vector = vectorizer.transform([review])

        # Predict
        prediction = model.predict(vector)[0]

        if prediction == 1:
            st.success("Positive Review 😊")
        else:
            st.error("Negative Review 😞")