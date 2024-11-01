import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import tkinter as tk
from tkinter import filedialog

# Function to extract skin color features from an image
def extract_skin_features(image):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Define skin color range in HSV
    lower_skin = np.array([0, 20, 70], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)
    
    # Create a mask for skin color
    skin_mask = cv2.inRange(hsv_image, lower_skin, upper_skin)
    
    # Extract skin pixels
    skin_pixels = cv2.bitwise_and(image, image, mask=skin_mask)
    
    # Convert to grayscale and flatten the array
    gray_skin = cv2.cvtColor(skin_pixels, cv2.COLOR_BGR2GRAY)
    features = gray_skin.flatten()
    
    # Remove zero values (non-skin pixels)
    features = features[features > 0]
    
    return features

# Function to categorize skin tones
def categorize_skin_tone(features):
    if len(features) == 0:
        return "No skin detected"
    
    mean_intensity = np.mean(features)
    
    if mean_intensity < 50:
        return "Very Light"
    elif mean_intensity < 100:
        return "Light"
    elif mean_intensity < 150:
        return "Medium Light"
    elif mean_intensity < 200:
        return "Medium"
    elif mean_intensity < 250:
        return "Medium Dark"
    else:
        return "Dark"

# Function to determine skin undertone
def determine_undertone(skin_tone):
    if skin_tone in ["Very Light", "Light"]:
        return "Cool"
    elif skin_tone in ["Medium Light", "Medium"]:
        return "Neutral"
    else:
        return "Warm"

# Function to recommend jewelry
def recommend_jewelry(undertone):
    if undertone == "Cool":
        return "Silver, white gold, platinum, and gemstones like sapphire, amethyst, and emerald."
    elif undertone == "Warm":
        return "Yellow gold, rose gold, copper, and gemstones like amber, citrine, and coral."
    else:
        return "Versatile options including both silver and gold, and gemstones like diamonds, pearls, and jade."

# Function to recommend color palette
def recommend_color_palette(undertone):
    if undertone == "Cool":
        return "Jewel tones (blues, purples, emerald greens), icy shades, and cool pastels."
    elif undertone == "Warm":
        return "Earthy tones (oranges, yellows, warm reds), warm pastels, and golden shades."
    else:
        return "A mix of both warm and cool colors, including soft neutrals and muted tones."

# Function to recommend outfit type
def recommend_outfit_type(skin_tone, undertone):
    if skin_tone in ["Very Light", "Light"] and undertone == "Cool":
        return "Anarkali suits in deep blue or emerald green, lehengas with silver embellishments, and sarees in icy pastels."
    elif skin_tone in ["Medium Light", "Medium"] and undertone == "Neutral":
        return "Cream or beige sarees with colorful borders, and anarkalis that mix both warm and cool colors."
    elif skin_tone in ["Medium Dark", "Dark"] and undertone == "Warm":
        return "Bright lehengas in orange or coral, sarees in warm golds, and salwar kameez in earthy tones."
    else:
        return "Classic white shirts paired with any color bottoms, and dresses that blend both warm and cool shades."

# Function to capture image from webcam
def capture_image():
    cap = cv2.VideoCapture(0)
    print("Press 'c' to capture an image.")
    
    while True:
        ret, frame = cap.read()
        cv2.imshow('Webcam', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('c'):
            cv2.imwrite('captured_image.jpg', frame)
            break
    
    cap.release()
    cv2.destroyAllWindows()
    return 'captured_image.jpg'

# Function to upload an image from the gallery
def upload_image():
    root = tk.Tk()
    root.withdraw()
    image_path = filedialog.askopenfilename()
    return image_path

# Main function to run the program
def main():
    root = tk.Tk()
    root.title ("Skin Tone Analyzer")
    
    label = tk.Label(root, text="Choose an option:")
    label.pack()
    
    def capture_image_callback():
        image_path = capture_image()
        analyze_image(image_path)
    
    def upload_image_callback():
        image_path = upload_image()
        analyze_image(image_path)
    
    capture_button = tk.Button(root, text="Capture Image from Webcam", command=capture_image_callback)
    capture_button.pack()
    
    upload_button = tk.Button(root, text="Upload Image from Gallery", command=upload_image_callback)
    upload_button.pack()
    
    root.mainloop()

def analyze_image(image_path):
    image = cv2.imread(image_path)
    features = extract_skin_features(image)
    skin_tone = categorize_skin_tone(features)
    undertone = determine_undertone(skin_tone)
    
    print("Skin Tone:", skin_tone)
    print("Undertone:", undertone)
    print("Recommended Jewelry:", recommend_jewelry(undertone))
    print("Recommended Color Palette:", recommend_color_palette(undertone))
    print("Recommended Outfit Type:", recommend_outfit_type(skin_tone, undertone))

if __name__ == "__main__":
    main()