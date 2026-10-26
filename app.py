import os
import json
import uuid
from datetime import datetime

try:
    import pillow_heif
    pillow_heif.register_heif_opener()
    HEIF_SUPPORTED = True
except ImportError:
    HEIF_SUPPORTED = False

from flask import Flask, render_template, request, redirect, url_for, jsonify
from PIL import Image

from utils.detector import detect_objects, draw_boxes
from utils.disposal import summarize, get_disposal_info
from utils.scoring import compute_eco_score


app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
OUTPUT_FOLDER = "static/output"
HISTORY_FILE = "data/history.json"
ALLOWED_EXT = {"png", "jpg", "jpeg", "webp", "heic", "heif"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024


def ensure_folders():
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "w") as f:
            json.dump([], f)


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT


def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except Exception:
        return []


def save_history(record):
    ensure_folders()
    history = load_history()
    history.append(record)
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)


def load_history_sorted():
    history = load_history()
    return sorted(history, key=lambda h: h.get("timestamp", ""), reverse=True)


ensure_folders()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return redirect(url_for("index"))

    file = request.files["image"]
    if file.filename == "" or not allowed_file(file.filename):
        return redirect(url_for("index"))

    ensure_folders()

    ext = file.filename.rsplit(".", 1)[1].lower()
    uid = uuid.uuid4().hex
    raw_name = f"{uid}.{ext}"
    raw_path = os.path.join(UPLOAD_FOLDER, raw_name)
    file.save(raw_path)

    try:
        image = Image.open(raw_path).convert("RGB")
    except Exception as e:
        print(f"[predict] Could not open image: {e}")
        return redirect(url_for("index"))

    jpg_name = f"{uid}.jpg"
    jpg_path = os.path.join(UPLOAD_FOLDER, jpg_name)
    image.save(jpg_path, "JPEG", quality=90)

    detections = detect_objects(image)
    summary = summarize(detections)
    eco = compute_eco_score(detections)

    annotated = draw_boxes(image, detections)
    annotated_name = f"{uid}_annotated.jpg"
    annotated_path = os.path.join(OUTPUT_FOLDER, annotated_name)
    annotated.save(annotated_path, "JPEG", quality=90)

    record = {
        "id": uid,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "filename": jpg_name,
        "annotated": annotated_name,
        "num_items": len(detections),
        "materials": {label: data["count"] for label, data in summary.items()},
        "eco_score": eco["score"],
        "grade": eco["grade"],
    }
    save_history(record)

    return render_template(
        "result.html",
        image_url=f"/static/uploads/{jpg_name}",
        annotated_url=f"/static/output/{annotated_name}",
        detections=detections,
        summary=summary,
        eco=eco,
        num_items=len(detections),
        scan_id=uid,
    )


@app.route("/dashboard")
def dashboard():
    history = load_history_sorted()
    total_scans = len(history)
    total_items = sum(h.get("num_items", 0) for h in history)

    material_totals = {}
    for h in history:
        for label, count in h.get("materials", {}).items():
            material_totals[label] = material_totals.get(label, 0) + count

    avg_score = round(
        sum(h.get("eco_score", 0) for h in history) / total_scans, 1
    ) if total_scans else 0

    return render_template(
        "dashboard.html",
        history=history,
        total_scans=total_scans,
        total_items=total_items,
        material_totals=material_totals,
        avg_score=avg_score,
    )


@app.route("/history")
def history_view():
    history = load_history_sorted()
    return render_template("history.html", history=history)


@app.route("/scan/<scan_id>")
def scan_detail(scan_id):
    history = load_history()
    record = next((h for h in history if h.get("id") == scan_id), None)
    if not record:
        return redirect(url_for("history_view"))

    summary = {}
    for mat, cnt in record.get("materials", {}).items():
        info = get_disposal_info(mat)
        summary[mat] = {"count": cnt, **info}

    return render_template("scan_detail.html", record=record, summary=summary)


@app.route("/delete/<scan_id>", methods=["POST"])
def delete_scan(scan_id):
    history = load_history()
    record = next((h for h in history if h.get("id") == scan_id), None)

    if record:
        for key, folder in [("filename", UPLOAD_FOLDER), ("annotated", OUTPUT_FOLDER)]:
            fname = record.get(key)
            if fname:
                fpath = os.path.join(folder, fname)
                if os.path.exists(fpath):
                    try:
                        os.remove(fpath)
                    except Exception as e:
                        print(f"[delete] Could not remove {fpath}: {e}")

        history = [h for h in history if h.get("id") != scan_id]
        with open(HISTORY_FILE, "w") as f:
            json.dump(history, f, indent=2)

    ref = request.referrer or url_for("history_view")
    return redirect(ref)

@app.route("/guide")
def guide():
    from utils.disposal import DISPOSAL_MAP
    return render_template("guide.html", materials=DISPOSAL_MAP)

@app.route("/api/stats")
def api_stats():
    return jsonify({"total_scans": len(load_history()), "history": load_history()})


@app.route("/reset", methods=["POST"])
def reset():
    ensure_folders()
    with open(HISTORY_FILE, "w") as f:
        json.dump([], f)
    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    ensure_folders()
    print("=" * 50)
    print("  EcoSort AI — starting up")
    print(f"  HEIC support: {'enabled' if HEIF_SUPPORTED else 'not installed'}")
    print("=" * 50)
    app.run(debug=True, port=5000)