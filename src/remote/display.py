import io
import logging
import requests

import fitz
from mcp.server.fastmcp.utilities.types import Image

logger = logging.getLogger(__name__)

async def display_remote_document_page_as_image(url:str, page_number: int = 1):
    """
    Display a specific page of a PDF document by its URL.
    """
    logger.info(f"Displaying page {page_number} from url {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()
        filestream = io.BytesIO(response.content)
        document = fitz.open(stream=filestream, filetype="pdf")
        page = document[page_number - 1] # 1-based index for users
        pixmap = page.get_pixmap(matrix=fitz.Matrix(2, 2)) # type: ignore
        return Image(data=pixmap.tobytes(), format="png")
    except requests.RequestException as e:
        logger.error(f"Failed to fetch PDF from URL: {str(e)}")
        return {
            "success": False,
            "error": f"Failed to fetch PDF from URL: {str(e)}"
        }
    except Exception as e:
        logger.error(str(e))
        return {
            "success": False,
            "error": str(e)
        }
