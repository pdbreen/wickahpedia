import os
import shutil
from datetime import datetime

SOURCE_DIR = "content/articles"
TARGET_DIR = "content/published"

def publish_today_article():
    files = sorted(os.listdir(SOURCE_DIR))
    if not files:
        print("No more articles to publish.")
        return

    today = datetime.now().strftime('%Y-%m-%d')
    article = files[0]
    new_filename = f"{today}-{article}"
    shutil.move(os.path.join(SOURCE_DIR, article), os.path.join(TARGET_DIR, new_filename))
    print(f"Published: {new_filename}")

if __name__ == "__main__":
    publish_today_article()
