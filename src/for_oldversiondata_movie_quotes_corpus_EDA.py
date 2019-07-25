#!/usr/bin/env python3
import fileinput
import pandas as pd

## Part 1: txt to csv, if already have converted csv, do not need this part

# When can not read txt directly to DataFrame, change txt format.(need to be improved)
# If can convert txt to df directly, do not need this function.
def read_txt(filename):
    with fileinput.FileInput(filename, inplace=True, backup='.bak') as file:
        for line in file:
            print(line)
            try:
                print(line.replace(" +++$+++ ", "\t"), end='')
            except:
                line.encode('utf-8').strip()
                print(line.replace(" +++$+++ ", "\t"), end='')
# # usage example
# read_txt('movie_characters_metadata.txt')
# read_txt('movie_conversations.txt')
# read_txt('movie_titles_metadata.txt')
# read_txt('movie_lines.txt')


# Convert changed txt to df and save to csv
def txt_to_df(filename, df_columnsname):
    return pd.read_csv(filename, sep="\t", header=None, error_bad_lines=False, names=df_columnsname, engine='python')
# # usage example
# characters_metadata_cols = ['characterID', 'character_name', 'movieID', 'movieTitle', 'gender', 'position_in_credits']
# conversations_cols = ["characterID_First", "characterID_second", "movieID", "list_of_utterances"]
# titles_metadata_cols = ['movieID', 'movieTitle', 'movieYear', 'IMDB_rating', 'numIMDBvotes', 'Genres']
# lines_cols = ['lineID', 'characterID', 'movieID', 'character_name', 'text_of_utterances']

# characters_metadata_df = txt_to_df('movie_characters_metadata.txt', characters_metadata_cols)
# conversations_df = txt_to_df('movie_conversations.txt', conversations_cols)
# titles_metadata_df = txt_to_df('movie_titles_metadata.txt', titles_metadata_cols)
# lines_df = txt_to_df('movie_lines.txt', lines_cols)

# Save to csv: df.to_csv(csv_filename, index=False)


## Part 2: ?