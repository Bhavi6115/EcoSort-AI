DISPOSAL_MAP = {
    "cardboard": {
        "bin": "Blue — Dry Recyclable",
        "color": "#2563eb",
        "recyclable": True,
        "instruction": "Flatten and place in dry recyclable bin.",
        "tip": "Remove tape and staples before disposal.",
        "diy_idea": "Cut into strips to make a magazine holder or photo frame.",
    },
    "paper": {
        "bin": "Blue — Dry Recyclable",
        "color": "#2563eb",
        "recyclable": True,
        "instruction": "Keep dry, place in paper recycling bin.",
        "tip": "Avoid greasy or wet paper — it contaminates the batch.",
        "diy_idea": "Shred and soak to make handmade paper or paper-mâché crafts.",
    },
    "plastic": {
        "bin": "Red — Non-Biodegradable",
        "color": "#dc2626",
        "recyclable": True,
        "instruction": "Rinse and drop into plastic recycling bin.",
        "tip": "Check the resin code (PET, HDPE) for better sorting.",
        "diy_idea": "Cut bottle in half → self-watering planter. Or make a pencil stand.",
    },
    "glass": {
        "bin": "Green — Glass",
        "color": "#16a34a",
        "recyclable": True,
        "instruction": "Handle carefully, place in glass bin.",
        "tip": "Do not mix broken glass with general waste.",
        "diy_idea": "Clean jar → candle holder, spice jar, or mini terrarium.",
    },
    "metal": {
        "bin": "Yellow — Metal",
        "color": "#eab308",
        "recyclable": True,
        "instruction": "Rinse and place in metal recycling bin.",
        "tip": "Crush cans to save space.",
        "diy_idea": "Tin can → lantern with holes, or painted pencil holder.",
    },
    "trash": {
        "bin": "Black — General Waste",
        "color": "#111827",
        "recyclable": False,
        "instruction": "Dispose in general waste bin.",
        "tip": "Consider if any part can be recycled separately.",
        "diy_idea": "Separate any recyclable parts before disposal to reduce landfill waste.",
    },
}


def get_disposal_info(label: str):
    return DISPOSAL_MAP.get(label.lower(), {
        "bin": "Unknown",
        "color": "#6b7280",
        "recyclable": False,
        "instruction": "No disposal info available.",
        "tip": "Please check local guidelines.",
        "diy_idea": "No DIY idea available.",
    })


def summarize(detections):
    summary = {}
    for d in detections:
        label = d["label"]
        if label not in summary:
            summary[label] = {
                "count": 0,
                "total_confidence": 0.0,
                **get_disposal_info(label),
            }
        summary[label]["count"] += 1
        summary[label]["total_confidence"] += d["confidence"]

    for label, data in summary.items():
        data["avg_confidence"] = round(data["total_confidence"] / data["count"], 3)
        del data["total_confidence"]

    return summary