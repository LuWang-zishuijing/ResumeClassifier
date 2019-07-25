import os, glob, json, nltk, numpy, csv, re
from filter import look_for_sections, extract_expected_sections_titles
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from re import finditer
import itertools
import operator

from functools import reduce 
from unicode_punctuation import is_unicode_punctuation


porter = PorterStemmer()

stop_words = stopwords.words('english')
input_location = './output/selected'

punctuations = '[!#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]'

re_paren = re.compile("(\{|\(|\[)\d+(\}|\)|\])")

re_url = re.compile("^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$")

re_textNumber = re.compile(r"([A-Za-z\.\-]+)|([0-9\.]+)")

re_date = re.compile(r"\d{2,4}-\d{1,2}-\d{1,2}")


def camel_case_split(identifier):
    matches = finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', identifier)
    return [m.group(0) for m in matches]

# Filter patterns like (1), [2], {3}
def remove_parens(words):
    l = len(words)

    for i in range(l - 1, -1, -1):
        group = words[i:i+3]
        joined_group = ''.join(group)
        if re_paren.match(joined_group):
            del words[i:i+3]

    return words

def are_all_punctuation(word):
    return all([ c in punctuations for c in word])

def break_unicode_punctuation(word):
    if all([not is_unicode_punctuation(c) for c in word]):
        return [word]

    l = len(word)

    remain = word

    collect = []

    for i in range(l - 1, -1, -1):
        c = word[i]
        if is_unicode_punctuation(c):
            part = remain[i + 1:]
            collect.append(part)
            remain = remain[:i]
    
    collect.append(remain)
    collect.reverse()

    return collect

def is_url(word):
    return re_url.match(word)

def break_text_number(word):
    if re_date.match(word): # make an exception of date 1999-01-01
        return [word]

    collect = []

    i = 0

    while True:
        match = re_textNumber.search(word, i)

        if match is None:
            break
        collect.append(match.group(0))
        i = match.end(0)

    return collect

def extract_section_words(text):
    lines = [line for line in text.split('\n') if line.strip() != '']
    
    # Word tokenize
    words = [ word_tokenize(line) for line in lines]

    words = reduce(operator.concat, words)

    words = [ camel_case_split(word) for word in words]
    # words = list(itertools.chain(*words))
    words = reduce(operator.concat, words)

    # Remove parens
    words = remove_parens(words)
    # Filter punctuation
    words = [ word for word in words if not are_all_punctuation(word)]

    # Break unicode punctuation
    words = [ break_unicode_punctuation(word) for word in words]
    # words = list(itertools.chain(*words))
    words = reduce(operator.concat, words)

    # Filter URL
    words = [ word for word in words if not is_url(word)]

    # break text and number
    words = [ break_text_number(word) for word in words]
    # words = list(itertools.chain(*words))
    words = reduce(operator.concat, words)

    # Filter stop words and stem
    words = [porter.stem(word) for word in words]
    words = [word for word in words if word not in stop_words]

    return words

def extract_info(json_file):

    with open(json_file) as json_file:  
        data = json.load(json_file)

    titles = extract_expected_sections_titles(data)

    sections = [section for section in data['sections'] if section['title'] in titles]

    all_section_words = [extract_section_words(section['text']) for section in sections]

    # numpy.array(all_section_words).flatten().tolist()
    return  reduce(operator.concat, all_section_words)


c = 1

with open('actor_words.csv', 'w', encoding="utf8") as csvfile:
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

# json_file = glob.glob(os.path.join('./output/selected/nm0005211', "./*.json"))[0]
# words = extract_info(json_file)

# print(words[:100], len(words))

# with open("Output.txt", "w") as text_file:
#     text_file.write(str(words))

