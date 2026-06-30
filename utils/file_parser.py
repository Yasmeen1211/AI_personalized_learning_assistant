from pypdf import PdfReader

from PIL import Image

import pytesseract

import tempfile

import os


# -----------------------------------
# OPTIONAL:
# SET TESSERACT PATH FOR WINDOWS
# -----------------------------------

# Uncomment and update if needed

# pytesseract.pytesseract.tesseract_cmd = (
#     r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# )


def parse_uploaded_file(uploaded_file):

    # --------------------------------
    # RESET FILE POINTER
    # --------------------------------

    uploaded_file.seek(0)

    file_name = uploaded_file.name.lower()

    # --------------------------------
    # PDF
    # --------------------------------

    if file_name.endswith(".pdf"):

        uploaded_file.seek(0)

        reader = PdfReader(uploaded_file)

        text = ""

        for page in reader.pages:

            extracted = page.extract_text()

            if extracted:

                text += extracted + "\n"

        return text

    # --------------------------------
    # TXT
    # --------------------------------

    elif file_name.endswith(".txt"):

        uploaded_file.seek(0)

        text = uploaded_file.getvalue().decode("utf-8")

        return text

    # --------------------------------
    # IMAGE OCR
    # --------------------------------
    elif (

    file_name.endswith(".png")

    or file_name.endswith(".jpg")

    or file_name.endswith(".jpeg")):

        uploaded_file.seek(0)

        image = Image.open(uploaded_file)

        extracted_text = pytesseract.image_to_string(image,config="--psm 6")

    return extracted_text

    return ""
