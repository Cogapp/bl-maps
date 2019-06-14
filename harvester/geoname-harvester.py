import json
import requests
import json
import requests

# Import the json files
with open("../docs/data/ocr_json/IOR_L_PS_10_595_0243.ptif.json", "r") as read_file:
    data = json.load(read_file)
    words = data['responses'][0]['textAnnotations']
    words.pop(0)

exclude = ['Miles', 'Inches', '..', '.', 'Scale', "", "i", "me", "my", "myself", "we", "our", "ours", "ourselves",
           "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers",
           "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who",
           "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have",
           "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because",
           "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through",
           "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over",
           "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any",
           "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same",
           "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now", '&']

results = []


def find_xywh(coords):
    min_x = 10000
    min_y = 10000
    max_x = 0
    max_y = 0
    for pair in coords['vertices']:
        min_x = min(min_x, pair['x'])
        min_y = min(min_y, pair['y'])
        max_x = max(max_x, pair['x'])
        max_y = max(max_y, pair['y'])
    return {'x': min_x, 'y': min_y, 'w': max_x - min_x, 'h': max_y - min_y}


for word in words:
    if word['description'] not in exclude and len(word['description']) > 3:
        url = "http://api.geonames.org/searchJSON?maxRows=1&username=cogapp&q=" + word['description']
        response = requests.get(url)
        if len(response.json()['geonames']) > 0:
            result = response.json()['geonames'][0]
            result['description'] = word['description']
            result['xywh'] = find_xywh(word['boundingPoly'])
            results.append(result)


with open('../docs/data/places_json/IOR_L_PS_10_595_0243.ptif.json', 'w') as file:
    json.dump(results, file)
