import sys
import csv

initial_csv_file = sys.argv[1]

from pymongo import MongoClient
client = MongoClient()

client = MongoClient('localhost', 27017)

db = client.resumeclassifier

collection = db.actor_labels

with open(initial_csv_file, 'r', encoding="utf8") as csvfile:

    csvreader = csv.reader(csvfile, delimiter='\t')
    next(csvreader)

    c = 0    
    for row in csvreader:
        actor_id = row[1]
        name = row[3]
        gender = row[4]
        known_for_titles = row[5].split(',')

        print(actor_id, name)

        collection.insert_one({
            "actor_id": actor_id,
            "name": name,
            "gender": gender,
            "known_for_titles": known_for_titles,
            "is_adult" : int(row[6]),
            "is_adventure" : int(row[7]),
            "is_romance" : int(row[8]),
            "is_history" : int(row[9]),
            "is_crime" : int(row[10]),
            "is_western" : int(row[11]),
            "is_fantasy" : int(row[12]),
            "is_documentary" : int(row[13]),
            "is_horror" : int(row[14]),
            "is_mystery" : int(row[15]),
            "is_reality_tv" : int(row[16]),
            "is_talk_show" : int(row[17]),
            "is_sci_fi" : int(row[18]),
            "is_thriller" : int(row[19]),
            "is_news" : int(row[20]),
            "is_action" : int(row[21]),
            "is_war" : int(row[22]),
            "is_animation" : int(row[23]),
            "is_short" : int(row[24]),
            "is_game_show" : int(row[25]),
            "is_comedy" : int(row[26]),
            "is_biography" : int(row[27]),
            "is_sport" : int(row[28]),
            "is_musical" : int(row[29]),
            "is_music" : int(row[30]),
            "is_family" : int(row[31]),
            "is_drama" : int(row[32]),
            "is_film_noir" : int(row[33])
        })
        c += 1

print(c)


client.close()