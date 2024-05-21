import os
import streamlit as st
from openai import OpenAI
from io import BytesIO
from docx import Document
import base64
import tiktoken

# Initialize OpenAI client with the API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Function to load CSS
def load_css(file_name):
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the absolute path to the CSS file
    file_path = os.path.join(script_dir, file_name)

    with open(file_path) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load the CSS
load_css('styles.css')

# Function to read the context file
def read_context(file_name):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, file_name)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

# Read the context from the text file
context_text = read_context('context.txt')

# Function to count tokens
def count_tokens(text):
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    return len(encoding.encode(text))

# Function to truncate text
def truncate_text(text, max_tokens):
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    tokens = encoding.encode(text)
    if len(tokens) > max_tokens:
        tokens = tokens[:max_tokens]
    return encoding.decode(tokens)

def get_recommendations(text, context, experience, language, employment_type, location, driving_license, education):
    # Max tokens for the prompt
    max_tokens = 16385 - 1000  # Keeping some buffer for response and system message
    
    combined_text = f"{context}\n\n{text}"
    if count_tokens(combined_text) > max_tokens:
        # Truncate context and text if they exceed max_tokens
        context_tokens = max_tokens // 2
        text_tokens = max_tokens - context_tokens
        context = truncate_text(context, context_tokens)
        text = truncate_text(text, text_tokens)
    
    if language == 'Swedish':
        prompt = f"{context}\n\n{text}\n\nJag har en jobbannons och jag vill förbättra den baserat på vissa kriterier. Den ideala kandidaten för min jobbannons har följande egenskaper: {employment_type}, {experience}, {location}, {driving_license} och {education}. Kan du ge en översiktlig bedömning av jobbannonsen och kommentera specifika meningar, ord eller stycken som kan förbättras eller ändras för att bättre attrahera den ideala kandidaten? Skriv svaret på Svenska."
        system_message = "Du är en hjälpsam assistent."
    else:  # Default to English
        prompt = f"{context}\n\n{text}\n\nJag har en jobbannons och jag vill förbättra den baserat på vissa kriterier. Den ideala kandidaten för min jobbannons har följande egenskaper: {employment_type}, {experience}, {location}, {driving_license} och {education}. Kan du ge en översiktlig bedömning av jobbannonsen och kommentera specifika meningar, ord eller stycken som kan förbättras eller ändras för att bättre attrahera den ideala kandidaten? Skriv svaret på Engelska."
        system_message = "You are a helpful assistant."

    response = client.chat.completions.create(model="ft:gpt-3.5-turbo-0125:personal::9N4jESmA",
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

# Function to convert image to base64
def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

# Convert logo to base64
logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo_transparent.png")
logo_base64 = image_to_base64(logo_path)

# Main page content
st.markdown(
    f"""
    <div style="display: flex; align-items: center;">
        <img src="data:image/png;base64,{logo_base64}" style="height: 120px; margin-right: 15px;">
        <h1 style="display: inline;">CoRecruit AI</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# Display the logo in the sidebar
st.sidebar.markdown(
    f"""
    <div style="display: flex; align-items: center;">
        <img src="data:image/png;base64,{logo_base64}" style="height: 120px; margin-right: 15px;">
        <h1 style="display: inline;">CoRecruit AI</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# Sidebar options
st.sidebar.title('Options')
language = st.sidebar.selectbox('AI Response Language', ['English', 'Swedish'])
employment_type = st.sidebar.selectbox('Employment Type', ['Full Time', 'Part Time'])
experience = st.sidebar.selectbox('Experience', ['Not applicable', '0-1 years','1-3 years','3-5 years','5-10 years','10+ years'])
location = st.sidebar.selectbox('On-site', ['Yes', 'No', 'Hybrid'])
education = st.sidebar.selectbox('Education', ['Not applicable', 'Upper Secondary School', 'Higher Education'])
driving_license = st.sidebar.checkbox('Driving License')

uploaded_file = st.file_uploader("", type=['txt', 'docx'], label_visibility="hidden")

if uploaded_file is not None:
    if st.button('Run'):
        # Process the text from the job posting
        text = read_file(uploaded_file)

        # Use the GPT API to recommend changes if text extraction is successful
        if text:
            recommendations = get_recommendations(text, context_text, experience, language, employment_type, location, driving_license, education)
            st.subheader("Recommendations:")
            st.write(recommendations)
        else:
            st.error("Failed to extract text from the uploaded file.")

# Add some space
st.markdown('&nbsp;', unsafe_allow_html=True)
# Add some space
st.markdown('&nbsp;', unsafe_allow_html=True)
# Add some space
st.markdown('&nbsp;', unsafe_allow_html=True)

# Add some space and a downward arrow
st.markdown("""
&nbsp;
&nbsp;
&nbsp;
<div style='text-align: center;'><span style='font-size:50px;'>&#8595;</span></div>
&nbsp;
""", unsafe_allow_html=True)

st.header('Tutorial')
st.write("""
1. Upload your job posting in either .txt or .docx format.
2. Adjust the parameters in the sidebar to match your ideal candidate's profile.
3. Click 'Run' to get AI-generated recommendations for improving your job posting.
""")

st.header('FAQ')
st.write("""
**Q: What file formats are supported?**
A: We support .txt and .docx files.

**Q: How does the AI provide recommendations?**
A: The AI analyzes your job posting based on the criteria you set and suggests improvements to better attract your ideal candidate.

**Q: Is my data secure?**
A: Yes, we prioritize your data privacy and security. Your uploaded files and data are not stored or shared.
""")

st.header('About Us')
st.markdown("""
<p>Welcome to CoRecruit AI, a platform designed to help you refine your job postings and attract the ideal candidates.
Our AI-driven recommendations ensure that your job ads are optimized for clarity, attractiveness, and relevance.</p>
<h3>Our Team</h3>
<ul>
    <li>Brandon Nilsson (<a href="https://www.linkedin.com/in/b-nilsson/" target="_blank">LinkedIn</a>)</li>
    <li>Jakob Delin (<a href="https://www.linkedin.com/in/jakob-delin-3b186430a/" target="_blank">LinkedIn</a>)</li>
    <li>Molly Korse (<a href="https://www.linkedin.com/in/molkor/" target="_blank">LinkedIn</a>)</li>
    <li>Peter Markus (<a href="https://www.linkedin.com/in/kedinpetmark/" target="_blank">LinkedIn</a>)</li>
    <li>Tobias Magnusson (<a href="https://www.linkedin.com/in/tobias-magnusson-333650194/" target="_blank">LinkedIn</a>)</li>
</ul>
<p>Check out our GitHub repository: <a href="https://github.com/BarreBN/CoRecruit.git" target="_blank">CoRecruit</a></p>
""", unsafe_allow_html=True)
