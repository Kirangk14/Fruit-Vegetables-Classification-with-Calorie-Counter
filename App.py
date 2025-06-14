import streamlit as st
from PIL import Image
import requests
from bs4 import BeautifulSoup
import numpy as np
import os
from keras.preprocessing.image import load_img, img_to_array
from keras.models import load_model

model = load_model('FV.h5')

labels = {
    0: 'apple', 1: 'banana', 2: 'beetroot', 3: 'bell pepper', 4: 'cabbage', 5: 'capsicum', 6: 'carrot',
    7: 'cauliflower', 8: 'chilli pepper', 9: 'corn', 10: 'cucumber', 11: 'eggplant', 12: 'garlic', 13: 'ginger',
    14: 'grapes', 15: 'jalepeno', 16: 'kiwi', 17: 'lemon', 18: 'lettuce', 19: 'mango', 20: 'onion', 21: 'orange',
    22: 'paprika', 23: 'pear', 24: 'peas', 25: 'pineapple', 26: 'pomegranate', 27: 'potato', 28: 'raddish',
    29: 'soy beans', 30: 'spinach', 31: 'sweetcorn', 32: 'sweetpotato', 33: 'tomato', 34: 'turnip', 35: 'watermelon'
}

fruits = ['Apple', 'Banana', 'Bello Pepper', 'Chilli Pepper', 'Grapes', 'Jalepeno', 'Kiwi', 'Lemon', 'Mango',
          'Orange', 'Paprika', 'Pear', 'Pineapple', 'Pomegranate', 'Watermelon']

vegetables = ['Beetroot', 'Cabbage', 'Capsicum', 'Carrot', 'Cauliflower', 'Corn', 'Cucumber', 'Eggplant', 'Ginger',
              'Lettuce', 'Onion', 'Peas', 'Potato', 'Raddish', 'Soy Beans', 'Spinach', 'Sweetcorn', 'Sweetpotato',
              'Tomato', 'Turnip']


# def fetch_calories(prediction):
#     try:
#         url = f'https://www.google.com/search?q=calories+in+{prediction}'
#         headers = {"User-Agent": "Mozilla/5.0"}
#         req = requests.get(url, headers=headers).text
#         soup = BeautifulSoup(req, 'html.parser')
#         calories = soup.find("div", class_="BNeawe iBp4i AP7Wnd")
#         return calories.text if calories else "Not available"
#     except:
#         st.error("⚠️ Unable to fetch calorie information.")
#         return None


def prepare_image(img_path):
    img = load_img(img_path, target_size=(224, 224, 3))
    img = img_to_array(img)
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    prediction = model.predict(img)
    pred_index = np.argmax(prediction, axis=1)[0]
    return labels[pred_index].capitalize()


def run():
    st.set_page_config(page_title="Fruit & Vegetable Classifier", layout="centered")

    st.markdown("## 🍎 Fruit & Vegetable Classifier")
    st.markdown("Upload an image to classify it as a fruit or vegetable, and get its calorie estimate!")

    img_file = st.file_uploader("📤 Upload Image (JPG/PNG)", type=["jpg", "png"])

    if img_file:
        img = Image.open(img_file).resize((250, 250))
        st.image(img, caption="🖼️ Uploaded Image", use_container_width=True)

        upload_folder = './upload_images/'
        os.makedirs(upload_folder, exist_ok=True)
        save_image_path = os.path.join(upload_folder, img_file.name)

        with open(save_image_path, "wb") as f:
            f.write(img_file.getbuffer())

        with st.spinner("🔍 Classifying image..."):
            result = prepare_image(save_image_path)

        st.divider()
        st.markdown("### 📌 Prediction Result")

        if result in vegetables:
            st.info("🥕 **Category: Vegetable**")
        else:
            st.info("🍉 **Category: Fruit**")

        st.success(f"✅ **Predicted: {result}**")

        # calories = fetch_calories(result)
        # if calories:
        #     st.warning(f"🔥 **Estimated Calories**: {calories} *(per 100g)*")


if __name__ == "__main__":
    run()
