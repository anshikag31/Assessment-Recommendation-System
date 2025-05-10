import streamlit as st
import requests
import pandas as pd
import numpy as np

# Title
st.set_page_config(page_title="SHL Assessment Recommender", layout="centered")
st.title("🔍 SHL Assessment Recommendation Engine")

# Input area
query = st.text_area("Enter Job Description or Query", height=200)

# Submit button
if st.button("Get Recommendations"):
    if not query.strip():
        st.warning("Please enter a valid job description or query.")
    else:
        # Call your API endpoint
        try:
            response = requests.post(
                "https://assessment-recommendation-system-3p5c.onrender.com/recommend",  # change this to your deployed API URL if needed
                json={"query": query}
            )
            if response.status_code == 200:
                data = response.json()["recommended_assessments"]  # Updated to match the response structure

                # Convert to DataFrame
                df = pd.DataFrame(data)

                # Clean 'Duration (mins)' column to handle non-numeric values
                df['duration'] = pd.to_numeric(df['duration'], errors='coerce')  # Convert to numeric, invalid values become NaN
                df['duration'] = df['duration'].fillna(0)
  # Replace NaN with 0 or a default value of your choice

                # Use description as the assessment name
                df["Assessment Name"] = df.apply(
                    lambda x: f"[{x.get('description', 'No Name')}]({x.get('url', '#')})", axis=1
                )

                # Display selected columns
                st.markdown("### 🔗 Top Recommendations")
                st.write(
                    df[["Assessment Name", "test_type", "duration", "remote_support", "adaptive_support"]]
                    .rename(columns={
                        "test_type": "Test Type",
                        "duration": "Duration (mins)",
                        "remote_support": "Remote Testing",
                        "adaptive_support": "Adaptive/IRT"
                    }),
                    unsafe_allow_html=True
                )
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"Failed to reach backend API. Error: {e}")
