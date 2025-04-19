import logging
import io
import requests
import base64

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.utilities.types import Image
import mcp.types as types

import fitz
from pydantic import AnyUrl

logger = logging.getLogger(__name__)

mcp = FastMCP("pdf-tools")

@mcp.tool()
async def display_page_as_image(url:str, page_number: int):
    """
    Display a specific page of the PDF document.
    """
    logger.info(f"Displaying page {page_number} from url {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()
        filestream = io.BytesIO(response.content)
        document = fitz.open(stream=filestream, filetype="pdf")
        page = document[page_number]
        pixmap = page.get_pixmap(matrix=fitz.Matrix(2, 2))
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

def main():
    try:
        mcp.run()
    except Exception as e:
        logger.error(f"Error starting server: {str(e)}")
        raise


if __name__ == "__main__":
    main()
