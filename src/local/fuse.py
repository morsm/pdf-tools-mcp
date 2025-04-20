from typing import List
import fitz
import uuid
import logging
from pathlib import Path

from config import DATA_DIR, uuid4_pdf_re

logger = logging.getLogger(__name__)

async def fuse_documents(document_names: List[str], page_numbers: List[int]):
    """
    Fuse specific pages from multiple PDF documents into a single page PDF document.
    """

    logger.info(f"Fusing documents: {document_names} with pages: {page_numbers}")
    
    # Check if the lengths of document_names and page_numbers match
    if len(document_names) != len(page_numbers):
        raise ValueError("The lengths of document_names and page_numbers must match.")
    
    # Create a new PDF document
    fused_document = fitz.open()
    
    pages = []

    for doc_name, page_num in zip(document_names, page_numbers):
        doc = fitz.open(Path(DATA_DIR, doc_name))
        
        pages.append(doc[page_num - 1])

    height = sum(page.rect.height for page in pages)
    width = max(page.rect.width for page in pages)

    target_page = fused_document.new_page(width=width, height=height)

    current_height = 0

    for page in pages:
        target_page.show_pdf_page(fitz.Rect(0, current_height, width, current_height + page.rect.height), page.parent)
        current_height += page.rect.height
        page.parent.close()
    
    fused_doc_name = f"fused_{uuid.uuid4()}.pdf"

    fused_document.save(Path(DATA_DIR, fused_doc_name))

    fused_document.close()

    return {
        "success": True,
        "message": f"Fused document saved as {fused_doc_name}",
    }
