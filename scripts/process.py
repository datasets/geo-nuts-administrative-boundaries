import os
import json
import requests
from bs4 import BeautifulSoup

url = 'https://gisco-services.ec.europa.eu/distribution/v2/nuts/'
format_ESPG = '4326'
scale = '60M'
unit = 'RG'

def update_datapackage(list_of_geojson):
    cnt = 0
    for elem in list_of_geojson:
        with open('datapackage.json', 'r') as f:
            data = json.load(f)
            byte_size = os.path.getsize('data/'+elem)
            data['resources'][cnt]['name'] = elem.split('.')[0]
            data['resources'][cnt]['path'] = 'data/'+elem
            data['resources'][cnt]['bytes'] = byte_size
            cnt += 1
        with open('datapackage.json', 'w') as f:
            json.dump(data, f, indent=2)
    print('datapackage.json has been updated')

def run():
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    a_tags = soup.find_all('a')
    latest_tag = ''
    for a in a_tags:
        if 'files' in a.get('href'):
            latest_tag = a.get('href')
            break
    print(f'Latest tag found: {latest_tag}')

    response_2 = requests.get(url + latest_tag)
    soup_2 = BeautifulSoup(response_2.text, 'html.parser')
    li_tags = soup_2.find_all('li')
    list_of_geojson = []
    for elem in li_tags:
        if scale in elem.text and format_ESPG in elem.text and unit in elem.text \
        and (elem.text.endswith('_1.geojson') or elem.text.endswith('_2.geojson') or \
             elem.text.endswith('_3.geojson')):
            a_tag = elem.find('a')
            get_href = a_tag.get('href')
            list_of_geojson.append(get_href)
    print(f'GeoJSON files to download: {list_of_geojson}')

    for geojson in list_of_geojson:
        response_3 = requests.get(url+geojson)
        with open('data/'+geojson.split('/')[1], 'wb') as f:
            f.write(response_3.content)
            print(f'{geojson} has been downloaded')
    list_of_geojson = [geojson.split('/')[1] for geojson in list_of_geojson]
    return list_of_geojson

if __name__ == '__main__':
    list_of_geojson = run()
    update_datapackage(list_of_geojson)
