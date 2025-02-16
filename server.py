from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
from PIL import Image
from collections import Counter
import math

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def color_distance(color1, color2):
    """Calculate Euclidean distance between two RGB colors."""
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    return math.sqrt((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2)

@app.route("/process-image", methods=["POST"])
def process_image():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image_file = request.files["image"]
    
    # Open and process the image
    processed_image = Image.open(image_file).convert("RGBA")  # Convert to RGBA (including alpha channel)
    
    # Convert to RGB to discard alpha channel
    processed_image = processed_image.convert("RGB")
    
    # Resize for faster color analysis
    processed_image = processed_image.resize((100, 100))
    
    # Get pixel data
    pixels = list(processed_image.getdata())

    # Count colors
    color_counts = Counter(pixels)
    top_colors = color_counts.most_common(3)  # Get top 3 most frequent colors

    # Extract the two most common colors
    first_color, _ = top_colors[0]
    second_color, _ = top_colors[1]

    # Now we need to find the third color with the highest contrast compared to the first two
    max_contrast = -1
    third_color = None

    # Iterate through all the remaining colors to find the one with the most contrast
    for color, _ in color_counts.most_common():
        if color != first_color and color != second_color:
            contrast = min(color_distance(color, first_color), color_distance(color, second_color))
            if contrast > max_contrast:
                max_contrast = contrast
                third_color = color

    # Convert to JSON-friendly format (RGB, no alpha channel)
    selected_colors_json = [
        {"rgb": list(first_color)},
        {"rgb": list(second_color)},
        {"rgb": list(third_color)}
    ]

    return jsonify({"top_colors": selected_colors_json})

if __name__ == "__main__":
    app.run(debug=True)
