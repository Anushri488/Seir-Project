import sys
import requests
from bs4 import BeautifulSoup

def count_words(text):
    text = text.lower()
    word_list = []
    temp = ""
    for c in text:
        if c.isalnum():
            temp += c
        else:
            if temp != "":
                word_list.append(temp)
                temp = ""
    if temp != "":
        word_list.append(temp)

    word_count = {}
    for w in word_list:
        if w not in word_count:
            word_count[w] = 1
        else:
            word_count[w] += 1
    return word_count
    

def make_hash(word):
    base = 31
    limit = 2**64
    value = 0
    for ch in word:
            value = (value * base + ord(ch)) % limit
    return value
    

def build_simhash(word_count):
    bit_score = [0] * 64
    for w in word_count:
        h = make_hash(w)
        freq = word_count[w]
        pos = 0
        while pos < 64:
            if (h >> pos) & 1 == 1:
                bit_score[pos] += freq
            else:
                bit_score[pos] -= freq
            pos += 1
    final_hash = 0
    index = 0
    while index < 64:
        if bit_score[index] > 0:
            final_hash = final_hash | (1 << index)
        index += 1

    return final_hash


def similarity(hash_a, hash_b):
    diff = hash_a ^ hash_b
    mismatch = 0
    while diff > 0:
        if diff % 2 == 1:
            mismatch += 1
        diff = diff // 2

    return 64 - mismatch


if len(sys.argv) != 3:
    print("Please enter two URLs")
    sys.exit(1)

u1 = sys.argv[1]
u2 = sys.argv[2]

page1 = requests.get(u1)
page2 = requests.get(u2)

soup1 = BeautifulSoup(page1.text, "html.parser")
soup2 = BeautifulSoup(page2.text, "html.parser")

text1 = soup1.body.get_text(" ") if soup1.body else ""
text2 = soup2.body.get_text(" ") if soup2.body else ""

freq_a = count_words(text1)
freq_b = count_words(text2)

hash_a = build_simhash(freq_a)
hash_b = build_simhash(freq_b)

result = similarity(hash_a, hash_b)

print("Number of matching bits:", result)
