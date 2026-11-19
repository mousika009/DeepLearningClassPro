
from pathlib import Path
import json
from collections import defaultdict, Counter
from PIL import Image, ImageDraw

# ==================================================
# 1. FIND PROJECT DIRECTORY
# ==================================================

project_dir = Path(__file__).resolve().parent

# ==================================================
# 2. LOCATE ANNOTATION FILE
# ==================================================

json_path = (
    project_dir / "data" / "idd" /
    "annotations" / "instances.json"
)

image_dir = project_dir / "data" / "idd" / "images"

output_dir = project_dir / "docs"
output_dir.mkdir(parents=True, exist_ok=True)

# ==================================================
# 3. LOAD JSON FILE
# ==================================================

if not json_path.exists():
    raise FileNotFoundError(f"JSON file not found: {json_path}")

with open(json_path, "r", encoding="utf-8") as file:
    coco = json.load(file)

print("COCO JSON loaded successfully!")

# ==================================================
# 4. READ THREE MAIN SECTIONS
# ==================================================

images = coco["images"]
categories = coco["categories"]
annotations = coco["annotations"]

# ==================================================
# 5. DATASET SUMMARY
# ==================================================

print("\nDATASET SUMMARY")

print("Images:", len(images))
print("Categories:", len(categories))
print("Annotations:", len(annotations))

# ==================================================
# 6. AVAILABLE CATEGORIES
# ==================================================

print("\nAVAILABLE CATEGORIES")

for category in categories:
    print(category["id"], ":", category["name"])

# ==================================================
# 7. IMAGE INFORMATION
# ==================================================

print("\nIMAGE INFORMATION")

for image in images:
    print(
        "Image ID:", image["id"],
        "| File:", image["file_name"],
        "| Width:", image["width"],
        "| Height:", image["height"]
    )

# ==================================================
# 8. OBJECT ANNOTATIONS
# ==================================================

print("\nOBJECT ANNOTATIONS")

for annotation in annotations:
    print(
        "Annotation ID:", annotation["id"],
        "| Image ID:", annotation["image_id"],
        "| Category ID:", annotation["category_id"],
        "| Bounding Box:", annotation["bbox"]
    )

# ==================================================
# 9. IMAGE AND CATEGORY MAPPING
# ==================================================

category_names = {
    category["id"]: category["name"]
    for category in categories
}

annotations_by_image = defaultdict(list)

for annotation in annotations:
    annotations_by_image[annotation["image_id"]].append(annotation)

# ==================================================
# 10. IMAGE FILE INFORMATION
# ==================================================

print("\nAVAILABLE IMAGE FILES")

for image_info in images:

    candidate = image_dir / image_info["file_name"]

    print(
        "ID:", image_info["id"],
        "| File:", image_info["file_name"],
        "| Exists:", candidate.exists(),
        "| Annotations:",
        len(annotations_by_image[image_info["id"]])
    )

# ==================================================
# 11. DRAW BOTH IMAGES
# ==================================================

TARGET_IMAGE_IDS = [1, 2 , 3,10]

print("\nDRAWING")

for target_id in TARGET_IMAGE_IDS:

    selected_image = None

    for image_info in images:

        if image_info["id"] != target_id:
            continue

        candidate = image_dir / image_info["file_name"]

        if candidate.exists() and annotations_by_image[target_id]:
            selected_image = image_info
            break

    if selected_image is None:
        print(f"Image ID {target_id} not found or has no annotations.")
        continue

    image_path = image_dir / selected_image["file_name"]

    image = Image.open(image_path).convert("RGB")

    draw = ImageDraw.Draw(image)

    image_annotations = annotations_by_image[target_id]

    # Image 1: Draw only two bounding boxes
    if target_id == 1:
        image_annotations = image_annotations[:2]

    # Image 2: Draw all its bounding boxes
    for annotation in image_annotations:

        x, y, width, height = annotation["bbox"]

        x1 = x
        y1 = y
        x2 = x + width
        y2 = y + height

        label = category_names.get(
            annotation["category_id"],
            "Unknown"
        )

        draw.rectangle(
            [x1, y1, x2, y2],
            outline="red",
            width=3
        )

        label_position = (
            int(x1),
            max(0, int(y1) - 15)
        )

        draw.rectangle(
            draw.textbbox(label_position, label),
            fill="red"
        )

        draw.text(
            label_position,
            label,
            fill="white"
        )

    output_path = (
        output_dir / f"coco_preview_{target_id}.jpg"
    )

    image.save(output_path)

    print("Preview saved to:", output_path)

# ==================================================
# 12. OBJECTS PER CATEGORY
# ==================================================

print("\nOBJECTS PER CATEGORY")

category_counts = Counter(
    a["category_id"] for a in annotations
)

for category_id, name in category_names.items():

    print(
        f"{category_id:>3} : {name:<12} "
        f"{category_counts.get(category_id, 0)}"
    )

# ==================================================
# 13. IMAGES WITH AND WITHOUT ANNOTATIONS
# ==================================================

print("\nImages with annotations   :",
      sum(
          1 for im in images
          if annotations_by_image.get(im["id"])
      )
)

print("Images without annotations:",
      sum(
          1 for im in images
          if not annotations_by_image.get(im["id"])
      )
)

# ==================================================
# 14. VERIFICATION CHECKS
# ==================================================

image_by_id = {
    image["id"]: image
    for image in images
}

bad_image = [
    a["id"]
    for a in annotations
    if a["image_id"] not in image_by_id
]

bad_category = [
    a["id"]
    for a in annotations
    if a["category_id"] not in category_names
]

bad_size = [
    a["id"]
    for a in annotations
    if (
        a["bbox"][2] <= 0
        or a["bbox"][3] <= 0
    )
]

outside = [
    a["id"]
    for a in annotations
    if a["image_id"] in image_by_id and (
        a["bbox"][0] < 0
        or a["bbox"][1] < 0
        or a["bbox"][0] + a["bbox"][2] >
        image_by_id[a["image_id"]]["width"]
        or a["bbox"][1] + a["bbox"][3] >
        image_by_id[a["image_id"]]["height"]
    )
]

# ==================================================
# 15. DEBUGGING MISSING IMAGE REFERENCES
# ==================================================

print("\nDEBUGGING MISSING IMAGE REFERENCES")

for annotation in annotations:

    if annotation["image_id"] not in image_by_id:

        print(
            "Annotation ID:", annotation["id"],
            "| Refers to Image ID:", annotation["image_id"],
            "| Category ID:", annotation["category_id"]
        )

print("\nAVAILABLE IMAGE IDs")

for image in images:
    print(
        image["id"],
        ":",
        image["file_name"]
    )

# ==================================================
# 16. PRINT VERIFICATION RESULTS
# ==================================================

print("\nVERIFICATION CHECKS")

checks = [
    (
        "Every annotation points to an existing image",
        bad_image
    ),
    (
        "Every annotation points to an existing category",
        bad_category
    ),
    (
        "Every box has width > 0 and height > 0",
        bad_size
    ),
    (
        "Every box lies inside its image",
        outside
    )
]

for check_name, bad_ids in checks:

    result = (
        "PASS"
        if not bad_ids
        else f"FAIL {bad_ids[:5]}"
    )

    print(f"{check_name:<50} {result}")

# ==================================================
# 17. FINAL STATUS
# ==================================================

print("\nCOCO DATASET EXPLORATION COMPLETED!")

