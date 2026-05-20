import fitz
import google.generativeai as genai
import json
import os
from dotenv import load_dotenv

# This loads your API key from the .env file
load_dotenv()

# Connect to Gemini using your free API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def extract_text_from_pdf(pdf_path):
    """
    Opens the PDF and reads all text from every page.
    fitz is the pymupdf library — best tool for PDF text extraction.
    """
    doc = fitz.open(pdf_path)
    full_text = ""

    for page in doc:
        full_text += page.get_text()

    doc.close()
    return full_text


def chunk_text(text, max_chars=12000):
    """
    Papers are long. We only take the first 12000 characters.
    This covers abstract, introduction, methodology —
    the most important parts. Keeps it fast and free.
    """
    return text[:max_chars]


def analyze_paper(pdf_path):
    """
    The main function.
    1. Extracts text from PDF
    2. Cuts it to a safe size
    3. Sends to Gemini
    4. Returns structured result as a Python dictionary
    """

    # Extract raw text
    raw_text = extract_text_from_pdf(pdf_path)

    # Take only what we need
    text_chunk = chunk_text(raw_text)

    # Load the free Gemini Flash model
    # gemini-1.5-flash is fast, free, and good enough for this task
    model = genai.GenerativeModel("gemini-flash-latest")

    # This is the prompt — we tell Gemini exactly what to return
    # The double curly braces {{ }} are how you write { } inside
    # a Python f-string without it breaking
    prompt = f"""You are a research paper analyst. Read the following research paper text and extract key information.

Return ONLY a valid JSON object with exactly these fields — no extra text, no explanation, just the JSON:

{{
    "title": "the paper title",
    "problem": "what problem is this paper trying to solve, in 2-3 sentences",
    "claims": ["main claim 1", "main claim 2", "main claim 3"],
    "methods": ["method or technique 1", "method or technique 2"],
    "findings": ["key finding 1", "key finding 2", "key finding 3"],
    "summary": "a plain English summary of the entire paper in 4-5 sentences that a non-expert can understand",
    "difficulty": "Beginner / Intermediate / Advanced"
}}

Here is the paper text:

{text_chunk}"""

    # Send to Gemini and get response
    response = model.generate_content(prompt)
    response_text = response.text

    # Gemini sometimes wraps the JSON in ```json ``` blocks
    # This cleans that out so we get pure JSON
    response_text = response_text.strip()
    if response_text.startswith("```"):
        response_text = response_text.split("```")[1]
        if response_text.startswith("json"):
            response_text = response_text[4:]

    # Convert JSON text into a Python dictionary
    try:
        result = json.loads(response_text.strip())
    except json.JSONDecodeError:
        # If something goes wrong, return a safe fallback
        result = {
            "title": "Could not parse",
            "problem": "Try uploading the paper again.",
            "claims": [],
            "methods": [],
            "findings": [],
            "summary": response_text,
            "difficulty": "Unknown"
        }

    return result