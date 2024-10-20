from flask import Flask, render_template, request, jsonify
import pickle
import re
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
STOPWORDS = set(stopwords.words('english'))

app = Flask(__name__)

# Load the trained model and vectorizer
with open('spam_model_nvb2.pkl', 'rb') as model_file:
    model, tfidf = pickle.load(model_file)

# Function to preprocess input email
def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    
    # Remove unwanted characters using regex (only keep letters, numbers, and spaces)
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  # Remove all non-alphanumeric characters except spaces
    
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()  # Replace multiple spaces with a single space and trim
    
    # Remove stopwords
    text = " ".join([word for word in text.split() if word not in STOPWORDS])
    
    return text

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Prediction route
@app.route('/predict', methods=['POST'])
def predict():
    # Get the input email text
    email_text = request.form['email_text']
    
    # Preprocess and convert input to feature vector
    processed_email = preprocess_text(email_text)  # Use the new preprocessing function
    email_features = tfidf.transform([processed_email]).toarray()
    
    # Make prediction
    prediction = model.predict(email_features)
    result = "Spam" if prediction[0] == 1 else "Not Spam"
    
    # Return result as JSON
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
