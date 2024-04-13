import re
from striprtf.striprtf import rtf_to_text
from pathlib import Path

p = Path("dataset/")
for path in p.rglob("*"):
    if path.is_file():
        print(path)
        with open(path, encoding='utf-8') as infile:
            content = infile.read()
            text = rtf_to_text(content)
            #text = re.sub(r'(_)\1+', ' fill-in field ', text)
            new_path = str(path).replace("dataset", "raw_dataset")
            new_path = new_path[:new_path.rindex('.') + 1] + 'txt'
            outfile = open(new_path,'w', encoding='utf-8')
            outfile.write(text)