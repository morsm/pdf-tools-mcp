import fitz
import logging
import re

logger = logging.getLogger(__name__)

pdf_in_data_folder_re = re.compile(r"^data/[^/]+\.pdf$")

async def get_metadata(file_path: str):
    """
    Extract metadata and content from all pages of a PDF file.
    """

    if not pdf_in_data_folder_re.match(file_path):
        logger.error("Input file must be in the 'data' folder and have a .pdf extension.")
        return False


    # Initialize result dictionary
    result = {
        "metadata": {},
        "pages": []
    }
    
    try:
        # Open the PDF file
        doc = fitz.open(file_path)
        
        # Extract metadata
        metadata = doc.metadata

        if metadata is None:
            logger.error("No metadata found in the PDF.")
            return False

        result["metadata"] = metadata
        
        # Get additional document info
        result["metadata"]["page_count"] = len(doc)
        
        # Extract content from each page
        for page_num, page in enumerate(doc):
            # Get page dimensions
            rect = page.rect
            
            # Store page information
            page_info = {
                "page_number": page_num + 1,
                "width": rect.width,
                "height": rect.height,
            }
            
            result["pages"].append(page_info)
        
        # Close the document
        doc.close()
        
        return result
    except Exception as e:
        logger.error(f"Error processing PDF file: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }
