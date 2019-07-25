import os
import glob
import json
from fuzzywuzzy import process, fuzz
import shutil
import random

num_selection = 10000
input_location = './output/succeed'
output_selected = './output/selected'

look_for_sections = ['section 0', 'Early life', 'Career', 'Personal life']

output_selected_dir = os.path.realpath(output_selected)
if not os.path.exists(output_selected_dir):
    os.makedirs(output_selected_dir)

def find_most_likely_standard_title(title):
    scores = [fuzz.ratio(standard, title) for standard  in look_for_sections ]

    max_score = max(scores)

    max_score_index = scores.index(max_score)

    return look_for_sections[max_score_index]

def map_to_standard_title(titles):
    return [find_most_likely_standard_title(title) for title in titles]

def has_expected_sections(json_object):
    extracted = extract_expected_sections_titles(json_object)

    deduped_extracted = set(extracted)

    map_to_standard_titles = map_to_standard_title(deduped_extracted)

    if len(deduped_extracted) == len(look_for_sections):
        return True
        
    return ('section 0' in map_to_standard_titles) and ('Career' in map_to_standard_titles)

def extract_expected_sections_titles(json_object):
    titles = [section['title'] for section in json_object['sections']]
    extracted = [process.extractOne(name, titles)[0] for name in look_for_sections]

    return extracted

def process_one_json(folder):
    json_file = glob.glob(os.path.join(input_location, folder, "./*.json"))[0]

    with open(json_file) as json_file:  
        data = json.load(json_file)

        valid = has_expected_sections(data)

        if valid:
            original_location = os.path.realpath(os.path.join(input_location, folder))
            dest_location = os.path.realpath(os.path.join(output_selected, folder))

            if not os.path.exists(dest_location):
                 os.makedirs(dest_location)

            for f in os.listdir(original_location):
                filename = os.path.join(original_location, f)
                shutil.copy(filename, dest_location)
            return True
        else:
            return False

if __name__ == "__main__":
    all_folders = list(os.listdir(input_location))

    all_folders_count = len(all_folders)

    count = 0

    print()

    while count < num_selection or len(all_folders) == 0:

        if len(all_folders) == 0:
            print('drained all folders')
            break; 

        pick = random.choice(all_folders)

        all_folders.remove(pick)

        result = process_one_json(pick)

        if result:
            count+=1
            print(f'\r process {pick} succeeded {count} / {num_selection} / {all_folders_count}', end="")
        else:
            print(f'\r process {pick} failed {count} / {num_selection} / {all_folders_count}', end="")


    