import sys
import requests
from bs4 import BeautifulSoup
if len(sys.argv) < 2:
    print("Give the URL.")
else:
    url = sys.argv[1].strip()
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    for tag in soup(["script", "style"]):
        tag.decompose()
    if soup.title:
        print(soup.title.get_text().strip())
    else:
        print("Title missing")
    if soup.body:
        text = soup.body.get_text()
        lines = text.split("\n")
        for line in lines:
            line = line.strip()
            if line != "":
                print(line)
   else:
        print("Body Content is missing")   
    links = soup.find_all("a")
    for link in links:
        href = link.get("href")
        if href:
            print(href)
            
