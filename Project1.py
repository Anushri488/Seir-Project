import sys
import requests
from bs4 import BeautifulSoup

if len(sys.argv) < 2:
    print("Enter your Url.")
else:
    url = sys.argv[1]

    response = requests.get(url)
    html = response.text

    soup = BeautifulSoup(html, "html.parser")
    if soup.title:
        print(soup.title.get_text().strip())
    else:
        print("Title missing")
    if soup.body:
        body_text = soup.body.get_text(separator="\n").strip()
        print(body_text)
    else:
        print("Body Content is missing")
    links = soup.find_all("a")
    for link in links:
        href = link.get("href")
        if href:
            print(href)