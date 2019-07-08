import json
import requests
import re
import statistics

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

interim_results = []
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


def hasNumbers(inputString):
    return bool(re.search(r'\d', inputString))

def get_bounding_box(results, sensitivity = 0.75):
    """
    :param results: An array of GeoNames results
    :param sensitivity: Multiplier for sigma in bounding box
    :return: [minX, minY, maxX, maxY]
    """
    lats = [float(result['lat']) for result in results]
    lngs = [float(result['lng']) for result in results]

    mean_lng = statistics.mean(lngs)
    mean_lat = statistics.mean(lats)

    sigma_lng = statistics.stdev(lngs)
    sigma_lat = statistics.stdev(lats)

    return [
        mean_lng - sensitivity * sigma_lng,
        mean_lat - sensitivity * sigma_lat,
        mean_lng + sensitivity * sigma_lng,
        mean_lat + sensitivity * sigma_lat,
    ]


def in_bounding_box (result, bounding_box):
    lng, lat = float(result['lng']), float(result['lat'])

    if bounding_box[0] < lng < bounding_box[2] and bounding_box[1] < lat < bounding_box[3]:
        return True

    return False


for word in words:
    if word['description'] not in exclude and len(word['description']) > 4 and hasNumbers(word['description']) is False:
        url = "http://api.geonames.org/searchJSON?maxRows=1&username=cogapp&featureClass=A&name=" + word['description']
        response = requests.get(url)
        if len(response.json()['geonames']) > 0:
            result = response.json()['geonames'][0]
            result['description'] = word['description']
            result['xywh'] = find_xywh(word['boundingPoly'])
            interim_results.append(result)

bounding_box = get_bounding_box(interim_results)

results = [result for result in interim_results if in_bounding_box(result, bounding_box)
                                                and result['population'] > 0]

with open('../docs/data/places_json/IOR_L_PS_10_595_0243.ptif.json', 'w') as file:
    json.dump(results, file)
