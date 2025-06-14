
import streamlit as st
from PIL import Image
import requests
from bs4 import BeautifulSoup
import numpy as np
from keras.preprocessing.image import load_img, img_to_array
from keras.models import load_model

model = load_model('FV.h5')

labels = {0: 'apple', 1: 'banana', 2: 'beetroot', 3: 'bell pepper', 4: 'cabbage', 5: 'capsicum', 6: 'carrot',
          7: 'cauliflower', 8: 'chilli pepper', 9: 'corn', 10: 'cucumber', 11: 'eggplant', 12: 'garlic', 13: 'ginger',
          14: 'grapes', 15: 'jalepeno', 16: 'kiwi', 17: 'lemon', 18: 'lettuce',
          19: 'mango', 20: 'onion', 21: 'orange', 22: 'paprika', 23: 'pear', 24: 'peas', 25: 'pineapple',
          26: 'pomegranate', 27: 'potato', 28: 'raddish', 29: 'soy beans', 30: 'spinach', 31: 'sweetcorn',
          32: 'sweetpotato', 33: 'tomato', 34: 'turnip', 35: 'watermelon'}

fruits = ['Apple', 'Banana', 'Bello Pepper', 'Chilli Pepper', 'Grapes', 'Jalepeno', 'Kiwi', 'Lemon', 'Mango', 'Orange',
          'Paprika', 'Pear', 'Pineapple', 'Pomegranate', 'Watermelon']
vegetables = ['Beetroot', 'Cabbage', 'Capsicum', 'Carrot', 'Cauliflower', 'Corn', 'Cucumber', 'Eggplant', 'Ginger',
              'Lettuce', 'Onion', 'Peas', 'Potato', 'Raddish', 'Soy Beans', 'Spinach', 'Sweetcorn', 'Sweetpotato',
              'Tomato', 'Turnip']


def fetch_calories(prediction):
    try:
        url = 'https://www.google.com/search?&q=calories in ' + prediction
        req = requests.get(url).text
        scrap = BeautifulSoup(req, 'html.parser')
        calories = scrap.find("div", class_="BNeawe iBp4i AP7Wnd").text
        return calories
    except Exception as e:
        st.error("Can't able to fetch the Calories")
        print(e)


def prepare_image(img_path):
    img = load_img(img_path, target_size=(224, 224, 3))
    img = img_to_array(img)
    img = img / 255
    img = np.expand_dims(img, [0])
    answer = model.predict(img)
    y_class = answer.argmax(axis=-1)
    print(y_class)
    y = " ".join(str(x) for x in y_class)
    y = int(y)
    res = labels[y]
    print(res)
    return res.capitalize()


def run():
    st.title("Fruits🍍-Vegetable🍅 Classification")
    img_file = st.file_uploader("Choose an Image", type=["jpg", "png"])
    if img_file is not None:
        img = Image.open(img_file).resize((250, 250))
        st.image(img, use_column_width=False)
        save_image_path = './upload_images/' + img_file.name
        with open(save_image_path, "wb") as f:
            f.write(img_file.getbuffer())

        # if st.button("Predict"):
        if img_file is not None:
            result = prepare_image(save_image_path)
            if result in vegetables:
                st.info('**Category : Vegetables**')
            else:
                st.info('**Category : Fruit**')
            st.success("**Predicted : " + result + '**')
            cal = fetch_calories(result)
            if cal:
                st.warning('**' + cal + '(100 grams)**')



if __name__ == "__main__":
    run()
import streamlit as st
from PIL import Image
import numpy as np
import os
import time
import random
from keras.preprocessing.image import load_img, img_to_array
from keras.models import load_model
import random

