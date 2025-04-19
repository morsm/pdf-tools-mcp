import aiohttp
import aiofiles
import os
import uuid

from config import DATA_DIR

async def download_pdf(url):
    """
    Saves a PDF file from a given URL
    """

    file_name = uuid.uuid4()

    save_path = os.path.join(os.getcwd(), DATA_DIR, f"{file_name}.pdf")

    try:
        # Make an asynchronous request to the URL
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    print(f"Error: Received status code {response.status}")
                    return False
                
                # Save the content to a temporary file asynchronously
                async with aiofiles.open(save_path, 'wb') as file:
                    while True:
                        chunk = await response.content.read(8192)
                        if not chunk:
                            break
                        await file.write(chunk)

        print(f"File downloaded successfully: {save_path}")
        return f"File saved to {file_name}.pdf"
            
    except Exception as e:
        print(f"Error downloading the file: {e}")
        return False
