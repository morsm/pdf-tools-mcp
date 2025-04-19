import re

DATA_DIR = "data"

allowed_prefixes = [
    "merged_"
    # Add more prefixes here as needed
]
# Join the prefixes with | for alternation and make the entire group optional
prefix_pattern = f"(?:{'|'.join(re.escape(prefix) for prefix in allowed_prefixes)})?"
uuid4_pdf_re = re.compile(f"^{prefix_pattern}[0-9a-f]{{8}}-[0-9a-f]{{4}}-4[0-9a-f]{{3}}-[89ab][0-9a-f]{{3}}-[0-9a-f]{{12}}\\.pdf$")
