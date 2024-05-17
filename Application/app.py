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

def get_recommendations(text, experience, language, employment_type, location, driving_license, education):
    if language == 'Swedish':
        prompt = f"{text}\n\nJag har en jobbannons och jag vill förbättra den baserat på vissa kriterier. Den ideala kandidaten för min jobbannons har följande egenskaper: {employment_type}, {experience}, {location}, {driving_license} och {education}. Kan du ge en översiktlig bedömning av jobbannonsen och kommentera specifika meningar, ord eller stycken som kan förbättras eller ändras för att bättre attrahera den ideala kandidaten? Skriv svaret på Svenska."
        system_message = "Du är en hjälpsam assistent."
    else:  # Default to English
        prompt = f"{text}\n\nI have a job posting and I want to improve it based on certain criteria. The ideal candidate for my job posting has the following characteristics: {employment_type}, {experience}, {location}, {driving_license} and {education}. Can you provide an overall assessment of the job posting and comment on specific sentences, words, or paragraphs that can be improved or changed to better attract the ideal candidate? Write the answer in English."
        system_message = "You are a helpful assistant."

    response = client.chat_completions.create(
        model="ft:gpt-3.5-turbo-0125:personal::9N4jESmA",  # Use your fine-tuned chat model
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500,
        temperature=0.7)
    return response.choices[0].message['content']

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

# Define pages
def main_page():
    st.title('CoRecruit AI')

    uploaded_file = st.file_uploader("Upload a job posting", type=['txt', 'docx'])

    if uploaded_file is not None:
        if st.button('Run'):
            # Process the text from the job posting
            text = read_file(uploaded_file)

            # Use the GPT API to recommend changes if text extraction is successful
            if text:
                recommendations = get_recommendations(text, experience, language, employment_type, location, driving_license, education)
                st.subheader("Recommendations:")
                st.write(recommendations)
            else:
                st.error("Failed to extract text from the uploaded file.")

    # About Us Section
    st.markdown("""
    <hr>
    <h2>About Us</h2>
    <p>Welcome to CoRecruit AI, a platform designed to help you refine your job postings and attract the ideal candidates.
    Our AI-driven recommendations ensure that your job ads are optimized for clarity, attractiveness, and relevance.</p>
    """, unsafe_allow_html=True)

def tutorial_page():
    st.title('Tutorial')
    st.write("""
    ### How to Use CoRecruit AI
    1. Upload your job posting in either .txt or .docx format.
    2. Adjust the parameters in the sidebar to match your ideal candidate's profile.
    3. Click 'Run' to get AI-generated recommendations for improving your job posting.
    """)

def faq_page():
    st.title('FAQ')
    st.write("""
    ### Frequently Asked Questions

    **Q: What file formats are supported?**
    A: We support .txt and .docx files.

    **Q: How does the AI provide recommendations?**
    A: The AI analyzes your job posting based on the criteria you set and suggests improvements to better attract your ideal candidate.

    **Q: Is my data secure?**
    A: Yes, we prioritize your data privacy and security. Your uploaded files and data are not stored or shared.
    """)

# Load CSS
load_css('styles.css')

# Top navigation with clickable titles
st.markdown("""
<nav style="display: flex; justify-content: space-around; background-color: #f0f0f0; padding: 10px;">
    <a href="?page=main" style="text-decoration: none; font-weight: bold;" onclick="loadPage('main'); return false;">Home</a>
    <a href="?page=tutorial" style="text-decoration: none; font-weight: bold;" onclick="loadPage('tutorial'); return false;">Tutorial</a>
    <a href="?page=faq" style="text-decoration: none; font-weight: bold;" onclick="loadPage('faq'); return false;">FAQ</a>
</nav>
<hr>
""", unsafe_allow_html=True)

# Render the selected page based on URL parameter
query_params = st.experimental_get_query_params()
page = query_params.get("page", ["main"])[0]

if page == "main":
    # Sidebar options only for the main page
    st.sidebar.title('Options')

    experience = st.sidebar.slider('Experience (years)', 0, 10)
    language = st.sidebar.selectbox('Language', ['English', 'Swedish'])
    employment_type = st.sidebar.selectbox('Employment Type', ['Full Time', 'Part Time'])
    location = st.sidebar.selectbox('On-site', ['Yes', 'No', 'Hybrid'])
    education = st.sidebar.selectbox('Education', ['Not applicable', 'Upper Secondary School', 'Higher Education'])
    driving_license = st.sidebar.checkbox('Driving License')
    
    main_page()
elif page == "tutorial":
    tutorial_page()
elif page == "faq":
    faq_page()

# JavaScript to handle navigation without page reload
st.markdown("""
<script type="text/javascript">
    function loadPage(page) {
        const urlParams = new URLSearchParams(window.location.search);
        urlParams.set('page', page);
        window.history.pushState({}, '', `${window.location.pathname}?${urlParams.toString()}`);
        window.dispatchEvent(new Event('popstate'));
    }
</script>
""", unsafe_allow_html=True)
