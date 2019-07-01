import csv
from random import sample

with open('actors_70s.csv', encoding = 'utf8', newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')

    c = 0    
    for row in csvreader:
        file_id = row[0].strip()
        name = row[1].strip()
        print(file_id, name)

        try:
            file = open(f'./input/{file_id}', 'w')
            file.write(name)
            file.close()
        except:
            print(f'cannot process {file_id}')
