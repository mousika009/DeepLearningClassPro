import json
from pathlib import Path

from PIL import Image, ImageDraw

# Project directory
root = Path(__file__).resolve().parent

image_dir = root / "data" / "idd" / "images"
ann_dir = root / "data" / "idd" / "annotations"

image_dir.mkdir(parents=True, exist_ok=True)
ann_dir.mkdir(parents=True, exist_ok=True)

# Categories
categories = [
    {"id": 1, "name": "car", "supercategory": "vehicle"},
    {"id": 2, "name": "motorcycle", "supercategory": "vehicle"},
    {"id": 3, "name": "pedestrian", "supercategory": "person"},
    {"id": 4, "name": "bus", "supercategory": "vehicle"},
    {"id": 5, "name": "truck", "supercategory": "vehicle"},
    {"id": 6, "name": "traffic_cone", "supercategory": "object"},
]

# Images
images = [
    {"id": 1, "file_name": "traffic_001.jpg", "width": 1280, "height": 720},
    {"id": 2, "file_name": "traffic_002.jpg", "width": 1280, "height": 720},
    {"id": 3, "file_name": "traffic_003.jpg", "width": 1280, "height": 720},
]

# Bounding boxes: [x, y, width, height]
annotations = [
    # Image 1
    {"id": 1, "image_id": 1, "category_id": 1,
     "bbox": [100, 180, 260, 150], "area": 39000, "iscrowd": 0},

    {"id": 2, "image_id": 1, "category_id": 3,
     "bbox": [500, 200, 60, 160], "area": 9600, "iscrowd": 0},

    {"id": 3, "image_id": 1, "category_id": 2,
     "bbox": [700, 300, 120, 140], "area": 16800, "iscrowd": 0},

    # Image 2
    {"id": 4, "image_id": 2, "category_id": 4,
     "bbox": [200, 150, 400, 300], "area": 120000, "iscrowd": 0},

    {"id": 5, "image_id": 2, "category_id": 5,
     "bbox": [800, 250, 300, 200], "area": 60000, "iscrowd": 0},

    # Image 3
    # Image 3
    {"id": 6, "image_id": 3, "category_id": 1,
     "bbox": [100, 180, 260, 150], "area": 39000, "iscrowd": 0},

    {"id": 7, "image_id": 3, "category_id": 2,
     "bbox": [700, 300, 120, 140], "area": 16800, "iscrowd": 0},

    {"id": 8, "image_id": 3, "category_id": 4,
     "bbox": [400, 100, 250, 200], "area": 50000, "iscrowd": 0},

    {"id": 9, "image_id": 3, "category_id": 6,
     "bbox": [950, 400, 150, 120], "area": 18000, "iscrowd": 0},
]

# Colors for each category
fill = {
    1: (120, 120, 200),  # Blue - Car
    2: (120, 200, 120),  # Green - Motorcycle
    3: (200, 160, 100),  # Orange - Pedestrian
    4: (200, 120, 120),  # Red - Bus
    5: (150, 150, 150),  # Gray - Truck
    6: (180, 100, 220),  # Purple - Traffic cone
}

# Generate images with bounding boxes
for info in images:

    canvas = Image.new(
        "RGB",
        (info["width"], info["height"]),
        (225, 225, 225)
    )

    draw = ImageDraw.Draw(canvas)

    for a in annotations:

        if a["image_id"] == info["id"]:

            x, y, w, h = a["bbox"]

            draw.rectangle(
                [x, y, x + w, y + h],
                fill=fill[a["category_id"]]
            )

    canvas.save(image_dir / info["file_name"])

# Save COCO JSON annotations
with open(ann_dir / "instances.json", "w", encoding="utf-8") as f:

    json.dump(
        {
            "images": images,
            "categories": categories,
            "annotations": annotations
        },
        f,
        indent=2
    )

print("========== DATASET CREATED ==========")
print("Total images:", len(images))
print("Total categories:", len(categories))
print("Total bounding boxes:", len(annotations))
print("New purple bounding box added!")
print("Image folder:", image_dir)
print("Annotation file:", ann_dir / "instances.json")

print("\nReminder: This is synthetic teaching data,")
print("not the official IDD dataset.")