# Page configuration
st.set_page_config(
    page_title="🍎 Fruit & Vegetable Classifier 🥬",
    page_icon="🍎",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for animations and styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container styling */
    .main {
        padding: 0rem 1rem;
    }
    
    /* Custom font */
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Animated background */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
    }
    
    /* Title animation */
    .animated-title {
        font-size: 3rem !important;
        text-align: center;
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: titleGlow 3s ease-in-out infinite alternate;
        margin-bottom: 0.5rem;
        font-weight: 700;
    }
    
    @keyframes titleGlow {
        from { filter: brightness(1); }
        to { filter: brightness(1.3); }
    }
    
    /* Subtitle styling */
    .subtitle {
        text-align: center;
        color: #ffffff;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        opacity: 0;
        animation: fadeInUp 1s ease-out 0.5s forwards;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Upload container */
    .upload-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        animation: slideUp 0.8s ease-out;
    }
    
    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(50px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* File uploader styling */
    .stFileUploader > div > div > div {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border: 3px dashed #ffffff;
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .stFileUploader > div > div > div:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2);
        border-color: #4ecdc4;
    }
    
    /* Upload text */
    .upload-text {
        color: white;
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .upload-subtext {
        color: rgba(255, 255, 255, 0.8);
        font-size: 1rem;
    }
    
    /* Image container */
    .image-container {
        text-align: center;
        margin: 2rem 0;
        animation: zoomIn 0.6s ease-out;
    }
    
    @keyframes zoomIn {
        from {
            opacity: 0;
            transform: scale(0.8);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    /* Progress bar container */
    .progress-container {
        background: rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
    }
    
    /* Custom progress bar */
    .custom-progress {
        width: 100%;
        height: 8px;
        background: rgba(255, 255, 255, 0.3);
        border-radius: 4px;
        overflow: hidden;
        margin: 1rem 0;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #4ecdc4, #45b7d1);
        border-radius: 4px;
        transition: width 0.3s ease;
        animation: progressGlow 2s ease-in-out infinite;
    }
    
    @keyframes progressGlow {
        0%, 100% { box-shadow: 0 0 5px rgba(69, 183, 209, 0.5); }
        50% { box-shadow: 0 0 20px rgba(69, 183, 209, 0.8); }
    }
    
    /* Loading animation */
    .loading-container {
        text-align: center;
        padding: 2rem;
        color: white;
    }
    
    .spinner {
        width: 50px;
        height: 50px;
        border: 4px solid rgba(255, 255, 255, 0.3);
        border-top: 4px solid #4ecdc4;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin: 0 auto 1rem;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Result cards */
    .result-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        margin: 1rem 0;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
        animation: resultSlide 0.8s ease-out;
        text-align: center;
    }
    
    @keyframes resultSlide {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Error result card */
    .error-result-card {
        background: linear-gradient(135deg, #ff6b6b 0%, #ff5252 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        margin: 1rem 0;
        box-shadow: 0 15px 35px rgba(255, 107, 107, 0.3);
        animation: errorSlide 0.8s ease-out;
        text-align: center;
    }
    
    @keyframes errorSlide {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Category badges */
    .category-badge {
        display: inline-block;
        padding: 0.5rem 1.5rem;
        border-radius: 25px;
        font-size: 1rem;
        font-weight: 600;
        margin: 1rem 0;
        animation: badgePop 0.6s ease-out 0.3s backwards;
    }
    
    @keyframes badgePop {
        from {
            opacity: 0;
            transform: scale(0.8);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    .fruit-badge {
        background: linear-gradient(45deg, #ff6b6b, #ff8e8e);
    }
    
    .vegetable-badge {
        background: linear-gradient(45deg, #51cf66, #69db7c);
    }
    
    .unknown-badge {
        background: linear-gradient(45deg, #ffa726, #ff9800);
    }
    
    /* Prediction text */
    .prediction-text {
        font-size: 2rem;
        font-weight: 700;
        margin: 1rem 0;
        animation: textGlow 2s ease-in-out infinite alternate;
    }
    
    @keyframes textGlow {
        from { text-shadow: 0 0 10px rgba(255, 255, 255, 0.3); }
        to { text-shadow: 0 0 20px rgba(255, 255, 255, 0.6); }
    }
    
    /* Calorie info */
    .calorie-info {
        background: rgba(255, 255, 255, 0.2);
        padding: 1rem;
        border-radius: 15px;
        margin-top: 1rem;
        backdrop-filter: blur(10px);
        animation: fadeInUp 0.6s ease-out 0.6s backwards;
    }
    
    /* Floating elements */
    .floating-element {
        position: fixed;
        font-size: 2rem;
        animation: float 6s ease-in-out infinite;
        opacity: 0.1;
        pointer-events: none;
        z-index: -1;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(180deg); }
    }
    
    /* Success/Error messages */
    .stSuccess > div {
        background: linear-gradient(45deg, #51cf66, #69db7c);
        color: white;
        border: none;
        animation: slideInRight 0.5s ease-out;
    }
    
    .stError > div {
        background: linear-gradient(45deg, #ff6b6b, #ff8e8e);
        color: white;
        border: none;
        animation: shake 0.5s ease-out;
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(100px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-10px); }
        75% { transform: translateX(10px); }
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #4ecdc4, #44a08d);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
    }
    
    /* Confetti animation */
    .confetti {
        position: fixed;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        animation: confetti-fall 3s linear forwards;
        pointer-events: none;
        z-index: 1000;
    }
    
    @keyframes confetti-fall {
        to {
            transform: translateY(100vh) rotate(360deg);
            opacity: 0;
        }
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .animated-title {
            font-size: 2rem !important;
        }
        
        .upload-container {
            padding: 1rem;
            margin: 0.5rem;
        }
        
        .prediction-text {
            font-size: 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'processed' not in st.session_state:
    st.session_state.processed = False
if 'prediction_result' not in st.session_state:
    st.session_state.prediction_result = None

# Load model (comment out if model file not available)
@st.cache_resource
def load_trained_model():
    try:
        model = load_model('FV.h5')
        return model
    except:
        st.warning("⚠ Model file 'FV.h5' not found. Using demo mode.")
        return None

# Class labels and categories
labels = {
    0: 'apple', 1: 'banana', 2: 'beetroot', 3: 'bell pepper', 4: 'cabbage', 5: 'capsicum', 6: 'carrot',
    7: 'cauliflower', 8: 'chilli pepper', 9: 'corn', 10: 'cucumber', 11: 'eggplant', 12: 'garlic', 13: 'ginger',
    14: 'grapes', 15: 'jalepeno', 16: 'kiwi', 17: 'lemon', 18: 'lettuce', 19: 'mango', 20: 'onion', 21: 'orange',
    22: 'paprika', 23: 'pear', 24: 'peas', 25: 'pineapple', 26: 'pomegranate', 27: 'potato', 28: 'raddish',
    29: 'soy beans', 30: 'spinach', 31: 'sweetcorn', 32: 'sweetpotato', 33: 'tomato', 34: 'turnip', 35: 'watermelon'
}

fruits = [
    'apple', 'banana', 'bell pepper', 'chilli pepper', 'grapes', 'jalepeno', 'kiwi', 'lemon', 'mango',
    'orange', 'paprika', 'pear', 'pineapple', 'pomegranate', 'watermelon'
]

vegetables = [
    'beetroot', 'cabbage', 'capsicum', 'carrot', 'cauliflower', 'corn', 'cucumber', 'eggplant', 'ginger',
    'lettuce', 'onion', 'peas', 'potato', 'raddish', 'soy beans', 'spinach', 'sweetcorn', 'sweetpotato',
    'tomato', 'turnip', 'garlic'
]

# Calorie data
calorie_data = {
    'apple': '52 calories', 'banana': '89 calories', 'beetroot': '43 calories', 'bell pepper': '31 calories',
    'cabbage': '25 calories', 'capsicum': '31 calories', 'carrot': '41 calories', 'cauliflower': '25 calories',
    'chilli pepper': '40 calories', 'corn': '86 calories', 'cucumber': '16 calories', 'eggplant': '25 calories',
    'garlic': '149 calories', 'ginger': '80 calories', 'grapes': '62 calories', 'jalepeno': '29 calories',
    'kiwi': '61 calories', 'lemon': '29 calories', 'lettuce': '15 calories', 'mango': '60 calories',
    'onion': '40 calories', 'orange': '47 calories', 'paprika': '282 calories', 'pear': '57 calories',
    'peas': '81 calories', 'pineapple': '50 calories', 'pomegranate': '83 calories', 'potato': '77 calories',
    'raddish': '16 calories', 'soy beans': '446 calories', 'spinach': '23 calories', 'sweetcorn': '86 calories',
    'sweetpotato': '86 calories', 'tomato': '18 calories', 'turnip': '28 calories', 'watermelon': '30 calories'
}

# Floating elements
st.markdown("""
<div class="floating-element" style="top: 10%; left: 10%; animation-delay: 0s;">🍎</div>
<div class="floating-element" style="top: 20%; right: 15%; animation-delay: 1s;">🥕</div>
<div class="floating-element" style="top: 60%; left: 5%; animation-delay: 2s;">🍌</div>
<div class="floating-element" style="bottom: 20%; right: 10%; animation-delay: 3s;">🥬</div>
<div class="floating-element" style="bottom: 10%; left: 20%; animation-delay: 4s;">🍊</div>
""", unsafe_allow_html=True)

def is_valid_category(label):
    """Check if the predicted label is a valid fruit or vegetable"""
    return label.lower() in fruits or label.lower() in vegetables

def prepare_image(img_path, model):
    """Prepare image for prediction and validate category"""
    try:
        img = load_img(img_path, target_size=(224, 224, 3))
        img = img_to_array(img)
        img = img / 255.0
        img = np.expand_dims(img, axis=0)
        
        if model:
            prediction = model.predict(img)
            pred_index = np.argmax(prediction, axis=1)[0]
            confidence = np.max(prediction) * 100
            label = labels[pred_index]
            
            # Check if confidence is too low (threshold can be adjusted)
            if confidence < 50:
                return None, confidence
            
            # Check if it's a valid fruit or vegetable
            if not is_valid_category(label):
                return None, confidence
            
            return label, confidence
        else:
            # Demo mode - random prediction
            if random.random() < 0.8:  # 80% chance of valid prediction
                label = random.choice(list(labels.values()))
                confidence = random.uniform(60, 95)
                return label, confidence
            else:
                return None, random.uniform(20, 49)
                
    except Exception as e:
        st.error(f"❌ Error processing image: {str(e)}")
        return None, 0

def create_confetti():
    """Create confetti animation"""
    confetti_colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#ffeaa7']
    confetti_html = ""
    
    for i in range(20):
        color = random.choice(confetti_colors)
        left = random.randint(0, 100)
        delay = random.uniform(0, 2)
        
        confetti_html += f"""
        <div class="confetti" style="
            background-color: {color};
            left: {left}%;
            top: -10px;
            animation-delay: {delay}s;
        "></div>
        """
    
    return confetti_html

def animate_progress():
    """Animate progress bar"""
    progress_container = st.empty()
    
    with progress_container.container():
        st.markdown("""
        <div class="progress-container">
            <div style="text-align: center; color: white; margin-bottom: 1rem;">
                <div class="spinner"></div>
                <h3>🔍 Analyzing your image with AI magic...</h3>
                <p>Please wait while we identify your fruit or vegetable</p>
            </div>
            <div class="custom-progress">
                <div class="progress-fill" id="progress" style="width: 0%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Simulate progress
        for i in range(0, 101, 5):
            time.sleep(0.1)
            st.markdown(f"""
            <script>
                document.getElementById('progress').style.width = '{i}%';
            </script>
            """, unsafe_allow_html=True)
    
    progress_container.empty()

def display_result(prediction, category, calories, confidence):
    """Display animated result for valid predictions"""
    category_emoji = "🍎" if category == "fruit" else "🥕"
    badge_class = "fruit-badge" if category == "fruit" else "vegetable-badge"
    
    # Create confetti
    confetti_html = create_confetti()
    st.markdown(confetti_html, unsafe_allow_html=True)
    
    # Display result card
    st.markdown(f"""
    <div class="result-card">
        <div class="category-badge {badge_class}">
            {category_emoji} {category.upper()}
        </div>
        <div class="prediction-text">
            ✅ {prediction.title()}
        </div>
        <div style="font-size: 1rem; margin: 1rem 0; opacity: 0.9;">
            🎯 Confidence: {confidence:.1f}%
        </div>
        <div class="calorie-info">
            🔥 <strong>Approximate Calories:</strong> {calories} (per 100g)
        </div>
    </div>
    """, unsafe_allow_html=True)

def display_error_result(confidence):
    """Display error result for invalid predictions"""
    st.markdown(f"""
    <div class="error-result-card">
        <div class="category-badge unknown-badge">
            ❓ UNKNOWN
        </div>
        <div class="prediction-text">
            🚫 Not a Fruit or Vegetable
        </div>
        <div style="font-size: 1rem; margin: 1rem 0; opacity: 0.9;">
            🎯 Confidence: {confidence:.1f}%
        </div>
        <div class="calorie-info">
            💡 <strong>Suggestion:</strong> Please upload an image of a fruit or vegetable for classification
        </div>
        <div style="margin-top: 1rem; font-size: 0.9rem; opacity: 0.8;">
            <p>📸 <strong>Tips for better results:</strong></p>
            <p>• Use clear, well-lit images</p>
            <p>• Ensure the fruit/vegetable is the main subject</p>
            <p>• Avoid blurry or heavily processed images</p>
            <p>• Try single items rather than mixed collections</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Main app
def main():
    # Title and subtitle
    st.markdown('<h1 class="animated-title">🍎 Fruit & Vegetable Classifier 🥬</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Upload an image to identify fruits and vegetables with AI-powered recognition</p>', unsafe_allow_html=True)
    
    # Upload container
    st.markdown('<div class="upload-container">', unsafe_allow_html=True)
    
    # Custom upload text
    st.markdown("""
    <div style="text-align: center; margin-bottom: 1rem;">
        <div class="upload-text">📤 Upload Your Image</div>
        <div class="upload-subtext">Drag and drop or click to browse (JPG, PNG)</div>
    </div>
    """, unsafe_allow_html=True)
    
    # File uploader
    uploaded_file = st.file_uploader(
        "",
        type=['jpg', 'jpeg', 'png'],
        help="Upload a clear image of a fruit or vegetable for best results"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Load model
    model = load_trained_model()
    
    if uploaded_file is not None:
        # Display uploaded image
        st.markdown('<div class="image-container">', unsafe_allow_html=True)
        
        # Open and resize image
        image = Image.open(uploaded_file)
        
        # Display image with custom styling
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(
                image, 
                caption="🖼 Uploaded Image", 
                use_container_width=True,
                width=300
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Create upload directory
        upload_folder = './upload_images/'
        os.makedirs(upload_folder, exist_ok=True)
        
        # Save uploaded file
        save_image_path = os.path.join(upload_folder, uploaded_file.name)
        with open(save_image_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Process button
        if st.button("🚀 Classify Image", type="primary", use_container_width=True):
            # Animate progress
            animate_progress()
            
            # Get prediction
            with st.spinner("Processing..."):
                prediction, confidence = prepare_image(save_image_path, model)
            
            if prediction is not None:
                # Valid fruit or vegetable detected
                category = "fruit" if prediction.lower() in fruits else "vegetable"
                calories = calorie_data.get(prediction.lower(), "Not available")
                
                # Store result in session state
                st.session_state.prediction_result = {
                    'prediction': prediction,
                    'category': category,
                    'calories': calories,
                    'confidence': confidence,
                    'is_valid': True
                }
                st.session_state.processed = True
                
                # Success message
                st.success("🎉 Classification completed successfully!")
                
                # Display result
                display_result(prediction, category, calories, confidence)
                
            else:
                # Invalid item detected or low confidence
                st.session_state.prediction_result = {
                    'confidence': confidence,
                    'is_valid': False
                }
                st.session_state.processed = True
                
                # Warning message
                st.warning("⚠ This doesn't appear to be a fruit or vegetable!")
                
                # Display error result
                display_error_result(confidence)
    
    # Reset button
    if st.session_state.processed:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Analyze Another Image", use_container_width=True):
            st.session_state.processed = False
            st.session_state.prediction_result = None
            st.rerun()
    
    # Info section
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    with st.expander("ℹ How it works"):
        st.markdown("""
        ### 🧠 AI-Powered Recognition
        This application uses deep learning to identify fruits and vegetables from images:
        
        - *🔍 Image Analysis*: Advanced computer vision algorithms analyze your uploaded image
        - *🎯 Classification*: The AI model predicts the type of fruit or vegetable
        - *✅ Validation*: Checks if the detected item is actually a fruit or vegetable
        - *📊 Nutritional Info*: Get calorie information for healthy eating choices
        - *⚡ Fast Processing*: Results in seconds with confidence scores
        
        ### 📱 Tips for Best Results
        - Use clear, well-lit images
        - Ensure the fruit/vegetable is the main subject
        - Avoid blurry or heavily filtered photos
        - Single items work better than mixed collections
        - Make sure the item fills most of the frame
        
        ### 🎯 Supported Items
        *Fruits:* Apple, Banana, Bell Pepper, Chilli Pepper, Grapes, Jalapeño, Kiwi, Lemon, Mango, Orange, Paprika, Pear, Pineapple, Pomegranate, Watermelon
        
        *Vegetables:* Beetroot, Cabbage, Capsicum, Carrot, Cauliflower, Corn, Cucumber, Eggplant, Garlic, Ginger, Lettuce, Onion, Peas, Potato, Radish, Soy Beans, Spinach, Sweet Corn, Sweet Potato, Tomato, Turnip
        """)
    
    # Footer
    st.markdown("""
    <div style="text-align: center; margin-top: 3rem; padding: 2rem; color: rgba(255,255,255,0.7);">
        <p>Made with ❤ using Streamlit and Deep Learning</p>
        <p>🌟 Helping you make healthier food choices with AI</p>
    </div>
    """, unsafe_allow_html=True)

if __name__== "_main_":
    main()
