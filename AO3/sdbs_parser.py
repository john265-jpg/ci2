import html as html_lib
from bs4 import BeautifulSoup

with open("webpage.html", encoding="utf-8") as f:
    outer = BeautifulSoup(f, "html.parser")

escaped_source = outer.get_text()

real_source = html_lib.unescape(escaped_source)

inner = BeautifulSoup(real_source, "html.parser")

for td in inner.find_all("td", class_="comp-name"):
    name = td.get_text(strip=True)
    if name:
        print(name)
