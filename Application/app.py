import os
import streamlit as st
from openai import OpenAI
from io import BytesIO
from docx import Document

# Initialize OpenAI client with the API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Function to load CSS
def load_css(file_name):
    # Get the directory of the current script
    script_dir = os.path.dirname(__file__)

    # Construct the absolute path to the CSS file
    file_path = os.path.join(script_dir, file_name)

    with open(file_path) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load the CSS
load_css('styles.css')

def get_recommendations(text, gender, experience, age, language, employment_type, location, driving_license, education):
    if language == 'Swedish':
        prompt = f"{text}\n\nJag har en jobbannons och jag vill förbättra den baserat på vissa kriterier. Den ideala kandidaten för min jobbannons har följande egenskaper: {employment_type}, {experience}, {location}, {driving_license} och {education}. Kan du ge en översiktlig bedömning av jobbannonsen och kommentera specifika meningar, ord eller stycken som kan förbättras eller ändras för att bättre attrahera den ideala kandidaten? Skriv svaret på Svenska."
        system_message = "Du är en hjälpsam assistent."
    else:  # Default to English
        prompt = f"{text}\n\nJag har en jobbannons och jag vill förbättra den baserat på vissa kriterier. Den ideala kandidaten för min jobbannons har följande egenskaper: {employment_type}, {experience}, {location}, {driving_license} och {education}. Kan du ge en översiktlig bedömning av jobbannonsen och kommentera specifika meningar, ord eller stycken som kan förbättras eller ändras för att bättre attrahera den ideala kandidaten? Skriv svaret på Engelska."
        system_message = "You are a helpful assistant."

    response = client.chat.completions.create(
        model="ft:gpt-3.5-turbo-0125:personal::9N4jESmA",  # Use your fine-tuned chat model
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500,
        temperature=0.7)
    return response.choices[0].message.content

# Function to read file
def read_file(file):
    if file.type == 'text/plain':
        try:
            return file.getvalue().decode()
        except Exception as e:
            st.error(f"Error reading text file: {e}")
            return ""
    elif file.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        try:
            doc = Document(BytesIO(file.getvalue()))
            return '\n'.join([para.text for para in doc.paragraphs])
        except Exception as e:
            st.error(f"Error reading DOCX file: {e}")
            return ""
    else:
        st.error("Unsupported file type.")
        return ""

# Load CSS
load_css('styles.css')

# Sidebar
st.sidebar.title('Options')

# Add a language selection option
language = st.sidebar.radio('Language', ['English', 'Swedish'])

employment_type = st.sidebar.radio('Employment Type', ['N/A', 'Full time', 'Part time'])
experience = st.sidebar.radio('Experience Preference', ['N/A', 'Entry Level', 'Mid Level', 'Experienced'])
location = st.sidebar.radio('Location', ['N/A', 'On-Site', 'Hybrid', 'Remote'])
driving_license = st.sidebar.radio('Driving License', ['N/A', 'Required', 'Not Required'])
education = st.sidebar.radio('Education', ['N/A', 'Gymnasial', 'Eftergymnasial/Universitet'])

# Main Area
st.title('CoRecruit AI')

uploaded_file = st.file_uploader("Upload a job posting", type=['txt', 'docx'])

if uploaded_file is not None:
    if st.button('Run'):
        # Process the text from the job posting
        text = read_file(uploaded_file)

        # Use the GPT API to recommend changes if text extraction is successful
        if text:
            recommendations = get_recommendations(text, gender, experience, age, language, employment_type, location, driving_license, education)
            st.subheader("Recommendations:")
            st.write(recommendations)
        else:
            st.error("Failed to extract text from the uploaded file.")
