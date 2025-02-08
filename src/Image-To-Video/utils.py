import os
import re
import base64
import time
from tqdm import tqdm
import fitz
from PIL import Image
import subprocess

def setup_directories():
    for d in ["uploads", "output/images", "output/scripts", "output/audio", "static"]:
        os.makedirs(d, exist_ok=True)

def clean_directories(keep_video=None):
    """clean up temporary files."""
    for d, ext in [
        ("uploads", ".pdf"),
        ("output/images", ".png"),
        ("output/scripts", ".txt"),
        ("output/audio", ".mp3")
    ]:
        if os.path.exists(d):
            for f in os.listdir(d):
                if f.endswith(ext):
                    os.remove(os.path.join(d, f))

    if os.path.exists("static"):
        for f in os.listdir("static"):
            full_path = os.path.join("static", f)
            if f.startswith("video_") and f.endswith(".mp4"):
                if keep_video and os.path.abspath(full_path) == os.path.abspath(keep_video):
                    continue
                os.remove(full_path)

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def natural_sort_key(s):
    """for sorting 'page_1.png', 'page_2.png', etc."""
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(r'(\d+)', s)]

def convert_pdf_to_images(pdf_path):
    images_dir = "output/images"
    os.makedirs(images_dir, exist_ok=True)

    pdf_document = fitz.open(pdf_path)
    for page_number in tqdm(range(pdf_document.page_count), desc="Converting PDF pages"):
        page = pdf_document[page_number]
        zoom = 300 / 72
        matrix = fitz.Matrix(zoom, zoom)
        pixmap = page.get_pixmap(matrix=matrix)
        img_data = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)
        output_path = os.path.join(images_dir, f'page_{page_number + 1}.png')
        img_data.save(output_path, 'PNG')
    
    pdf_document.close()
    return images_dir

def get_audio_duration(audio_path):
    """get audio duration using ffprobe."""
    result = subprocess.run(
        ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
         '-of', 'default=noprint_wrappers=1:nokey=1', audio_path],
        capture_output=True,
        text=True
    )
    return float(result.stdout.strip()) if result.stdout.strip() else 0.0

def get_sorted_pairs(images_dir, audio_dir):
    """match images with audio files."""
    images = sorted([f for f in os.listdir(images_dir) if f.endswith(".png")],
                    key=lambda x: int(re.search(r'page_(\d+)', x).group(1)))
    audio_files = sorted([f for f in os.listdir(audio_dir) if f.endswith(".mp3")],
                         key=lambda x: int(re.search(r'slide_(\d+)', x).group(1)))

    return [(os.path.join(images_dir, img), os.path.join(audio_dir, aud))
            for img, aud in zip(images, audio_files)
            if int(re.search(r'page_(\d+)', img).group(1)) == 
               int(re.search(r'slide_(\d+)', aud).group(1))]