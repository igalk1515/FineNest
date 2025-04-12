import pytesseract
from PIL import Image, ImageSequence

TESSERACT_CONFIG = "--oem 3 --psm 6"

LANGUAGES = {
    "eng": "eng",
    "heb_eng": "heb+eng",
    "heb": "heb"
}

def extract_text_from_image_file(file_path, max_pages=None):
    selected_languages = ["eng", "heb_eng", "heb"]

    text_results = {lang_key: [] for lang_key in selected_languages}

    def extract_from_image(image):
        for lang_key in selected_languages:
            text = pytesseract.image_to_string(
                image,
                lang=LANGUAGES[lang_key],
                config=TESSERACT_CONFIG
            )
            text_results[lang_key].append(text)

    with Image.open(file_path) as img:
        if getattr(img, "n_frames", 1) > 1:
            frames = list(ImageSequence.Iterator(img))
            for i, page in enumerate(frames, start=1):
                if max_pages and i > max_pages:
                    break
                extract_from_image(page)
        else:
            extract_from_image(img)

    return {
        f"text_{lang}": "\n".join(text_results[lang]).strip()
        for lang in selected_languages
    }
