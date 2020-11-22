from PyDictionary import PyDictionary
import requests
from bs4 import BeautifulSoup
import random
import string
import re
import unicodedata
import spacy
from spacy.lang.en.stop_words import STOP_WORDS

dictionary=PyDictionary()
no_synonyms = set()
write_file = open("outputfile.txt", "a")
synonyms = {}
links_visited = set()

def replace_with_synonyms(sentence):
    sentence_new = []
    for word in sentence.split(' '):
        if word.lower() in STOP_WORDS:
            sentence_new.append(word)
        elif word not in no_synonyms:
            synonyms = dictionary.synonym(word)
            if synonyms:
                sentence_new.append(random.choice(synonyms))
            else:
                no_synonyms.add(word)
                sentence_new.append(word)
    return ' '.join(sentence_new)

def clean_text(text):
    '''
    input: "AAAAA.BBBBB [2], CCCCC."
    output: "AAAAA BBBBB CCCCC"
    '''
    text = re.sub(r'\[.*?\]', '', text) 
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

def remove_accented_chars(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    return text

linkToScrape = []
def scrapeWikiArticle(url):
    if url in links_visited:
        pass
    links_visited.add(url)
    response = requests.get(
        url=url,
    )
    
    soup = BeautifulSoup(response.content, 'html.parser')

    
    paragraphs = soup.select("p")

    for para in paragraphs:
        content = clean_text(para.text)
        # content = replace_with_synonyms(content)
        content = remove_accented_chars(content)
        content = content.lower()
        print(content)
        write_file.write(content + "\n")


    # allLinks = soup.find(id="bodyContent").find_all("a")
    # random.shuffle(allLinks)
    

    # for link in allLinks:
    #     # We are only interested in other wiki articles
    #     if link.has_attr('href'):
    #         if link['href'].find("/wiki/") == -1: 
    #             continue
    #         if re.search(r"^[a-zA-Z0-9_\(\)\/]*$", link['href']):
    #             linkToScrape.append(link)
    #         # link.translate(str.maketrans('', '', string.punctuation))
    
    # try:
    #     linkToScrape.pop()
    #     scrapeWikiArticle("https://simple.wikipedia.org" + link['href'])
    # except:
    #     linkToScrape.pop()
    #     scrapeWikiArticle("https://simple.wikipedia.org" + link['href'])

for _ in range(100):
    scrapeWikiArticle("https://en.wikipedia.org/wiki/Special:Random")
