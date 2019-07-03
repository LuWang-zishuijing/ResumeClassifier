import os, glob, json, nltk, numpy, csv
from filter import look_for_sections, extract_expected_sections_titles
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import string
porter = PorterStemmer()

stop_words = stopwords.words('english')
input_location = './output/succeed'

def extract_section_words(text):
    lines = [line for line in text.split('\n') if line.strip() != '']
    
    # Work tokenize
    words = [ word_tokenize(text) for line in lines]
    words = numpy.array(words).flatten().tolist()

    # Filter stop words and stem
    words = [word.lower() for word in words]
    words = [word for word in words if word not in stop_words]
    words = [porter.stem(word) for word in words]
    

    return words

def extract_info(json_file):

    with open(json_file) as json_file:  
        data = json.load(json_file)

    titles = extract_expected_sections_titles(data)

    sections = [section for section in data['sections'] if section['title'] in titles]

    all_section_words = [extract_section_words(sections[0]['text']) for section in sections]

    return numpy.array(all_section_words).flatten().tolist()


c = 1

with open('actor_words_all.csv', 'w', encoding="utf8") as csvfile:
    csv_writer = csv.writer(csvfile, delimiter='\t')
    csv_writer.writerow(['actor_id', 'words'])
    all_folders = os.listdir(input_location)
    c_all_folder = len(all_folders)
    for folder in all_folders:
        json_file = glob.glob(os.path.join(input_location, folder, "./*.json"))[0]
        words = extract_info(json_file)

        csv_writer.writerow([folder, ' '.join(words)])
        
        print(f'dump text for {folder} {c}/{c_all_folder}')

        c += 1