import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import string
import re
from nltk.corpus import stopwords
data_set= pd.read_csv('data.csv')
punctuations = '''`÷×؛<>_()*&^%][ـ،/:"؟.,'{}~¦+|!”…“–ـ''' + string.punctuation
# Arabic stop words with nltk
stop_words = stopwords.words()
# remove diacritics
arabic_diacritics = re.compile("""
                             ّ    | # Shadda
                             َ    | # Fatha
                             ً    | # Tanwin Fath
                             ُ    | # Damma
                             ٌ    | # Tanwin Damm
                             ِ    | # Kasra
                             ٍ    | # Tanwin Kasr
                             ْ    | # Sukun
                             ـ     # Tatwil/Kashida
                         """, re.VERBOSE)
def preprocess(text):
    '''
    text is an arabic string input
    
    the preprocessed text is returned
    '''
    #remove punctuations
    translator = str.maketrans('', '', punctuations)
    text = text.translate(translator)
    # remove Tashkeel
    text = re.sub(arabic_diacritics, '', text)
    #remove longation
    text = re.sub("[إأآا]", "ا", text)
    text = re.sub("ى", "ي", text)
    text = re.sub("ؤ", "ء", text)
    text = re.sub("ئ", "ء", text)
    text = re.sub("ة", "ه", text)
    text = re.sub("گ", "ك", text)
    text = ' '.join(word for word in text.split() if word not in stop_words)
    return text
data_set['response'] = data_set['response'].apply(preprocess)
data_set['question'] = data_set['question'].apply(preprocess)

print(data_set.head(5))

data_set.to_csv('fichier_preprocessed.csv', index=False)