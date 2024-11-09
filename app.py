import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

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

# Function to recommend outfit type based on skin tone and body shape
def recommend_outfit_type(skin_tone, undertone, body_shape):
    outfit_recommendations = []

    # Skin tone and undertone recommendations
    if skin_tone in ["Very Light", "Light"] and undertone == "Cool":
        outfit_recommendations.append("Anarkali suits in deep blue or emerald green, lehengas with silver embellishments, and sarees in icy pastels.")
    elif skin_tone in ["Medium Light", "Medium"] and undertone == "Neutral":
        outfit_recommendations.append("Cream or beige sarees with colorful borders, and anarkalis that mix both warm and cool colors.")
    elif skin_tone in ["Medium Dark", "Dark"] and undertone == "Warm":
        outfit_recommendations.append("Bright lehengas in orange or coral, sarees in warm golds, and salwar kameez in earthy tones.")
    else:
        outfit_recommendations.append("Classic white shirts paired with any color bottoms, and dresses that blend both warm and cool shades.")

    # Body shape recommendations
    if body_shape == "Hourglass":
        outfit_recommendations.append("Fitted dresses that cinch at the waist, such as wrap dresses or A-line dresses.")
    elif body_shape == "Pear":
        outfit_recommendations.append("A-line dresses that flare out from the waist, off-the-shoulder tops to broaden the shoulder line.")
    elif body_shape == "Apple":
        outfit_recommendations.append("Empire waist dresses that flow from the bust, V-neck tops that elongate the torso.")
    elif body_shape == "Rectangle":
        outfit_recommendations.append("Shift dresses that create a more defined waistline with a belt, layered tops to add shape.")
    elif body_shape == "Inverted Triangle":
        outfit_recommendations.append("A-line dresses that balance the upper body with a flared skirt, simple fitted tops.")
    elif body_shape == "Diamond":
        outfit_recommendations.append("A-line or empire waist dresses that flow over the midsection, tops with embellishments at the neckline.")

    return outfit_recommendations

# Function to analyze the image and display results
def analyze_image(image_path, body_shape):
    image = cv2.imread(image_path)
    features = extract_skin_features(image)
    skin_tone = categorize_skin_tone(features)
    undertone = determine_undertone(skin_tone)
    
    recommendations = {
        "Skin Tone": skin_tone,
        "Undertone": undertone,
        "Recommended Jewelry": recommend_jewelry(undertone),
        "Recommended Color Palette": recommend_color_palette(undertone),
        "Recommended Outfit Type": recommend_outfit_type(skin_tone, undertone, body_shape)
    }
    
    return recommendations, image

# Function to resize the image while maintaining the aspect ratio
def resize_image(image, max_width, max_height):
    """Resize the image while maintaining the aspect ratio."""
    width, height = image.size
    aspect_ratio = width / height
    
    if width > max_width:
        width = max_width
        height = int(width / aspect_ratio)
    
    if height > max_height:
        height = max_height
        width = int(height * aspect_ratio)
    
    return image.resize((width, height), Image.LANCZOS)

# Function to capture image from webcam
def capture_image():
    # Initialize the webcam
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    
    if ret:
        # Save the captured image
        image_path = "captured_image.jpg"
        cv2.imwrite(image_path, frame)
        return image_path
    else:
        messagebox.showerror("Error", "Failed to capture image from webcam.")
        return None

# Function to upload an image from the gallery
def upload_image():
    file_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
    return file_path

# Main function to run the program
def main():
    root = tk.Tk()
    root.title("Skin Tone Analyzer")
    root.geometry("600x400")  # Increased size for the main dialog
    root.resizable(False, False)  # Disable resizing

    # Load background image
    background_image = Image.open("clo1.png")  # Update with your image path
    background_image = background_image.resize((600, 400), Image.LANCZOS)  # Use LANCZOS instead of ANTIALIAS
    background_photo = ImageTk.PhotoImage(background_image)

    background_label = tk.Label(root, image=background_photo)
    background_label.image = background_photo  # Keep a reference
    background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Cover the entire window

    label = tk.Label(root, text="Choose an option:", bg='white')  # Set background color for text
    label.pack(pady=10)

    # Body shape selection
    body_shapes = ["Select Body Shape", "Pear", "Rectangle", "Apple", "Hourglass", "Athletic"]
    selected_body_shape = tk.StringVar(value=body_shapes[0])  # Default value

    body_shape_label = tk.Label(root, text="Select your body shape:", bg='white')
    body_shape_label.pack(pady=5)

    body_shape_menu = tk.OptionMenu(root, selected_body_shape, *body_shapes)
    body_shape_menu.pack(pady=5)

    def capture_image_callback():
        image_path = capture_image()
        display_results(image_path, selected_body_shape.get())
    
    def upload_image_callback():
        image_path = upload_image()
        if image_path:
            display_results(image_path, selected_body_shape.get())
        else:
            messagebox.showwarning("Warning", "No image selected.")

    capture_button = tk.Button(root, text="Capture Image from Webcam", command=capture_image_callback)
    capture_button.pack(pady=5)
    
    upload_button = tk.Button(root, text="Upload Image from Gallery", command=upload_image_callback)
    upload_button.pack(pady=5)
    
    root.mainloop()

def display_results(image_path, body_shape):
    recommendations, image = analyze_image(image_path , body_shape)
    
    # Display the image in a new window
    result_window = tk.Toplevel()
    result_window.title("Analysis Results")
    result_window.geometry("600x500")  # Increased size for the results dialog
    result_window.resizable(False, False)  # Disable resizing

    # Load background image for results window
    background_image = Image.open("clo1.png")  # Update with your image path
    background_image = background_image.resize((600, 500), Image.LANCZOS)  # Use LANCZOS instead of ANTIALIAS
    background_photo = ImageTk.PhotoImage(background_image)

    background_label = tk.Label(result_window, image=background_photo)
    background_label.image = background_photo  # Keep a reference
    background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Cover the entire window

    # Convert image for Tkinter
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(image)

    # Resize the image to fit within a maximum size
    max_width, max_height = 500, 400
    image = resize_image(image, max_width, max_height)  # Resize only the image
    image = ImageTk.PhotoImage(image)
    
    img_label = tk.Label(result_window, image=image)
    img_label.image = image  # Keep a reference to avoid garbage collection
    img_label.pack(pady=10)
    
    # Create a Text widget for recommendations
    results_text = "\n".join([f"{key}: {value}" for key, value in recommendations.items()])
    results_text_box = tk.Text(result_window, wrap=tk.WORD, height=10, width=70)  # Adjust height and width as needed
    results_text_box.insert(tk.END, results_text)
    results_text_box.config(state=tk.DISABLED)  # Make it read-only
    results_text_box.pack(pady=10, padx=10)  # Add padding for better appearance

    # Add a scrollbar
    scrollbar = tk.Scrollbar(result_window, command=results_text_box.yview)
    results_text_box['yscrollcommand'] = scrollbar.set
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    results_text_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Display the selected body shape
    body_shape_label = tk.Label(result_window, text=f"Selected Body Shape: {body_shape}", bg='white')
    body_shape_label.pack(pady=5)

if __name__ == "__main__":
    main()