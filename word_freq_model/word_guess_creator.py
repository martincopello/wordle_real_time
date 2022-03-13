import numpy as np
import pandas as pd

# Most Frequent English Words on the Web from kaggle dataset
# get the word freq and filter for 5 letter words
freq = pd.read_csv('word-frequencies.txt',header=None)
freq.columns = ['word','freq']
print(freq.shape[0])
freq['word_len'] = freq['word'].str.len()
freq = freq[freq['word_len'] == 5]
print(freq.shape[0])

# wordle allowed guesses from wordle site
guess = pd.read_csv('wordle-allowed-guesses.txt',header=None)
guess.columns = ['word']
print(guess.shape[0])

# inner join - drops words with no freq bc they are weird words
df = guess.merge(freq, on='word', how='inner')
df = df[['word','freq']]
print(df.shape[0])
df.to_csv('possible_solutions_freq.txt',index=False)
