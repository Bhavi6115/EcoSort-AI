import torch
import torch.serialization
from ultralytics.nn.tasks import DetectionModel

# --- PyTorch 2.6+ compatibility fix ---
torch.serialization.add_safe_globals([DetectionModel])
# --------------------------------------

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from ultralytics import YOLO

# Load the retrained 18-class model
model = YOLO("model/best_v2.pt")

# 18 TACO classes — order MUST match data_v2.yaml
TACO_NAMES = [
    'Aluminium foil', 'Bottle cap', 'Bottle', 'Broken glass',
    'Can', 'Carton', 'Cigarette', 'Cup', 'Lid', 'Other litter',
    'Other plastic', 'Paper', 'Plastic bag - wrapper',
    'Plastic container', 'Pop tab', 'Straw',
    'Styrofoam piece', 'Unlabeled litter'
]

# Map 18 TACO sub-classes → 6 disposal categories
TACO_TO_MATERIAL = {
    'Aluminium foil':        'metal',
    'Bottle cap':            'plastic',   # most caps on waste bottles are plastic
    'Bottle':                'plastic',
    'Broken glass':          'glass',
    'Can':                   'metal',
    'Carton':                'cardboard',
    'Cigarette':             'trash',
    'Cup':                   'plastic',
    'Lid':                   'plastic',
    'Other litter':          'trash',
    'Other plastic':         'plastic',
    'Paper':                 'paper',
    'Plastic bag - wrapper': 'plastic',
    'Plastic container':     'plastic',
    'Pop tab':               'metal',
    'Straw':                 'plastic',
    'Styrofoam piece':       'trash',
    'Unlabeled litter':      'trash',
}

# Box colors per disposal category (RGBA)
BOX_COLORS = {
    "cardboard": (180, 120, 60, 255),
    "glass":     (0, 180, 180, 255),
    "metal":     (200, 200, 60, 255),
    "paper":     (60, 120, 220, 255),
    "plastic":   (220, 60, 60, 255),
    "trash":     (80, 80, 80, 255),
}


def detect_objects(image: Image.Image, conf_threshold: float = 0.20):
    """
    Run YOLOv8 (18-class TACO model) on a PIL image.
    Returns list of detections: [{bbox, label, taco_label, confidence}, ...]
    """
    img_array = np.array(image)
    results = model(img_array, conf=conf_threshold, iou=0.45, verbose=False)

    img_h, img_w = img_array.shape[:2]
    img_area = img_h * img_w
    min_area = img_area * 0.004   # ignore tiny noise boxes

    raw = []
    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int).tolist()
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])

            if cls_id >= len(TACO_NAMES):
                continue

            taco_name = TACO_NAMES[cls_id]
            material = TACO_TO_MATERIAL.get(taco_name, "trash")

            area = (x2 - x1) * (y2 - y1)
            if area < min_area:
                continue

            raw.append({
                "bbox": [x1, y1, x2, y2],
                "label": material,
                "taco_label": taco_name,
                "confidence": round(conf, 3),
            })

    # Deduplicate heavily-overlapping boxes (keep highest confidence)
    def iou(a, b):
        ax1, ay1, ax2, ay2 = a
        bx1, by1, bx2, by2 = b
        ix1, iy1 = max(ax1, bx1), max(ay1, by1)
        ix2, iy2 = min(ax2, bx2), min(ay2, by2)
        iw, ih = max(0, ix2 - ix1), max(0, iy2 - iy1)
        inter = iw * ih
        ua = (ax2-ax1)*(ay2-ay1) + (bx2-bx1)*(by2-by1) - inter
        return inter / ua if ua > 0 else 0

    keep = []
    for d in sorted(raw, key=lambda x: -x["confidence"]):
        if not any(iou(d["bbox"], k["bbox"]) > 0.55 for k in keep):
            keep.append(d)

    return keep


def draw_boxes(image: Image.Image, detections):
    """
    Draw high-contrast bounding boxes with material labels + confidence.
    """
    annotated = image.copy()
    draw = ImageDraw.Draw(annotated, "RGBA")

    img_w, img_h = annotated.size
    font_size = max(18, int(img_h * 0.028))
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except Exception:
        try:
            font = ImageFont.truetype("DejaVuSans-Bold.ttf", font_size)
        except Exception:
            font = ImageFont.load_default()

    for d in detections:
        x1, y1, x2, y2 = d["bbox"]
        label = d["label"]
        conf = d["confidence"]
        color = BOX_COLORS.get(label, (0, 0, 0, 255))

        # Thick border
        border_w = max(4, int(img_h * 0.005))
        for w in range(border_w):
            draw.rectangle([x1 - w, y1 - w, x2 + w, y2 + w], outline=color)

        # Label text — just material + confidence (no confusing sub-label)
        text = f"{label.upper()}  {int(conf * 100)}%"

        tb = draw.textbbox((0, 0), text, font=font)
        text_w = tb[2] - tb[0]
        text_h = tb[3] - tb[1]

        pad_x, pad_y = 12, 8
        label_w = text_w + pad_x * 2
        label_h = text_h + pad_y * 2

        # Position label above box (or inside if no room)
        label_y = y1 - label_h - 6
        if label_y < 0:
            label_y = y1 + 6
        label_x = x1
        if label_x + label_w > img_w:
            label_x = img_w - label_w - 6
        if label_x < 0:
            label_x = 0

        # Solid colored background
        draw.rectangle(
            [label_x, label_y, label_x + label_w, label_y + label_h],
            fill=color,
        )

        # White text
        draw.text(
            (label_x + pad_x, label_y + pad_y - 2),
            text,
            fill=(255, 255, 255, 255),
            font=font,
        )

        # Confidence bar under the box
        bar_h = max(5, int(img_h * 0.006))
        bar_w = int((x2 - x1) * conf)
        if bar_w > 0:
            draw.rectangle([x1, y2 + 4, x1 + bar_w, y2 + 4 + bar_h], fill=color)

    return annotated 