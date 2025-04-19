import fitz
import logging
from pathlib import Path

from config import uuid4_pdf_re, DATA_DIR

logger = logging.getLogger(__name__)

def merge_pages(input_file_name: str):
    """
    Merge all pages of a PDF document into a single long page.
    """

    if not uuid4_pdf_re.match(input_file_name):
        logger.error("Input file must be in the 'data' folder and have a .pdf extension.")
        return False

    input_file = Path(DATA_DIR, input_file_name)

    src = fitz.open(input_file.as_posix())
    doc = fitz.open()

    # make doc same width but height to sum of input page heights
    # big blank page of new height
    # put each page on the new page at the right height
    width = src[0].bound().width
    original_height = src[0].bound().height
    new_height = original_height * len(src)

    page = doc.new_page(-1,
                    width = width,
                    height = new_height)

    for i in range(len(src)):
        page.show_pdf_page(fitz.Rect(0, original_height * i, width, original_height * (i + 1)), src, i)

    output_file_name = "/merged_" + input_file.name

    output_file_path = input_file.parent.as_posix() + output_file_name

    doc.save(output_file_path, garbage=4, deflate=True)

    return {
        "success": True,
        "message": f"File saved to {output_file_name}",
    }
