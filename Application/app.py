import streamlit as st
import openai
import os

# Load your OpenAI API key from an environment variable or secret management system
openai.api_key = 'your-api-key'

# Function to load CSS
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Function to call the GPT-3 model
def get_recommendations(text, gender, experience, age):
    prompt = f"{text}\n\nGiven that the ideal candidate is {gender}, {experience}, and {age}, how could this job posting be improved?"

    response = openai.Completion.create(
      engine="text-davinci-002",
      prompt=prompt,
      temperature=0.5,
      max_tokens=150
    )

    return response.choices[0].text.strip()

# Load CSS
load_css('styles.css')

# Sidebar
st.sidebar.title('Options')

gender = st.sidebar.radio('Gender Preference', ['Male', 'Female', 'Non-binary'])
experience = st.sidebar.radio('Experience Preference', ['Entry Level', 'Mid Level', 'Experienced'])
age = st.sidebar.radio('Age', ['Young', 'Middle aged', 'Old'])

# Main Area
st.title('Job Posting Editor')

uploaded_file = st.file_uploader("Upload a job posting", type=['txt', 'pdf'])

if uploaded_file is not None:
    # Process the text from the job posting
    text = uploaded_file.read().decode()

    # Use the GPT API to recommend changes
    recommendations = get_recommendations(text, gender, experience, age)
    st.write(recommendations)