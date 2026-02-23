import sys
import requests
from bs4 import BeautifulSoup

def fetch_page(url):
    page = requests.get(url)
    html_data = page.text
    soup = BeautifulSoup(html_data, "html.parser")
    
    scripts = soup.find_all("script")
    for item in scripts:
        item.decompose()
        
    if soup.title is not None:
        page_title = soup.title.get_text().strip()
    else:
        page_title = "No Title"

    if soup.body is not None:
        page_text = soup.body.get_text(" ")
    else:
        page_text = ""
        
    page_links = []
    all_links = soup.find_all("a")
    for link in all_links:
        address = link.get("href")
        if address is not None:
            page_links.append(address)

    return page_title, page_text, page_links

def count_words(text):
    text = text.lower()
    words = []
    temp = ""
    for ch in text:
        if ch.isalnum():
            temp = temp + ch
        else:
            if temp != "":
                words.append(temp)
                temp = ""
    if temp != "":
        words.append(temp)
    freq = {}
    for w in words:
        if w in freq:
            freq[w] = freq[w] + 1
        else:
            freq[w] = 1
    return freq
    

def make_hash(word):
    p = 53
    m = 2**64
    h = 0
    power = 1
    for ch in word:
        h = (h + ord(ch) * power) % m
        power = (power * p) % m
    return h


def build_simhash(freq):
    bits = [0] * 64
    for w in freq:
        h = make_hash(w)
        count = freq[w]
        i = 0
        while i < 64:
            if (h >> i) & 1 == 1:
                bits[i] = bits[i] + count
            else:
                bits[i] = bits[i] - count
            i = i + 1
    simhash = 0
    i = 0
    while i < 64:
        if bits[i] > 0:
            simhash = simhash + (1 << i)
        i = i + 1

    return simhash


def similarity(h1, h2):
    x = h1 ^ h2
    diff = 0
    while x > 0:
        if x % 2 == 1:
            diff = diff + 1
        x = x // 2
    return 64 - diff

if len(sys.argv) != 3:
    print("Usage: python script.py url1 url2")
    sys.exit(1)

url1 = sys.argv[1]
url2 = sys.argv[2]

title1, body_text1, links1 = fetch_page(url1)
title2, body_text2, links2 = fetch_page(url2)

freq1 = count_words(text1)
freq2 = count_words(text2)

hash1 = build_simhash(freq1)
hash2 = build_simhash(freq2)

common_bits = similarity(hash1, hash2)

print("Title 1:", title1)
print("Title 2:", title2)
print()
print("BODY_TEXT 1:", body_text1)
print()
print("BODY_TEXT 2:", body_text2)
print()
print("LINKS IN URL 1:", links1)
print()
print("LINKS IN URL 2:", links2)
print()
print("Number of matching bits:", common_bits)
