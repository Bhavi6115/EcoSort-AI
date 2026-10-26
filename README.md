# ♻️ EcoSort AI: Smart Waste Segregation & Disposal System

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-yellow.svg)
![License](https://img.shields.io/badge/License-MIT-purple.svg)

EcoSort AI is a software-only, AI-powered web application designed to bridge the gap between waste identification and correct disposal action. Aligned with **UN SDG 11 (Sustainable Cities) and SDG 12 (Responsible Consumption)**, this platform makes source segregation accessible to anyone with a smartphone browser—no expensive hardware required.

## ✨ Key Features
- **Multi-Item Detection:** Uses a custom-trained YOLOv8 model to detect multiple mixed waste items in a single photo.
- **6-Class Material Mapping:** Classifies 18 raw waste classes into 6 clear disposal categories (Cardboard, Glass, Metal, Paper, Plastic, Trash).
- **The EcoScore Metric:** Calculates a 0-100 sustainability score based on recyclability to gamify the recycling process.
- **Smart Disposal & DIY:** Provides actionable bin-color guidance and circular economy DIY upcycling ideas.
- **Dark Mode & Analytics:** A fully responsive glassmorphism UI with a persistent dark mode toggle and interactive Chart.js dashboards.

## 🛠️ Tech Stack
- **Machine Learning:** YOLOv8s (Ultralytics), PyTorch, TACO Dataset
- **Backend:** Python, Flask, Jinja2
- **Frontend:** HTML5, Vanilla JS, Custom CSS3 (Glassmorphism)
- **Data Visualization:** Chart.js

## 🚀 How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/EcoSort-AI.git
   cd EcoSort-AI

   Create and activate a virtual environment:

2. bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
Install dependencies:

3. bash
pip install -r requirements.txt
Run the Flask App:

4. bash
python app.py
Open http://127.0.0.1:5000 in your browser.
