"""Testing web APIs with HTTP GET method"""

import json
import sys

import requests
import textrazor

def print_topic_score(url):
    """Print 10 most probable topics and confidence score for a text from a text on a website url passed as input.""" 
    textrazor.api_key = "fab1f5ef253a7daa2ec64726f01738f24bf84c59dde7c66f1ec1cd04"

    client = textrazor.TextRazor(extractors=["topics"])
    client.set_language_override('fre')
    response = client.analyze_url(url)

    for topic in response.topics()[:10]:
        print(topic.label, topic.score)

def print_coord(address):
    """Retrieve coordinates from Open Street Map"""
    osm = "https://nominatim.openstreetmap.org/search"
    data = {'q': address, 'format': 'json'}
    resp = requests.get(osm, data)
    json_list = json.loads(resp.text)
    for item in json_list:
        display_name = item['display_name']
        short_name = display_name.split(", ")[0]
        lat = item['lat']
        lon = item['lon']
        print(f"{short_name} ({lat} - {lon})")

def print_info(country_name):
    """Retrieve country info from REST API"""
    base_url = "https://restcountries.eu/rest/v2/"
    name_url = base_url + "name/"
    code_url = base_url + "alpha/"
    resp = requests.get(name_url + country_name)
    try:
        country = json.loads(resp.text)[0]
        languages = country['languages']
        print(f"Languages: {', '.join([lang['name'] for lang in languages])}")
        border_codes = country['borders']
        border_names = []
        for code in border_codes:
            resp = requests.get(code_url + code)
            border_country = json.loads(resp.text)
            border_name = border_country["name"]
            border_names.append(border_name)
        print(f"Borders: {', '.join(border_names)}")
    except KeyError:
        print("Unknown country, please use English or native name")

if __name__ == "__main__":
    try:
        service = sys.argv[1]
        if service == "coord":
            try:
                address = sys.argv[2]
                print_coord(address)
            except IndexError:
                print("Please enter an address")
        elif service == "info":
            try:
                country_name = sys.argv[2]
                print_info(country_name)
            except IndexError:
                print("Please enter a country name")
        elif service == 'topic':
            try:
                url_link = sys.argv[2]
                print_topic_score(url_link)
            except IndexError:
                print("Please enter a url to a text source")            
        else:
            print("Unknown action, please use either 'coord', 'info' or 'topic'")
    except IndexError:
        print("Missing action, please use either 'coord', 'info' or 'topic'")
