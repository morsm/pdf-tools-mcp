import fitz
import logging
import re
from pathlib import Path

logger = logging.getLogger(__name__)

pdf_in_data_folder_re = re.compile(r"^data/[^/]+\.pdf$")

def merge_pages(input_file_path: str):
    """
    Merge all pages of a PDF document into a single long page.
    """

    if not pdf_in_data_folder_re.match(input_file_path):
        logger.error("Input file must be in the 'data' folder and have a .pdf extension.")
        return False

    input_file = Path(input_file_path)

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

    output_file_path = input_file.parent.as_posix() + "/merged_" + input_file.name

    doc.save(output_file_path, garbage=4, deflate=True)

    return {
        "success": True,
        "message": f"File saved to {output_file_path}",
    }
