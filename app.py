import streamlit as st
import cv2
import numpy as np

def cartoonify_image(img_rgb, line_size, blur_value, k):
    """
    Applies a cartoon effect to an image using OpenCV.
    """
    
    # 1. Convert to Grayscale
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
    
    # 2. Apply Median Blur
    img_blur = cv2.medianBlur(img_gray, blur_value)
    
    # 3. Get Edges using Adaptive Threshold
    # This creates the black outlines
    img_edges = cv2.adaptiveThreshold(img_blur, 255, 
                                      cv2.ADAPTIVE_THRESH_MEAN_C, 
                                      cv2.THRESH_BINARY, 
                                      line_size, 
                                      blur_value)
    
    # 4. Reduce the Color Palette (Quantization)
    # Convert image to float32 for k-means
    data = np.float32(img_rgb).reshape(-1, 3)
    
    # Define criteria and apply k-means
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.001)
    ret, label, center = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    
    # Convert centers back to uint8
    center = np.uint8(center)
    
    # Reshape the data to the original image shape
    img_quantized = center[label.flatten()]
    img_quantized = img_quantized.reshape(img_rgb.shape)
    
    # 5. Apply Bilateral Filter to the quantized image
    # This smooths the colors while keeping edges sharp
    img_bilateral = cv2.bilateralFilter(img_quantized, d=7, sigmaColor=200, sigmaSpace=200)

    # 6. Combine Edges and Color-Reduced Image
    # Convert the single-channel edges to a 3-channel image
    img_edges_rgb = cv2.cvtColor(img_edges, cv2.COLOR_GRAY2RGB)
    
    # Use bitwise 'and' to combine the smoothed colors with the black outlines
    cartoon_img = cv2.bitwise_and(img_bilateral, img_edges_rgb)
    
    return cartoon_img

# --- Streamlit App ---

st.set_page_config(layout="wide", page_title="Cartoonify Your Image")
st.title("🎨 Cartoonify Your Image!")
st.write("Upload an image, or use your webcam, to see it transformed into a cartoon!")

# Sidebar for controls
st.sidebar.header("Tune Parameters")

# Sliders for parameters (must be odd numbers)
line_size = st.sidebar.slider("Line Size (Odd Numbers)", 3, 15, 7, step=2)
blur_value = st.sidebar.slider("Blur Value (Odd Numbers)", 3, 15, 7, step=2)
k = st.sidebar.slider("Number of Colors (k)", 2, 20, 9)

st.sidebar.write("Adjust the sliders to change the thickness of the lines, the amount of blur, and the number of colors in the final image.")

# Main content area
# --- NEW: Tabs for Upload or Webcam ---
tab1, tab2 = st.tabs(["Upload an Image 🖼️", "Capture with Webcam 📸"])

img_file_buffer = None

with tab1:
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        img_file_buffer = uploaded_file

with tab2:
    webcam_photo = st.camera_input("Take a picture")
    if webcam_photo is not None:
        img_file_buffer = webcam_photo

# Check if we have an image from either source
if img_file_buffer is not None:
    # Read the file buffer into an OpenCV image
    file_bytes = np.asarray(bytearray(img_file_buffer.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    
    # Convert from BGR (OpenCV default) to RGB (for display)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Process the image
    cartoon_output = cartoonify_image(img_rgb, line_size, blur_value, k)
    
    # Display the images side-by-side
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("Original Image")
        st.image(img_rgb, use_container_width=True) 
        
    with col2:
        st.header("Cartoonified Image")
        st.image(cartoon_output, use_container_width=True)

        # --- NEW: Download Button ---
        
        # 1. Convert cartoon image from RGB (for display) to BGR (for saving)
        cartoon_bgr = cv2.cvtColor(cartoon_output, cv2.COLOR_RGB2BGR)
        
        # 2. Encode image to PNG in memory
        _ , buf = cv2.imencode(".png", cartoon_bgr)
        
        # 3. Create the download button
        st.download_button(
            label="📥 Download Cartoon Image",
            data=buf.tobytes(),
            file_name="cartoon_image.png",
            mime="image/png"
        )
else:
    st.info("Please upload an image or take a photo to get started.")