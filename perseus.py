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

data = requests.get(url)
if data.status_code in [200, 204]:
    data = data.content
else:
    raise Exception(f"Invalid status code: {data.status_code}")

from bs4 import BeautifulSoup
soup = BeautifulSoup(data)

if class_:
    mydivs = soup.find_all(container, class_=class_)
else:
    mydivs = soup.find_all(container)

text = [x.get_text() for x in mydivs]
import re
text = [re.sub("\[\d\]","", x) for x in text]
text = [re.sub("\s+"," ", x) for x in text]


text = " ".join(text)
#text = text.split(".")
text = re.sub("[A-Z][.]","", text)
def split(string):
    delimiters = [".", ";"]
 
    for delimiter in delimiters:
        string = "|".join(string.split(delimiter))
    return string
text = split(text).split("|")

text = [x.strip() for x in text]
lines = [f"\n{x}" for x in text]

with open("source.txt" , "w") as file:
    file.writelines(lines)




import subprocess
#ps = subprocess.Popen(('cat', 'source.txt'), stdout=subprocess.PIPE)
#output = subprocess.check_output(('trans', '-brief', '-no-auto'), stdin=ps.stdout)

#ps.wait()
data = {}
for line in lines:
    output= subprocess.check_output(('trans','-brief', '-no-auto',line))
    trans = output.decode("utf-8")
    #trans = trans.split("\n")
    #trans = [x for x in trans if x]
    data[line]=trans.replace("\n","").strip()
#data = dict(zip(lines,trans))

with open("output.csv", "w") as file:
    for k,v in data.items():
        file.write(f"{k}|{v}\n")




