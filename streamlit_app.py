import streamlit as st
from main import FashionAgent
from PIL import Image
import os

# Initialize Fashion AI Agent
agent = FashionAgent()

# Streamlit UI
st.set_page_config(page_title="Fashion AI", page_icon="👗", layout="wide")

st.title("👗 Fashion AI: Outfit Matcher")
st.write("Upload an outfit image to get AI-powered fashion recommendations!")

# File Uploader
uploaded_file = st.file_uploader("Upload an outfit image (JPG/PNG)", type=["jpg", "png"])

if uploaded_file is not None:
    # Display Uploaded Image with controlled size
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Outfit", width=300)  # Adjust width as needed

    # Save image temporarily
    image_path = "temp_outfit.jpg"
    image.save(image_path)

    # Generate Recommendations
    with st.spinner("Analyzing outfit..."):
        recommendations = agent.analyze_outfit(image_path)

    # Format recommendations as a list
    formatted_recommendations = recommendations.split("\n")  # Split by newline for better formatting

    # Debugging Print
    print(f"\n----- Formatted AI Recommendations -----\n")
    print(formatted_recommendations)

    # Display Recommendations
    st.subheader("✨ AI Recommendations")
    for rec in formatted_recommendations:
        if rec.strip():  # Avoid empty lines
            st.markdown(f"- **{rec.strip()}**")  # Bold text for better readability

    # Remove temp file
    os.remove(image_path)
