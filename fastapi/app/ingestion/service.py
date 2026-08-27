from pathlib import Path

from pypdf import PdfReader


def extract_text_from_pdf(file_path: str) -> list[dict]:
    """
    Extract text from every page of a PDF.

    Returns:
        [
            {
                "page": 1,
                "content": "..."
            },
            ...
        ]
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {file_path}")

    reader = PdfReader(str(path))

    pages = []
    pages_needing_ocr = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        text = text.strip()

        if text:
            pages.append(
                {
                    "page": page_number,
                    "content": text,
                }
            )
        else:
            pages_needing_ocr.append(page_number)

    if pages_needing_ocr:
        pages.extend(extract_text_with_ocr(path, pages_needing_ocr))

    pages.sort(key=lambda page: page["page"])
    return pages


def extract_text_with_ocr(path: Path, page_numbers: list[int]) -> list[dict]:
    """Extract text from scanned pages with the local OCR toolchain."""
    try:
        import fitz
        import pytesseract
        from PIL import Image
    except ImportError as exc:
        raise RuntimeError(
            "This scanned PDF needs OCR. Install PyMuPDF and pytesseract."
        ) from exc

    try:
        document = fitz.open(str(path))
        pages = []

        for page_number in page_numbers:
            page = document[page_number - 1]
            pixmap = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
            image = Image.frombytes(
                "RGB",
                (pixmap.width, pixmap.height),
                pixmap.samples,
            )
            text = pytesseract.image_to_string(image).strip()

            if text:
                pages.append({
                    "page": page_number,
                    "content": text,
                })

        return pages
    except Exception as exc:
        raise RuntimeError(f"OCR could not read the PDF: {exc}") from exc