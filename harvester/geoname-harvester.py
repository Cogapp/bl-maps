import json
import requests


# Import the json files
with open("../docs/data/ocr_json/IOR_L_PS_10_595_0243.ptif.json", "r") as read_file:
    data = json.load(read_file)
    words = data['responses'][0]['fullTextAnnotation']['text']
    words = ''.join([i for i in words if not i.isdigit()]).strip("\n").strip('.').replace('\n', ' ').split(" ")

exclude = ['Miles', 'Inches','..', '.','Scale', "","i","me","my","myself","we","our","ours","ourselves","you","your","yours","yourself","yourselves","he","him","his","himself","she","her","hers","herself","it","its","itself","they","them","their","theirs","themselves","what","which","who","whom","this","that","these","those","am","is","are","was","were","be","been","being","have","has","had","having","do","does","did","doing","a","an","the","and","but","if","or","because","as","until","while","of","at","by","for","with","about","against","between","into","through","during","before","after","above","below","to","from","up","down","in","out","on","off","over","under","again","further","then","once","here","there","when","where","why","how","all","any","both","each","few","more","most","other","some","such","no","nor","not","only","own","same","so","than","too","very","s","t","can","will","just","don","should","now", '&']

# build up words
query_words = dict()

for word in words:
    if word not in exclude and len(word)> 3:
        query_words[word] = []

i=0

for key in query_words.keys():
    # query key
    url = "http://api.geonames.org/searchJSON?maxRows=1&username=cogapp&q=" + key
    response = requests.get(url)
    # add result to dict
    query_words[key] = response.json()['geonames']
    # add to iterator
    i +=1
    if i > 10:
        break


with open('../docs/data/places_json/IOR_L_PS_10_595_0243.ptif.json', 'w') as file:
    json.dump(query_words, file)
