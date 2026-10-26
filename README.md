# ♻️ EcoSort AI: Smart Waste Segregation & Disposal System

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-yellow.svg)
![License](https://img.shields.io/badge/License-MIT-purple.svg)

**EcoSort AI** is a software-only, AI-powered web application designed to bridge the gap between waste identification and correct disposal practices. Aligned with **UN Sustainable Development Goals SDG 11 (Sustainable Cities and Communities) and SDG 12 (Responsible Consumption and Production)**, the platform helps users identify waste and make informed disposal decisions using a simple web interface, without requiring expensive hardware.

## ✨ Key Features

- **Multi-Item Detection:** Uses a YOLOv8 model to detect multiple waste items in a single image.
- **6-Class Material Mapping:** Maps 18 raw waste classes into six disposal categories: Cardboard, Glass, Metal, Paper, Plastic, and Trash.
- **EcoScore Metric:** Calculates a sustainability score from 0 to 100 based on the recyclability of detected materials, encouraging responsible waste disposal.
- **Smart Disposal Guidance:** Provides actionable bin-color recommendations to help users segregate waste correctly.
- **DIY Upcycling Ideas:** Suggests creative ways to reuse suitable waste materials and support a circular economy.
- **Dark Mode:** Provides a persistent dark mode toggle for a personalized browsing experience.
- **Analytics Dashboard:** Uses interactive Chart.js visualizations to display waste detection statistics and sustainability insights.
- **Responsive Interface:** Features a modern glassmorphism-inspired UI designed for different screen sizes.

## 🛠️ Technology Stack

| Category | Technologies |
|---|---|
| Machine Learning | YOLOv8s, Ultralytics, PyTorch |
| Dataset | TACO Dataset |
| Backend | Python, Flask |
| Templating | Jinja2 |
| Frontend | HTML5, Vanilla JavaScript, CSS3 |
| Data Visualization | Chart.js |
| Interface Design | Responsive UI, Glassmorphism, Dark Mode |

## 🏗️ System Architecture

```text
              User
               |
               v
       Web Application
      HTML, CSS, JavaScript
               |
               v
          Flask Backend
               |
               v
       YOLOv8 Detection Model
               |
               v
       Waste Classification
               |
               v
      Material Category Mapping
               |
               v
       EcoScore Calculation
               |
               v
    Disposal & Upcycling Guidance
               |
               v
       Results and Analytics
```

## 🚀 How to Run Locally

Follow these steps to set up and run EcoSort AI on your local machine.

### Prerequisites

Ensure you have the following installed:

- Python 3.10 or later
- pip (Python package manager)
- Git
- A code editor such as Visual Studio Code

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/EcoSort-AI.git
cd EcoSort-AI
```

Replace `YOUR_USERNAME` with your GitHub username or use your actual repository URL.

### 2. Create and Activate a Virtual Environment

**Windows (PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**

```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

If the project does not contain a `requirements.txt` file, create one containing the dependencies actually used by your application, such as Flask, Ultralytics, and PyTorch.

### 4. Configure the Model

Ensure the trained YOLOv8 model weights are available at the path expected by your Flask application.

For example, if your application loads a file named `best.pt`, verify that the file exists in the configured model directory.

> Note: The trained model weights must be supplied separately if they are not included in the repository.

### 5. Run the Flask Application

Start the application using:

```bash
python app.py
```

Once the Flask server starts successfully, open the following URL in your browser:

**http://127.0.0.1:5000**

You can now upload a waste image and explore the available detection, classification, disposal guidance, and analytics features.

## 📂 Project Structure

A suggested project structure is shown below. Adapt the paths to match your actual implementation.

```text
EcoSort-AI/
│
├── app.py
├── requirements.txt
├── README.md
│
├── models/
│   └── best.pt
│
├── templates/
│   ├── index.html
│   └── ...
│
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── script.js
│   └── images/
│
├── uploads/
│
└── venv/
```

> The `models/`, `uploads/`, and other directory names are illustrative. Use the actual folder structure expected by your code. Avoid committing virtual environments, temporary uploads, or unnecessarily large model files to GitHub.

## ♻️ Waste Classification Categories

EcoSort AI maps detected waste classes into six broader disposal categories.

| Category | Example Materials |
|---|---|
| Cardboard | Packaging boxes, cardboard containers |
| Glass | Glass bottles, jars |
| Metal | Metal cans, scrap metal |
| Paper | Newspapers, paper sheets |
| Plastic | Plastic bottles, packaging |
| Trash | Non-recyclable or miscellaneous waste |

The final classification depends on the classes supported by the trained model. Actual disposal requirements may vary by local waste-management guidelines.

## 🌍 Sustainable Development Goals

EcoSort AI supports the following United Nations Sustainable Development Goals:

- **SDG 11 – Sustainable Cities and Communities:** Encourages cleaner communities through improved waste segregation and responsible disposal practices.
- **SDG 12 – Responsible Consumption and Production:** Promotes recycling, material reuse, and waste reduction through informed disposal decisions.

## 🔮 Future Enhancements

Potential future improvements include:

- Expand the waste detection model with additional material classes.
- Improve model accuracy using a larger and more diverse dataset.
- Add user accounts and personalized waste-management history.
- Generate downloadable PDF reports containing detection results and impact statistics.
- Integrate location-aware waste collection and recycling facility information.
- Add multilingual support for broader accessibility.
- Improve EcoScore calculations using transparent, category-specific sustainability rules.
- Deploy the application to a cloud hosting platform.

## ⚠️ Limitations

- Detection accuracy depends on image quality, lighting, object overlap, and model training.
- Waste classification is limited to the categories supported by the trained model.
- Bin-color recommendations should be adapted to local waste-management rules.
- The EcoScore is an application-defined sustainability metric, not an official environmental certification.
- The application requires a compatible Python environment and trained model weights.

## 🎯 Conclusion

EcoSort AI demonstrates how computer vision and web technologies can help make waste identification and segregation more accessible. By combining multi-item detection, material classification, disposal recommendations, and sustainability analytics, the project aims to encourage responsible waste-management habits and support a cleaner, more sustainable environment.

---

**Built with ♻️ Python, Flask, YOLOv8, PyTorch, HTML, CSS, JavaScript, and Chart.js.**

