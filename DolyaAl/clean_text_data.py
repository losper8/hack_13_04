import re
from pathlib import Path
import nltk
from cleantext import clean

word_tokenizer = nltk.WordPunctTokenizer()
add_stop_words = ["ооо"]

def delete_additional_stop_words(input_text):
    tokens = word_tokenizer.tokenize(input_text)
    tokens = [token for token in tokens if token not in add_stop_words]
    clean_text = ' '.join(tokens)
    return clean_text

def clear_trash(text):
    trash = ['─','┐','│','└','┌','┘','┤','├','┬','┴','«','»', '№', '¬', '’', '–','┼']
    for t in trash:
        text = text.replace(t, ' ')
    return text
 

def cleaning(text):
    text = re.sub(r'(_)\1+', ' fill-in field ', content)
    text = re.sub('<[^<]+?>', '', text) # tags
    text = re.sub(r'http\S+', '', text)
    text = clear_trash(text)
    text = clean(text, clean_all=True, stp_lang='russian')
    text = delete_additional_stop_words(text)

    return text


p = Path("raw_dataset/")
for path in p.rglob("*"):
    if path.is_file():
        print(path)
        with open(path, encoding='utf-8') as infile:
            content = infile.read()
            text = cleaning(content)
            new_path = str(path).replace("raw_dataset", "clean_dataset")
            outfile = open(new_path,'w', encoding='utf-8')
            outfile.write(text)