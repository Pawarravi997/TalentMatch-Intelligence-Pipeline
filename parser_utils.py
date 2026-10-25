import PyPDF2
import pytesseract
from PIL import Image
import io
import requests
from bs4 import BeautifulSoup

def extract_text_from_pdf(file_bytes):
    pdf_file = io.BytesIO(file_bytes)
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

def extract_text_from_image(file_bytes):
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    image = Image.open(io.BytesIO(file_bytes))
    text = pytesseract.image_to_string(image)
    return text

def scrape_jd_from_url(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "lxml")
            for script in soup(["script", "style"]):
                script.decompose()
            text = soup.get_text(separator=" ")
            lines = [line.strip() for line in text.splitlines()]
            chunks = [phrase.strip() for line in lines for phrase in line.split("  ")]
            text = "\n".join(chunk for chunk in chunks if chunk)
            return text
        return f"Error: Received HTTP status code {response.status_code}"
    except Exception as e:
        return f"Scraping Failed: {str(e)}"
