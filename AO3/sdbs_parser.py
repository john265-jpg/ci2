import html as html_lib
from bs4 import BeautifulSoup

with open("webpage.html", encoding="utf-8") as f:
    outer = BeautifulSoup(f, "html.parser")

# Collect the raw text of all the highlighted spans -> reconstruct the source
# The simplest reliable approach: take the whole <body> text, which
# reassembles the escaped HTML as a plain string.
escaped_source = outer.get_text()

# Unescape once: "&lt;td class="comp-name"&gt;" -> "<td class="comp-name">"
real_source = html_lib.unescape(escaped_source)

# Now parse the *recovered* HTML
inner = BeautifulSoup(real_source, "html.parser")

for td in inner.find_all("td", class_="comp-name"):
    name = td.get_text(strip=True)
    if name:
        print(name)
