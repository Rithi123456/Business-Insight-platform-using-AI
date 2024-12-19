import os
import streamlit as st
import google.generativeai as genai
import base64
from PIL import Image
import smtplib
from email.mime.text import MIMEText
import speech_recognition as sr
import googletrans
from googletrans import Translator

# Configure Gemini API
genai_api_key = 'AIzaSyC4NuVn03-OSV2C9OprFChupLmV7Azoq4I'
genai.configure(api_key=genai_api_key)

# Check if user is already logged in (session state)
if 'user_logged_in' not in st.session_state:
    st.session_state.user_logged_in = False

# Sample users data (for demo purposes, you can replace it with a database or file storage in a real-world scenario)
users_db = {}

# Function to save user preferences
def save_user_preferences(industry, user_query):
    st.session_state.user_industry = industry
    st.session_state.user_query_history.append(user_query)

# Login page
def login_page():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if username in users_db and users_db[username] == password:
            st.session_state.user_logged_in = True
            st.session_state.username = username
            st.success("Login successful!")
        else:
            st.error("Invalid username or password")

# Signup page
def signup_page():
    st.title("Sign Up")
    username = st.text_input("Choose a Username")
    password = st.text_input("Choose a Password", type="password")
    
    if st.button("Sign Up"):
        if username not in users_db:
            users_db[username] = password
            st.session_state.user_logged_in = True
            st.session_state.username = username
            st.success("Sign-up successful!")
        else:
            st.error("Username already exists!")

# User Dashboard
def user_dashboard():
    st.title(f"Welcome, {st.session_state.username}!")
    
    # User Preferences
    st.subheader("Your Preferences")
    st.write(f"Selected Industry: {st.session_state.user_industry}")
    
    # Display User's Query History
    st.subheader("Your Query History")
    for i, query in enumerate(st.session_state.user_query_history):
        st.write(f"{i+1}. {query}")
    
    # Option to logout
    if st.button("Logout"):
        st.session_state.user_logged_in = False
        st.session_state.clear()
        st.success("Logged out successfully!")

# Initialize user query history in session state
if 'user_query_history' not in st.session_state:
    st.session_state.user_query_history = []

# Function to upload the image to Gemini
def upload_to_gemini(path, mime_type=None):
    """Uploads the given file to Gemini."""
    file = genai.upload_file(path, mime_type=mime_type)
    return file

# Function to send a chat message to Gemini
def get_gemini_response(image_file, user_query):
    # Upload image to Gemini
    file = upload_to_gemini(image_file, mime_type="image/jpeg")

    # Create model config
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        generation_config=generation_config,
    )

    # Create chat session
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    file,
                    user_query,
                ],
            },
        ]
    )

    # Send the user query and get the response
    response = chat_session.send_message(user_query)
    return response.text

# Function to send email
def send_email(text, recipient_email):
    msg = MIMEText(text)
    msg['Subject'] = 'Your AI Business Insight'
    msg['From'] = 'your_email@example.com'
    msg['To'] = recipient_email

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login('your_email@example.com', 'your_password')
        server.sendmail('your_email@example.com', recipient_email, msg.as_string())

# Function to convert speech to text
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Say something...")
        audio = recognizer.listen(source)
        try:
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            st.error("Could not understand audio.")
            return ""
        except sr.RequestError:
            st.error("Could not request results from Google Speech Recognition service.")
            return ""

# Function to predict trends
def predict_trends(image_data):
    return "The AI predicts a steady growth in sales for the next quarter based on the data."

# Function to get personalized insights based on industry
def get_personalized_insight(industry):
    insights = {
        "Healthcare": "The healthcare sector is seeing a rise in digital health technologies.",
        "Retail": "The retail sector is shifting towards e-commerce and personalized shopping experiences.",
        "Finance": "Financial markets are increasingly using AI for stock predictions and risk management.",
        "Technology": "The tech industry is focusing on AI, blockchain, and cloud computing innovations."
    }
    return insights.get(industry, "Insights not available for this industry.")

# Set the background image for the app
def set_background_image(image_path):
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{base64_image}");
            background-size: cover;
            background-position: center;
            color: white;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

