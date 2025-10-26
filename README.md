# 🎨 ToonLens: The Live Cartoonifier App

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)
*(Deploy your app to Streamlit Community Cloud to get a live URL for this badge!)*

Instantly cartoonify your world! 🎨 This Streamlit web app uses OpenCV to transform any image into a cartoon. Upload a photo or capture one live from your webcam. 📸 Use built-in sliders to adjust line thickness, blur, and color quantization for the perfect look. Download your finished cartoon with a single click.

![Demo Screenshot](https://i.imgur.com/your-demo.gif)
*(**Note:** Record a quick GIF of your app and replace the link above to show it off!)*

---

## ✨ Features

* **Dual Input Modes:** Choose between uploading a static image (`.jpg`, `.png`) or capturing a live photo from your webcam.
* **Real-Time Parameter Tuning:** Use interactive sliders to control:
    * **Line Size:** Adjust the thickness of the cartoon outlines.
    * **Blur Value:** Control the amount of noise reduction.
    * **Number of Colors (k):** Reduce the color palette using k-means clustering for a classic cartoon look.
* **Instant Download:** Save your cartoonified image directly from the app with a single click.
* **Side-by-Side Comparison:** See the original and the transformed image at the same time.

---

## 🛠️ Technology Stack

* **Framework:** [Streamlit](https://streamlit.io/)
* **Image Processing:** [OpenCV-Python](https://opencv.org/)
* **Numerical Operations:** [NumPy](https://numpy.org/)

---

## 🚀 How to Run Locally

Follow these steps to get the app running on your local machine.

### 1. Clone the Repository

```bash
git clone [https://github.com/Sarthakdwivedi78/ToonLens.git](https://github.com/Sarthakdwivedi78/ToonLens.git)
cd ToonLens
```



2. Create a Virtual Environment (Recommended)
```Bash

# For Windows
python -m venv venv
.\venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install Dependencies
Create a file named requirements.txt in the ToonLens folder and add the following lines:
```bash
streamlit
opencv-python-headless
numpy
```
Now, run this command in your terminal:

```Bash

pip install -r requirements.txt
```
4. Run the App
```Bash

streamlit run app.py
```
