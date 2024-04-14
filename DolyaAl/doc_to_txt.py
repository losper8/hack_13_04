from pathlib import Path
import aspose.words as aw

def doc_and_pdf_to_txt(file_path: Path):
    doc = aw.Document(str(file_path))
    new_path = str(file_path)[:str(file_path).rindex('.') + 1] + 'txt'
    new_path = new_path.replace("new_data", "raw_dataset")
    doc.save(new_path)
    text = ""
    with open(new_path) as doc_with_trash:
        content = doc_with_trash.read()
        text = content.replace("Evaluation Only. Created with Aspose.Words. Copyright 2003-2024 Aspose Pty Ltd.", " ")
        text = text.replace("Created with an evaluation copy of Aspose.Words. To discover the full versions of our APIs please visit: https://products.aspose.com/words/", " ")
    file = open(new_path, 'w')
    file.write(text)
