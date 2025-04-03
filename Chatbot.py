import streamlit as st
import openai
import random
import os

from dotenv import load_dotenv

api_key = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))
if not api_key:
    st.error("API Key not found. Make sure it's set in Streamlit Secrets or environment variables.")


# Initialize Streamlit app
st.set_page_config(page_title="Chandler Bing Chatbot", layout="wide")

# Add custom CSS to style the heading text with italics and background color
st.markdown("""
    <style>
    .friends-heading {
        font-family: 'Arial', sans-serif;
        font-size: 50px;
        font-weight: bold;
        color: black;
        text-transform: uppercase;
        letter-spacing: 5px;
        text-align: center;
        font-style: italic;  /* Makes the text slanted/italic */
    }

    /* Add custom CSS to set the background color to blue (#9abcd5) */
    .stApp {
        background-color: #9abcd5;
    }
    </style>
""", unsafe_allow_html=True)


# Use the styled text in the Streamlit app
st.markdown('<div class="friends-heading">F.R.I.E.N.D.S</div>', unsafe_allow_html=True)


# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Chatbot function
def get_chandler_response(user_input):
    if not api_key:
        return "Please enter your OpenAI API key in the sidebar."
    
    try:
        client = openai.Client(api_key=api_key)

        
        chandler_lines = [
            "Could I *be* any more awkward?",
            "Oh, yeah, that sounds like a *great* idea.",
            "I'm not great at the advice, but I can interest you in some self-doubt!",
            "I just realized I have nothing to offer but sarcasm and a vague knowledge of statistical analysis!",
            "This is all a *moo* point. You know, like a cow's opinion. It doesn’t matter."
        ]
        
        janice_mention = "Oh. My. God. Did someone say Janice?" if random.random() < 0.3 else ""
        
        messages = [
            {"role": "system", "content": (
                "You are Chandler Bing from *Friends*. You are extremely sarcastic, with a sharp, dry wit that you use to deflect emotional vulnerability."
                " You love making jokes in uncomfortable situations and never miss a chance for a snarky comeback."
            )}
        ]
        
        messages.append({"role": "user", "content": user_input})
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            temperature=1.2,  
            top_p=0.9,       
            frequency_penalty=0.5,
            presence_penalty=0.3,
            messages=messages
        )
        
        return response.choices[0].message.content + "\n" + janice_mention
    
    except Exception as e:
        return f"Error: {str(e)}"

# Title and subtitle
st.markdown("""
    <h1 style="text-align: center;">Chandler Bing Chatbot</h1>
    <h3 style="text-align: center; font-size: 18px; font-weight: normal;">Expect sarcasm, wit, and humor.</h3>
""", unsafe_allow_html=True)


# Handle input
def handle_input():
    user_input = st.session_state.input_box.strip()  # Get input from session state
    if user_input:  
        response = get_chandler_response(user_input)

        # Append to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.messages.append({"role": "assistant", "content": response})

    # Clear input field
    st.session_state.input_box = ""

# Text input field with `on_change`
st.text_input("Say something:", key="input_box", on_change=handle_input)

# Display recent chat history at the top
with st.container():
    for message in reversed(st.session_state.messages):
        if message["role"] == "user":
            st.chat_message("user").write(message["content"])
        else:
            st.chat_message("assistant").write(message["content"])

# Display older chats in a scrollable container
with st.expander("Older Chats", expanded=False):  # Allows for scrolling
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.chat_message("user").write(message["content"])
        else:
            st.chat_message("assistant").write(message["content"])


# Push image to the bottom
st.markdown("<div style='flex-grow: 1;'></div>", unsafe_allow_html=True)

# Load the image at the very bottom
image_url = "https://raw.githubusercontent.com/asmaahmad5/Chandler-Chat-bot/main/bottom-image.jpg"
st.image(image_url, use_container_width=True)

# Sidebar feedback form
st.sidebar.subheader("Give Feedback")
feedback = st.sidebar.radio("Was this response helpful?", ["👍", "👎"], index=None)
additional_feedback = st.sidebar.text_area("Additional feedback (optional)")

if st.sidebar.button("Submit Feedback"):
    with open("feedback.txt", "a", encoding="utf-8") as f:
        f.write(f"Thumbs Up: {feedback}, Feedback: {additional_feedback}\n")
    st.sidebar.success("Thanks for your feedback!")



