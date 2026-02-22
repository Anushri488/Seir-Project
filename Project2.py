import sys
import requests
from bs4 import BeautifulSoup
import re

def get_word_frequency(text):
    words = re.findall(r"[a-z0-9]+", text.lower())
    freq = {}

    for word in words:
        freq[word] = freq.get(word, 0) + 1

    return freq


def polynomial_hash(word):
    p = 53
    m = 2**64
    hash_value = 0
    power = 1
    for ch in word:
        hash_value = (hash_value + ord(ch) * power) % m
        power = (power * p) % m
    return hash_value



def comp_simhash(freq):
    V = [0] * 64
    for word, count in freq.items():
        h = polynomial_hash(word)

        for i in range(64):
            if (h >> i) & 1:
                V[i] += count
            else:
                V[i] -= count
    simhash = 0
    for i in range(64):
        if V[i] > 0:
            simhash |= (1 << i)
    return simhash


def compare_simhash(hash1, hash2):
    xor = hash1 ^ hash2
    different_bits = bin(xor).count("1")
    return 64 - different_bits



if len(sys.argv) < 3:
    print("Enter the two Urls.")
    sys.exit()

url1 = sys.argv[1]
url2 = sys.argv[2]

response1 = requests.get(url1)
soup1 = BeautifulSoup(response1.text, "html.parser")
body1 = soup1.body.get_text() if soup1.body else ""

response2 = requests.get(url2)
soup2 = BeautifulSoup(response2.text, "html.parser")
body2 = soup2.body.get_text() if soup2.body else ""

freq1 = get_word_frequency(body1)
freq2 = get_word_frequency(body2)


hash1 = comp_simhash(freq1)
hash2 = comp_simhash(freq2)


common_bits = compare_simhash(hash1, hash2)

print("Common bits:", common_bits)