import sys

args = sys.argv

try:
    url = args[1]
except Exception as error:
    print("provide a url")
    sys.exit(1)
container = "div"
class_ = "text"
try:
    container=args[2]
except Exception as error:
    container="div"
try:
    class_ = args[3]
except Exception as error:
    print("continuing with out css  class selector")
if not class_ and "sputnik" in url:
    class_ = "article__block"


import requests
from bs4 import BeautifulSoup
def process(data):
    soup = BeautifulSoup(data)

    if class_:
        mydivs = soup.find_all(container, class_=class_)
    else:
        mydivs = soup.find_all(container)

    text = [x.get_text() for x in mydivs]
    import re
    text = [re.sub("\[\d\]","SECTION", x) for x in text]
    text = [re.sub("\s+"," ", x) for x in text]


    text = " ".join(text)
    return text


def getUrl(book, chapter):
    url = f"http://www.perseus.tufts.edu/hopper/text?doc=Perseus%3Atext%3A1999.02.0076%3Abook%3D{book}%3Achapter%3D{chapter}"
    return url

found = True
book=1
chapter=1

result = {}
while found:
    url = getUrl(book, chapter)
    print(f"Processing book {book} chapter {1} : {url}")
    content = requests.get(url).content.decode("utf-8")
    found = ("unable to find a document" not in content)
    if found:
        data = process(content)
        result[f"{book}.{chapter}"]=data
        chapter+=1
        continue
    if not found:
        book+=1
        chapter=1
        url = getUrl(book,chapter)
        content = requests.get(url).content.decode("utf-8")
        found = ("unable to find a document" not in content)
        if found:
            continue
        if not found:
            print(f"Finished processing at book {book} chapter {chapter}")
            break



with open("output.csv", "w") as file:
    for k,v in result.items():
        file.write(f"{k}|{v}\n")