# Enhanced frontend with styling and animations
def load_frontend():
    st.markdown(
        """
        <style>
        h1 {
            font-size: 3rem;
            color: white;
            text-align: center;
            margin-bottom: 20px;
        }
        p.description {
            color: white;
            font-size: 1.2rem;
            text-align: center;
            margin-bottom: 20px;
        }
        .custom-button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            font-size: 1rem;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            text-align: center;
            margin-top: 20px;
        }
        .custom-button:hover {
            background-color: #45a049;
        }
        </style>
        <h1>AI Powered Business Insight Platform</h1>
        <p class="description">
            Seamlessly analyze images and queries with cutting-edge AI technology.
        </p>
        <div style="text-align: center; margin-top: 20px;">
            <lottie-player src="https://assets6.lottiefiles.com/private_files/lf30_lPRAfo.json"
                           background="transparent"
                           speed="1"
                           style="width: 300px; height: 300px;"
                           loop autoplay>
            </lottie-player>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Initialize background
background_image = ("background.jpeg")
set_background_image("background.jpeg")

# Load frontend
load_frontend()

# Sidebar for theme toggle
theme = st.sidebar.radio("Choose Theme:", ["Light", "Dark"])
if theme == "Dark":
    st.markdown(
        """
        <style>
        .stApp {
            background-color: rgb(17, 16, 20);
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# File uploader for images
uploaded_file = st.file_uploader(
    "Upload an image for analysis", type=["jpg", "jpeg", "png"]
)
st.markdown(
    """
    <style>
       .stFileUploader label {
            color:rgb(235, 245, 129); 
            font-size: 1.2rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Text input for user query
user_query = st.text_input("Enter your query", "")
st.markdown(
    """
    <style>
       .stTextInput label {
            color:rgb(235, 245, 129); 
            font-size: 1.2rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Industry selection for personalized insights
industry = st.selectbox("Select your Industry for Personalized Insights:", ["Healthcare", "Retail", "Finance", "Technology"])

# Button for speech-to-text
if st.button("Speak your Query"):
    user_query = speech_to_text()

# Function to perform automated market research (Placeholder)
def automated_market_research(image_data):
    return "Based on the market data in the image, the AI predicts a surge in demand for your product in the next quarter."

# Function to translate text to a target language
def translate_text(text, target_language='en'):
    translator = Translator()
    try:
        translated = translator.translate(text, dest=target_language)
        return translated.text
    except Exception as e:
        st.error(f"Error in translation: {e}")
        return text

# Add translation and market research to the frontend

# Language selection
target_language = st.selectbox("Select Target Language for Translation:", ["en", "es", "fr", "de", "it", "pt", "zh", "ja"])

# Automated Market Research Section
if uploaded_file:
    st.subheader("Automated Market Research:")
    market_research = automated_market_research(uploaded_file)
    st.write(market_research)

# Language Translation
if user_query:
    translated_query = translate_text(user_query, target_language=target_language)
    st.subheader("Translated Query:")
    st.write(f"Original Query: {user_query}")
    st.write(f"Translated Query ({googletrans.LANGUAGES[target_language]}): {translated_query}")

# Handle file upload and query input along with market research and language translation
if uploaded_file and user_query:
    # Display uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Get response from Gemini API
    with st.spinner("Processing your request..."):
        response_text = get_gemini_response(uploaded_file, user_query)

    # Display the response
    st.subheader("Response from Gemini:")
    st.markdown(
        f"""
        <div style="padding: 10px; border: 1px solid #ddd; border-radius: 10px; background-color:rgb(17, 17, 17);">
            {response_text}
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Option to download the response
    st.download_button(
        label="Download Response",
        data=response_text,
        file_name="gemini_response.txt",
        mime="text/plain",
    )

    # Button to send the response via email
    email = st.text_input("Enter your email to receive the response:")
    if email and st.button("Send to Email"):
        send_email(response_text, email)
        st.success("Email sent successfully!")

    # Display AI Trend Forecast
    trend_forecast = predict_trends(uploaded_file)
    st.subheader("AI Trend Forecast:")
    st.write(trend_forecast)

    # Display Personalized Insight based on industry
    personalized_insight = get_personalized_insight(industry)
    st.subheader("Personalized AI Insight:")
    st.write(personalized_insight)

else:
    if not uploaded_file:
        st.warning("Please upload an image.")
    if not user_query:
        st.warning("Please enter a query.")

# Feedback Section
st.markdown(
    """
    <div style="margin-top: 20px; text-align: center;">
        <p style="color: rgb(235, 245, 129);">Have feedback? Let us know below:</p>
    </div>
    """,
    unsafe_allow_html=True,
)
feedback = st.text_area("Your Feedback:")
st.markdown(
    """
    <style>
       .stTextArea label {
            color:rgb(235, 245, 129); 
            font-size: 1.2rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

if feedback:
    st.success("Thank you for your feedback!")
