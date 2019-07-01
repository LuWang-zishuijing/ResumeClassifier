import requests
import json 
import html
import re
import sys
from bs4 import BeautifulSoup
from bs4 import Comment
from fuzzywuzzy import process

def eprint(*args, **kwargs):
    pass
    #print(*args, file=sys.stderr, **kwargs)

def get_wiki_content(name, output_file):
    resp = requests.get(f'https://en.wikipedia.org//w/api.php?action=opensearch&format=json&search={name}')

    if resp.status_code < 200 and  resp.status_code >= 300:
        eprint('Cannot get http request correctly')
        exit()


    jobject = json.loads(resp.text)

    candidates = jobject[1]

    links = jobject[-1]

    choice = process.extractOne(name, candidates)[0]
    link = links[candidates.index(choice)]

    pattern=re.compile("[^/]+$")
    page_id = pattern.search(link).group(0)
    print(choice, page_id)
    print("\n")
    
    json_sections = get_all_sections_info(page_id)

    json_output = {
        'name': name,
        'wiki_link': link,
        'sections': json_sections['sections']
    }
    
    json_output_str = json.dumps(json_output, indent=4)

    file = open(output_file, 'w')
    file.write(json_output_str)
    file.close()

    print('job finished\n')

def get_all_sections_info(name):
    url = f'https://en.wikipedia.org/w/api.php?action=parse&format=json&page={name}&prop=sections'

    resp = requests.get(url)

    if resp.status_code < 200 and  resp.status_code >= 300:
        eprint('Cannot get http request correctly')
        exit()
    
    jobject = json.loads(resp.text)

    sections = jobject["parse"]['sections']

    level1_sections = [section for section in sections if section['toclevel'] == 1]

    print(f"found {len(sections)} sections. {len(level1_sections)} level 1 sections\n")

    json_output={
        "sections": []
    }

    print(f'reading data for overall description')
    (section_text, refs) = request_section_text(name, 0)
    json_output['sections'].append({    
        "title": 'section 0',
        'text': section_text,
        'references': refs
    })

    count = 1
    all = len(level1_sections)
    for section in level1_sections:
        print(f'reading data for ({count}/{all}) section. {section["line"]}')
        count += 1

        (section_text, refs) = request_section_text(name, section['index'])

        json_output['sections'].append({
            "title": section['line'],
            'text': section_text,
            'references': refs
        })
    return json_output

def request_section_text(name, section_number):
    url = f'https://en.wikipedia.org/w/api.php?action=parse&format=json&page={name}&prop=text&section={section_number}'

    resp = requests.get(url)

    if resp.status_code < 200 and  resp.status_code >= 300:
        eprint('Cannot get http request correctly')
        exit()
    
    jobject = json.loads(resp.text)

    raw_html = jobject["parse"]['text']['*']

    soup = BeautifulSoup(raw_html, features="html.parser")

    for e in soup.find_all('style'):
        e.decompose()

    comments = soup.find_all(string=lambda text: isinstance(text, Comment))

    for e in comments:
        e.extract()

    references = soup.select('ol.references')

    r_refs = []

    for e in references:
        for li in e.find_all('li'):
            r_refs.append(li.text)

    for e in references:
        e.extract()

    # Remove some hidden 'error' tags 
    for e in soup.select('.error'):
        e.decompose()

    return (soup.text, r_refs)

name=sys.argv[1]
output=sys.argv[2]

get_wiki_content(name, output)
#get_all_sections_info(html.escape("Arnold_Schwarzenegger"))
#print(request_section_text(html.escape("Arnold_Schwarzenegger"), 9))
#request_section_text(html.escape("Arnold_Schwarzenegger"), 3)
