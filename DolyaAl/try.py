import re
f = open("dataset/®£« á¨ï/dopolnitelnoe-soglashenie-k-memorandumu-protivodeistviia-golosovym-vyzovam.rtf")
s = f.read()
s = s.replace("\n", " ")
cleaned_string = re.sub(r'<script\b[^>]*>(.*?)</script>', ' ', s)
cleaned_string = re.sub(r'<(.*?)>', ' ',cleaned_string)

print(cleaned_string)