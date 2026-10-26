from utils.disposal import DISPOSAL_MAP

MATERIAL_WEIGHT = {
    "metal":     1.0,
    "glass":     0.9,
    "paper":     0.85,
    "cardboard": 0.8,
    "plastic":   0.75,
    "trash":     0.2,
}


def compute_eco_score(detections):
    if not detections:
        return {
            "score": 0, "grade": "N/A",
            "recyclable_count": 0, "non_recyclable_count": 0,
            "message": "No items detected.",
        }

    total = 0.0
    recyclable = 0
    non_recyclable = 0

    for d in detections:
        w = MATERIAL_WEIGHT.get(d["label"], 0.5)
        total += w * d["confidence"]

        if DISPOSAL_MAP.get(d["label"], {}).get("recyclable", False):
            recyclable += 1
        else:
            non_recyclable += 1

    score = round((total / len(detections)) * 100, 1)

    if score >= 80:
        grade, msg = "A", "Excellent! Highly recyclable batch."
    elif score >= 60:
        grade, msg = "B", "Good — most items are recyclable."
    elif score >= 40:
        grade, msg = "C", "Mixed batch — separate recyclables next time."
    else:
        grade, msg = "D", "Low recyclability — mostly general waste."

    return {
        "score": score, "grade": grade,
        "recyclable_count": recyclable,
        "non_recyclable_count": non_recyclable,
        "message": msg,
    }