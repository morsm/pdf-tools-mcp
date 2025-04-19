import fitz
import logging
from pathlib import Path
import json

from config import DATA_DIR, uuid4_pdf_re

logger = logging.getLogger(__name__)


async def get_text_blocks(file_name: str, page_number: int = 0):
    """
    Extract text content from a specific page of a PDF file, in blocks. This contains the bounding box, text, number and type.
    """

    if not uuid4_pdf_re.match(file_name):
        logger.error(
            "Input file must be in the 'data' folder and have a .pdf extension."
        )
        return False

    file_path = Path(DATA_DIR, file_name)

    document = fitz.open(file_path)

    page = document[page_number - 1]

    result = page.get_text("blocks")

    result = [
        {
            "x0": block[0],
            "y0": block[1],
            "x1": block[2],
            "y1": block[3],
            "text": block[4],
            "block_no": block[5],
            "block_type": block[6],
        }
        for block in result
    ]

    response = {
        "success": True,
        "file_name": file_name,
        "page_number": page_number,
        "text_blocks": result,
    }

    logger.info("Returning response of length: %s", len(str(result)))

    return response

async def get_text_json(file_name: str, page_number: int = 0):
    """
    Extract text content from a specific page of a PDF file, as json. This contains the most information.
    """

    if not uuid4_pdf_re.match(file_name):
        logger.error(
            "Input file must be in the 'data' folder and have a .pdf extension."
        )
        return False

    file_path = Path(DATA_DIR, file_name)

    document = fitz.open(file_path)

    page = document[page_number - 1]

    result = page.get_text("json")

    result = json.loads(result)

    logger.info(type(result))

    response = {
        "success": True,
        "file_name": file_name,
        "page_number": page_number,
        "text_json": result,
    }

    logger.info("Returning response of length: %s", len(str(result)))

    return response
