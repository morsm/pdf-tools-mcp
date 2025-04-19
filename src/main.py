import logging

from mcp.server.fastmcp import FastMCP

from local.display import display_page_as_image
from local.merge import merge_pages
from local.metadata import get_metadata

from remote.display import display_remote_document_page_as_image
from remote.download import download_pdf


logger = logging.getLogger(__name__)

mcp = FastMCP("pdf-tools")

mcp.add_tool(display_page_as_image)
mcp.add_tool(merge_pages)
mcp.add_tool(get_metadata)

mcp.add_tool(display_remote_document_page_as_image)
mcp.add_tool(download_pdf)

def main():
    try:
        mcp.run()
    except Exception as e:
        logger.error(f"Error starting server: {str(e)}")
        raise

if __name__ == "__main__":
    main()
