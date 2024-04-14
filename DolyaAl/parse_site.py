import re
import requests

def get_data_by_url(url):
    r = requests.get(url)
    s = r.content.decode('cp1251')
    return s
maps = {
     "доверенность":"proxy",
     "договор":"contract",
     "акт":"act",
     "заявление":"application",
     "приказ":"order",
     "счет":"invoice",
     "приложение":"bill",
     "соглашение":"arrangement",
     "устав":"statute",
     "решение":"determination"
}

url = "https://internet-law.ru/docs/index-map.htm"
s = get_data_by_url(url)
refs = []
tags = re.findall(r'<p>(.+?)</p>', s)
for data in tags:
    refs.append(re.findall(r'<a href="(.+?)">', data))
for ref in refs:
    if len(ref):
        url = "https://internet-law.ru/docs/" + ref[0]
        s = get_data_by_url(url)
        title = re.findall(r'<title>(.+?)</title>', s)
        papka = ""
        if len(title):
            print(title[0])
            title[0] = title[0].replace("Образец. ", "")
            name = title[0][:title[0].find(' ')]
            name = name.lower()
            if maps.get(name):
                papka = maps[name]
        s = s.replace("<pre>", " <pre> ")
        s = s.replace("</pre>", " </pre> ")
        ind1 = s.find("<pre>")
        ind2 = s.find("</pre>")
        data = s[ind1 + 5:ind2]
        if papka != "" and len(data):
            path = ref[0].replace("htm", "txt")
            print("new_new_data/"+papka + "/" + path)
            if "new_new_data/"+papka + "/" + path == "new_new_data/proxy/doverennost-spetsialnaya.txt":
                some = 0
                a = some + 1
            file = open("new_new_data/"+papka + "/" + path, 'w')
            file.write(data)
            file.close()
        
print(s)