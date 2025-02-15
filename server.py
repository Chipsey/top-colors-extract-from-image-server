from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
from PIL import Image
from collections import Counter

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

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
    
    # Get pixel data and ignore alpha channel if present
    pixels = list(processed_image.getdata())

    # Count colors (now in RGB format)
    color_counts = Counter(pixels)
    top_colors = color_counts.most_common(3)

    # Convert to JSON-friendly format (only RGB, no alpha channel)
    top_colors_json = [{"rgb": list(color), "count": count} for color, count in top_colors]

    return jsonify({"top_colors": top_colors_json})

if __name__ == "__main__":
    app.run(debug=True)
