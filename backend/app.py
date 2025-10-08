import os
import cv2
import numpy as np
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from ultralytics import YOLO
from PIL import Image
import base64
from io import BytesIO
from pymongo import MongoClient  # For MongoDB

# ---------- MongoDB Setup ----------
client = MongoClient("mongodb://localhost:27017/")  # single client
db = client["ecobuddy_db"]
complaints_collection = db["complaints"]

# ---------- Initialize Flask App ----------
app = Flask(__name__)

# Directory for uploaded images
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Allowed image extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Load YOLOv8 model
model = YOLO("yolov8m.pt")

# Waste Management Recommendations
waste_recommendations = {
    "bottle": {"reuse": "Use it as a planter or storage container.", "dispose": "Drop at plastic recycling centers."},
    "can": {"reuse": "Make a DIY pen holder.", "dispose": "Dispose at a metal recycling facility."},
    "paper": {"reuse": "Use as scrap paper for notes.", "dispose": "Recycle at a paper recycling bin."},
    "plastic": {"reuse": "Repurpose for crafts.", "dispose": "Find a nearby plastic recycling bin."}
}

# ---------- Helper Functions ----------
def image_to_base64(image):
    """Convert image to base64 string"""
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str

def allowed_file(filename):
    """Check if uploaded file has an allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ---------- Routes ----------
@app.route("/")
def index():
    return render_template("index.html")

# YOLO Detection Route
@app.route("/upload", methods=["POST"])
def upload_file():
    if "image" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(file_path)

    # YOLOv8 Detection
    results = model(file_path)
    result = results[0]

    detections = {}
    for box in result.boxes.data.tolist():
        x1, y1, x2, y2, confidence, class_id = box
        class_name = result.names[int(class_id)]
        reuse_tip = waste_recommendations.get(class_name, {}).get("reuse", "No suggestion available.")
        dispose_tip = waste_recommendations.get(class_name, {}).get("dispose", "No disposal info available.")

        if class_name not in detections:
            detections[class_name] = {"count": 1, "reuse": reuse_tip, "dispose": dispose_tip}
        else:
            detections[class_name]["count"] += 1

    # Base64 Conversion
    original_image = Image.open(file_path)
    original_image_base64 = image_to_base64(original_image)

    processed_image = cv2.imread(file_path)
    for box in result.boxes.data.tolist():
        x1, y1, x2, y2, confidence, class_id = box
        class_name = result.names[int(class_id)]
        color = (0, 255, 0)
        label = f"{class_name} ({confidence:.2f})"
        cv2.rectangle(processed_image, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(processed_image, label, (int(x1), int(y1) - 10), font, 0.5, color, 2)

    processed_image_path = os.path.join(app.config["UPLOAD_FOLDER"], "processed_" + filename)
    cv2.imwrite(processed_image_path, processed_image)
    processed_image_pil = Image.open(processed_image_path)
    processed_image_base64 = image_to_base64(processed_image_pil)

    return jsonify({
        "detections": [{"class": key, "count": value["count"], "reuse": value["reuse"], "dispose": value["dispose"]} for key, value in detections.items()],
        "original_image_url": f"data:image/jpeg;base64,{original_image_base64}",
        "processed_image_url": f"data:image/jpeg;base64,{processed_image_base64}"
    })

# Complaint Reporting Route
@app.route("/report", methods=["POST"])
def report_dumping():
    data = request.form
    photos = request.files.getlist("photos")

    photo_paths = []
    for photo in photos:
        if photo and allowed_file(photo.filename):
            filename = secure_filename(photo.filename)
            path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            photo.save(path)
            photo_paths.append(path)

    report_data = {
        "name": data.get("name", "Anonymous"),
        "contact": data.get("contact"),
        "location": data.get("location"),
        "latitude": data.get("latitude"),
        "longitude": data.get("longitude"),
        "description": data.get("description"),
        "photos": photo_paths
    }
    complaints_collection.insert_one(report_data)

    return jsonify({"message": "Report submitted successfully!"})

# ---------- Run Server ----------
if __name__ == "__main__":
    app.run(debug=True)
