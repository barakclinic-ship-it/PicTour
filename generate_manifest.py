"""
סקריפט ליצירת manifest.json מתוך תיקיית images עם תת-תיקיות לפי נושא.

מבנה תיקיות לדוגמה:
  quiza-anatomy/
    generate_manifest.py
    images/
      nerves/
        ulnar nerve.png
        median nerve.png
      muscles/
        soleus.PNG
        femoral artery.PNG

שימוש:
  python3 generate_manifest.py

יווצר manifest.json בתיקייה הראשית.
"""

import json, os, sys

IMAGES_DIR = "images"
OUTPUT_FILE = "manifest.json"
VALID_EXT = {".jpg", ".jpeg", ".png", ".gif", ".webp"}

def make_name(filename):
    base = os.path.splitext(filename)[0]
    return base.replace("_", " ").replace("-", " ").strip()

def main():
    if not os.path.isdir(IMAGES_DIR):
        print(f"Error: folder '{IMAGES_DIR}' not found.")
        sys.exit(1)

    topics = []

    # סרוק תת-תיקיות (נושאים)
    subdirs = sorted(
        d for d in os.listdir(IMAGES_DIR)
        if os.path.isdir(os.path.join(IMAGES_DIR, d)) and not d.startswith('.')
    )

    # תמונות ישירות בתוך images/ (בלי תת-תיקייה) → נושא "General"
    root_files = sorted(
        f for f in os.listdir(IMAGES_DIR)
        if os.path.isfile(os.path.join(IMAGES_DIR, f))
        and os.path.splitext(f)[1].lower() in VALID_EXT
    )
    if root_files:
        topics.append({
            "name": "General",
            "images": [{"file": f, "name": make_name(f)} for f in root_files]
        })

    for subdir in subdirs:
        subdir_path = os.path.join(IMAGES_DIR, subdir)
        files = sorted(
            f for f in os.listdir(subdir_path)
            if os.path.isfile(os.path.join(subdir_path, f))
            and os.path.splitext(f)[1].lower() in VALID_EXT
        )
        if files:
            topics.append({
                "name": subdir,
                "images": [{"file": f"{subdir}/{f}", "name": make_name(f)} for f in files]
            })

    if not topics:
        print("Error: no images found.")
        sys.exit(1)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump({"topics": topics}, f, ensure_ascii=False, indent=2)

    total = sum(len(t["images"]) for t in topics)
    print(f"Created {OUTPUT_FILE}: {len(topics)} topics, {total} images total.")
    for t in topics:
        print(f"  - {t['name']}: {len(t['images'])} images")

if __name__ == "__main__":
    main()
