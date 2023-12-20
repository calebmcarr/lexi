# lexi is licensed under CC BY-SA 4.0

from collections import Counter
from ipatok import tokenise as tokenize
import itertools
import matplotlib.pyplot as plt
import nltk
import numpy as np
import pandas as pd
import seaborn as sns
import string
import re
from typing import Union

def transitionMap(T, plot=True):
    """
    Given a a text, return its transition map

    Parameters
    ----------
    T - class.Text instance
    plot - (bool) if True, prints a map before returning

    Returns
    -------
    transitionProbs - (list) list of every transition probability of bigrams
    """
    # get unigrams and bigrams
    unigrams = T.ngrams(n=1, sample=None, tokens=True, whitespace=False)
    bigrams = T.ngrams(n=2, sample=None, tokens=True, whitespace=False)
    # get unique bigrams and counts as dictionary
    bigram_counts = Counter(bigrams)
    bigrams = list(bigram_counts.keys()) # get valid bigrams in set
    unigram_counts = Counter(unigrams)
    transitionProbs = np.empty((len(unigram_counts), len(unigram_counts)))
    # loop through unigrams to solve Bayesian prob of transition probabilit O(n^2)
    for i, (uni1, count1) in enumerate(unigram_counts.items()):
        count_uni1 = unigram_counts[uni1] # get the number of times phoneme 1 occurs
        # loop through again to get all combos
        for j, (uni2, count2) in enumerate(unigram_counts.items()):
            bi = uni1+uni2 # the bigram
            # check to see if this combo even exists
            if bi not in bigrams:
                transitionProbs[i][j] = 0
            else:
                count_uni1_uni2 = bigram_counts[bi]
                p2_1 = count_uni1_uni2 / count_uni1
                transitionProbs[i][j] = p2_1 # the probability of phon2 given phon1
    # convert to pandas dataframe
    transitionProbs = pd.DataFrame(transitionProbs)
    transitionProbs.columns = list(unigram_counts.keys())
    transitionProbs.index = list(unigram_counts.keys())
    
    if plot:
        sns.heatmap(transitionProbs)
        plt.title('Transition Probabilities')
        plt.tick_params(axis='both', which='major', labelsize=10, labelbottom = False, bottom=False, top = False, labeltop=True)
        plt.show()


    return transitionProbs


def ngramCatplot(ngrams):
    """
    given a list of ngrams, plot a Catplot

    Parameter
    ---------
    ngrams - (list) list of ngrams
    """
    #we join tuples here so we can plot as aunit
    #ngrams = [''.join(gram) for gram in ngrams]
    df = pd.DataFrame(ngrams, columns=['phoneme'])
    sns.catplot(data=df, x="phoneme", kind='count')
    plt.ylabel('Count')
    plt.xlabel('Phoneme')
    plt.show()

class Text():
    """
    This class will read in both normal text and IPA transcriptions.
    Performs various tasks such as tokenizing, ngrams, and basics stats
    """

    def __init__(self, path: str, mode: str='text'):
        self.mode = mode
        # open text and read it, close file
        with open(path, 'r') as f:
            self.text = f.read()
        f.close()
        # remove puncuation and newlines from string
        self.text = self.text.translate(str.maketrans('', '', string.punctuation))
        self.text = self.text.replace("\n", " ")
        """
        # make a list of words/transcriptions. self.text = [[str1], ...,[strN]]
        self.text = self.text.split(' ')
        # also create a tokens variable. need a different tokenizer for IPA
        # self.tokens = [[t0,...,tNi],...,[t0,...,tNk]]
        if self.mode == 'text':
            self.tokens = [list(word) for word in self.text]
        elif self.mode == 'ipa':
            self.tokens = [tokenize(word) for word in self.text]
        """


    def ngrams(self, n: int = 2, sample: Union[int, None] = None,
                tokens: bool = True, whitespace: bool=True):
        """
        Given self.text, returns [sample] number of [n]-grams

        Parameters
        ----------
        n - (int) the size of the n-gram. Must be > 1 (not sure how to enforce this in typing)
        sample - [int, None] the number of n-grams to return. If None, it returns the whole text
        tokens - (bool) if true, n-grams of tokens, if false, n-grams of words
        whitespace - (bool) Text word n-grams will include spaces if true. preserves word boundaries

        Return
        ------
        ngrams - [list] the n-grams
        """
        
        # first determine whether we're doing words or tokens
        if tokens:
            # now build pool whether it's text or IPA transcription
            if self.mode == 'text':
                pool = list(self.text)
            elif self.mode == 'ipa':
                pool = tokenize(self.text)
        else:
            # discriminate b/w IPA and normal text
            if self.mode == 'text':
                # determine whether to preserve word boundaries
                if whitespace:
                    pool = re.split(r'(\s+)', self.text)
                else:
                    pool = self.text.split(' ')
            elif self.mode == 'ipa':
                pass

        # create the n-grams
        # if sample = None (read: all) set the range
        if sample == None:
            sample = len(pool) - n +1
        ngrams = [''.join(pool[i:i+n]) for i in range(sample)]

        return ngrams

class Stats():

    def __init__(self, ngrams: list, ngrams2: Union[list, None] = None):
        """
        For now, Stats just takes ngrams and can do statistical stuff with them

        Parameters
        ----------
        ngrams - (list) the list of ngrams from calling Text.ngrams()
        ngrams2 - (list) optional second language for comparison
        """
        self.ngrams = ngrams
        if ngrams2 != None:
            self.ngrams2 = ngram2

    
