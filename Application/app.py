import os
import streamlit as st
import openai

openai.api_key = st.secrets["OPENAI_API_KEY"]
import pdfplumber
from io import BytesIO


# Function to load CSS
def load_css(file_name):
    # Get the directory of the current script
    script_dir = os.path.dirname(__file__)

    # Construct the absolute path to the CSS file
    file_path = os.path.join(script_dir, file_name)

    with open(file_path) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def get_recommendations(text, gender, experience, age):
    prompt = f"{text}\n\nGiven that the ideal candidate is {gender}, {experience}, and {age}, how could this job posting be improved?"

    # Correct API call for version 1.0.0 and above
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}],
        max_tokens=500,
        temperature=0.7)

    # Accessing the completion text correctly
    return response['choices'][0]['message']['content'].strip()

# Function to read file
def read_file(file):
    if file.type == 'application/pdf':
        with pdfplumber.open(BytesIO(file.getvalue())) as pdf:
            return ' '.join(page.extract_text() for page in pdf.pages)
    else:
        return file.getvalue().decode()

# Load CSS
load_css('styles.css')

# Sidebar
st.sidebar.title('Options')

gender = st.sidebar.radio('Gender Preference', ['N/A', 'Male', 'Female', 'Non-binary'])
experience = st.sidebar.radio('Experience Preference', ['N/A', 'Entry Level', 'Mid Level', 'Experienced'])
age = st.sidebar.radio('Age', ['N/A', 'Young', 'Middle aged', 'Old'])

# Main Area
st.title('Job Posting Editor')

uploaded_file = st.file_uploader("Upload a job posting", type=['txt', 'pdf'])

if uploaded_file is not None:
    # Process the text from the job posting
    text = read_file(uploaded_file)

    # Use the GPT API to recommend changes
    recommendations = get_recommendations(text, gender, experience, age)
    st.write(recommendations)
