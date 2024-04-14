import re
from striprtf.striprtf import rtf_to_text
from pathlib import Path
from doc_to_txt import doc_and_pdf_to_txt

p = Path("new_data/")
for path in p.rglob("*"):
    if path.is_file():
        print(path)
        text = doc_and_pdf_to_txt(path)