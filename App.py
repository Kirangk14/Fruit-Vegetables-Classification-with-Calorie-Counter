import streamlit as st
import requests
import os
import numpy as np
from PIL import Image
from keras.models import load_model
from keras.preprocessing.image import load_img, img_to_array

model = load_model("FV.h5")

labels = {0: 'apple', 1: 'banana', 2: 'beetroot', 3: 'bell pepper', 4: 'cabbage', 5: 'capsicum',
          6: 'carrot', 7: 'cauliflower', 8: 'chilli pepper', 9: 'corn', 10: 'cucumber', 11: 'eggplant',
          12: 'garlic', 13: 'ginger', 14: 'grapes', 15: 'jalepeno', 16: 'kiwi', 17: 'lemon', 18: 'lettuce',
          19: 'mango', 20: 'onion', 21: 'orange', 22: 'paprika', 23: 'pear', 24: 'peas', 25: 'pineapple',
          26: 'pomegranate', 27: 'potato', 28: 'raddish', 29: 'soy beans', 30: 'spinach', 31: 'sweetcorn',
          32: 'sweetpotato', 33: 'tomato', 34: 'turnip', 35: 'watermelon'}

vegetables = ['Beetroot', 'Cabbage', 'Capsicum', 'Carrot', 'Cauliflower', 'Corn', 'Cucumber', 'Eggplant',
              'Ginger', 'Lettuce', 'Onion', 'Peas', 'Potato', 'Raddish', 'Soy Beans', 'Spinach', 'Sweetcorn',
              'Sweetpotato', 'Tomato', 'Turnip']

def prepare_image(img_path):
    img = load_img(img_path, target_size=(224, 224, 3))
    img = img_to_array(img) / 255.0
    img = np.expand_dims(img, axis=0)
    pred = model.predict(img)
    pred_index = np.argmax(pred, axis=1)[0]
    return labels[pred_index].capitalize()

def login_ui():
    st.title("🔐 Login / Signup")

    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    with tab1:
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            response = requests.post("http://127.0.0.1:5000/login", json={"username": username, "password": password})
            if response.status_code == 200:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("✅ Logged in successfully")
                st.experimental_rerun()
            else:
                st.error("❌ Invalid credentials")

    with tab2:
        new_user = st.text_input("New Username", key="new_user")
        new_pass = st.text_input("New Password", type="password", key="new_pass")
        if st.button("Sign Up"):
            res = requests.post("http://127.0.0.1:5000/signup", json={"username": new_user, "password": new_pass})
            if res.status_code == 201:
                st.success("🎉 Signup successful. Please login.")
            elif res.status_code == 409:
                st.warning("⚠️ Username already exists")
            else:
                st.error("Something went wrong. Try again.")

def app_ui():
    st.title("🍎 Fruit & Vegetable Classifier")
    st.write("Upload an image to classify it!")

    img_file = st.file_uploader("📤 Upload JPG/PNG Image", type=["jpg", "png"])
    if img_file:
        img = Image.open(img_file).resize((250, 250))
        st.image(img, caption="🖼️ Uploaded Image", use_container_width=True)

        upload_path = os.path.join("app/upload_images", img_file.name)
        os.makedirs("app/upload_images", exist_ok=True)
        with open(upload_path, "wb") as f:
            f.write(img_file.getbuffer())

        with st.spinner("🔍 Classifying..."):
            result = prepare_image(upload_path)

        st.markdown("### 📌 Prediction Result")
        if result.capitalize() in vegetables:
            st.info("🥕 **Vegetable**")
        else:
            st.info("🍉 **Fruit**")
        st.success(f"✅ **Predicted: {result}**")

        if st.button("Logout"):
            st.session_state.logged_in = False
            st.experimental_rerun()

if __name__ == "__main__":
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        app_ui()
    else:
        login_ui()
