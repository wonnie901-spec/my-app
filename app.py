import re
import streamlit as st
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Function to clean text
def clean_text(text):
    return re.sub(r'[^a-zA-Z0-9₹ ]', '', text.lower())

# Expanded fintech dataset
messages = [
    "Your loan is approved, click here to pay fee",   # scam
    "Update your KYC immediately or account blocked", # scam
    "Congratulations! You won a cashback reward, pay ₹999 to claim", # scam
    "Click here to unlock your credit card bonus", # scam
    "Your account will be frozen unless you verify now", # scam
    "Pay processing fee to release your insurance claim", # scam
    "Urgent: Transfer funds to secure your account", # scam
    "Limited time offer: Get instant loan by paying upfront fee", # scam
    "Your UPI ID has been compromised, click link to fix", # scam
    "Recharge wallet now to avoid penalty", # scam
    "Monthly statement is available in your netbanking portal", # safe
    "Your insurance premium reminder for May", # safe
    "KYC update successful, no further action needed", # safe
    "Transaction of ₹500 credited to your account",   # safe
    "Your EMI payment is due tomorrow",               # safe
    "₹2000 debited from your account for electricity bill", # safe
    "Your loan application is under review", # safe
    "Payment of ₹750 received successfully", # safe
    "Your credit card bill is generated", # safe
    "UPI transaction of ₹100 completed successfully", # safe
]

labels = [1,1,1,1,1,1,1,1,1,1,   # Scam = 1
          0,0,0,0,0,0,0,0,0,0]   # Safe = 0
          
          # Clean messages
cleaned_messages = [clean_text(msg) for msg in messages]

# Split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(
    cleaned_messages, labels, test_size=0.3, random_state=42
)

# Vectorize
vectorizer = CountVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Train model
model = MultinomialNB()
model.fit(X_train_vec, y_train)

# Evaluate accuracy
y_pred = model.predict(X_test_vec)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# Function to detect scam
def detect_scam(text):
    text = clean_text(text)
    X_new = vectorizer.transform([text])
    prediction = model.predict(X_new)[0]
    return "⚠️ Scam Detected" if prediction == 1 else "✅ Safe Message"

# Try new examples
print(detect_scam("Your EMI payment is due tomorrow"))
print(detect_scam("Click here to pay processing fee"))

st.title("Fintech Scam Detector")
user_input = st.text_input("Enter a fintech message message:")

if user_input:
    result = detect_scam(user_input)
    st.write(result)
