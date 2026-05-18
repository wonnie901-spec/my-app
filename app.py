import re
import streamlit as st
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
# Page config
st.set_page_config(
    page_title="AI Scam Detector",
    layout="centered"
)

# Hide Streamlit branding and footer so embed looks clean
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

#Custom CSS for font + background
st.markdown(
    """
    <style>
    @import url ('https://fonts.googleapis.com/css2?family=CatchyMager:wght@400;600&display=swap')
    
    html, body, [class*="css"] {
          font-family: 'Catchy Mager', sans-serif;
    }
    
    body  {
         background-color: #073763ff; /* dark blue 3 */
         color: white;
     }
    </style>
    """,
    unsafe_allow_html=True
)

# Function to clean text
def clean_text(text):
    return re.sub(r'[^a-zA-Z0-9 ]', '', text.lower())

# Training dataset (expand as needed)
messages = [
    "Your loan is approved, click here to pay fee", # scam
    "Update your KYC immediately or account blocked", # scam
    "Congratulations! You won a cashback reward, pay ₹999 to claim", # scam
    "Click here to unlock your credit card bonus", # scam
    "Your account will be frozen unless you verify now", # scam
    "Monthly statement is available on your banking portal", # safe
    "Your insurance premium reminder for May", # safe
    "Transaction of ₹500 credited to your account", # safe
    "Your EMI payment was successful", # safe
    "Your credit card statement for April is ready", # safe
]

labels = [
    "scam","scam","scam","scam","scam",
    "safe","safe","safe","safe","safe"
]

# Vectorize and train
vectorizer = CountVectorizer()
X = vectorizer.fit_transform([clean_text(m) for m in messages])
model = MultinomialNB()
model.fit(X, labels)

# Streamlit UI
st.title("PhishProof – Scam Detector")
st.write("Paste a **website link** or **email text** below to check if it looks suspicious.")

user_input = st.text_area("Enter website URL or email text:")

if st.button("Check"):
    if user_input.strip() == "":
        st.warning("Please enter some text or a link.")
    else:
        cleaned = clean_text(user_input)
        X_new = vectorizer.transform([cleaned])
        prediction = model.predict(X_new)[0]
        
        if prediction == "scam":
            st.error("⚠️ This looks like a **SCAM / Phishing attempt**.")
        else:
            st.success("✅ This looks **SAFE**.")
