#!/usr/bin/env python3
import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from wordcloud import WordCloud

# import nltk
# nltk.download('stopwords')
# nltk.download('wordnet')

# Function to convert a raw review to a string of words
# The input is a single string (a raw movie review), and 
# the output is a single string (a preprocessed movie review)
wordnet_lemmatizer = WordNetLemmatizer()
def clean_dialogue( dialogue ):
    # Remove non-letters        
    letters_only = re.sub("[^a-zA-Z]", " ", dialogue) 
    #
    # Convert to lower case, split into individual words
    words = letters_only.lower().split()                             
    #
    # In Python, searching a set is much faster than searching
    #   a list, so convert the stop words to a set
    stops = set(stopwords.words("english"))   

    # Use lemmatization and remove stop words
    meaningful_words = [wordnet_lemmatizer.lemmatize(w) for w in words if not w in stops]   
    #
    # Join the words back into one string separated by space, 
    # and return the result.
    return( " ".join( meaningful_words ))


# Get only lines spoken by out focus characters
def getDialogue(df, name, mName, ):
    dialogs = df[(df['character_name']==name)&(df['movieTitle']==mName)]['cleaned_text_of_utterances'].values
    if dialogs.shape[0]==0:
        print("Not Found")
        return "Not Found"
    return dialogs

# Plot one character and see its word cloud
def getWordCloud(df, chName, mName):
    dialogues= list(getDialogue(df, chName, mName))
    words = [word  for dialog in dialogues for word in dialog.split(" ")]
    wordcloud = WordCloud(max_font_size=40,background_color="white").generate(" ".join(words))
    plt.figure()
    plt.title("%s's word cloud from \"%s\""%(chName,mName))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    
    plt.show()

# Randomly select one character and see its word cloud
def randomWordCloud(df):
    sample = df.sample(1)
    getWordCloud(df, sample['character_name'].values[0],sample['movieTitle'].values[0])