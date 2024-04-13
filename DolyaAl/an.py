from pathlib import Path
from nltk import word_tokenize
import nltk
from nltk.probability import FreqDist
import string
from nltk.corpus import stopwords
import json
import asyncio

russian_stopwords = stopwords.words("russian")
nltk.download('punkt')
def remove_chars_from_text(text, chars):
    return "".join([ch for ch in text if ch not in chars])
def get_text_tokens(text):
    text = text.lower()
    spec_chars = string.punctuation + '\n\xa0«»\t—…' 
    text = remove_chars_from_text(text, spec_chars)
    text = remove_chars_from_text(text, string.digits)
    text_tokens = word_tokenize(text)
    for word in russian_stopwords:
        while text_tokens.count(word):
            text_tokens.remove(word)
    return text_tokens

def analyse_dataset(fdist:FreqDist):
    p = Path("clean_dataset/")
    print(p)
    for path in p.rglob("*"):
        if path.is_dir():
            print(f"{path=}")
            fdist = FreqDist()
            for fpath in path.rglob("*"):
                print(f"{fpath=}")
                with open(fpath, encoding='utf-8') as infile:
                    content = infile.read()
                    text_tokens = get_text_tokens(content)
                    text_nltk = nltk.Text(text_tokens)
                    fdist.update(text_nltk)
            json_path = str(path) + "_fdist.json"
            file = open(json_path, "w")
            file.write(json.dumps(dict(fdist), indent=4,ensure_ascii = False).encode('utf8').decode())
            file.close()
    return fdist

#file = open("clean_dataset/statute_fdist.json", "r")
#file_json = json.load(file)
#file.close()

#fdist = FreqDist(dict(file_json))
fdist = FreqDist()
fdist = analyse_dataset(fdist)

#fdist.plot(30,cumulative=False)


