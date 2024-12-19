import os
import streamlit as st
import google.generativeai as genai 
import base64
from PIL import Image

# Configure Gemini API
genai_api_key = 'AIzaSyC4NuVn03-OSV2C9OprFChupLmV7Azoq4I'
genai.configure(api_key=genai_api_key)

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

# Set the background image for the app
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




# Handle file upload and query input
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
