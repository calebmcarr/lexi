# lexi is licensed under CC BY-SA 4.0
# check out the phoible dataset at phoible.org

import matplotlib.pyplot as plt
from matplotlib_venn import venn2
import numpy as np
import pandas as pd

class PHOIBLEDATA():

    def __init__(self, root='../data/phoible/cldf'):
        # get language and IPA data
        self.languages = pd.read_csv(root+'/languages.csv')
        self.values = pd.read_csv(root+'/values.csv')
        # create language ID to name key
        self.langkey = self.languages.set_index('Name')['ID'].to_dict()

    def get_phonemes(self, lang):
        """
        given a lanuage name, return its phonemes and allophones

        Parameters
        ----------
        lang - (str) name of the language in English

        Return
        ------
        lang_inv - (list) [[phoneme, allophones]] pairs
        """

        # get the language code from the name
        name = self.langkey[lang]
        # get all entries related to this language (likely repeats for bigger languages)
        entries = self.values[self.values.Language_ID == name]
        phonemes, allophones = entries.Value, entries.Allophones
        # create all phoneme/allophone pairs
        pairs = [[p,a] for p,a in zip(phonemes, allophones)]
        # remove any pairs where the allophone column was empty
        pairs = [pair for pair in pairs if type(pair[1]) == str]
        # remove repeats
        seen, lang_inv = [], []
        for pair in pairs:
            if pair in seen:
                pass
            else:
                lang_inv.append(pair)
                seen.append(pair)
        # finally, turn the space-separated string of allophones to its own list
        lang_inv = [[i[0], list(i[1].split(" "))] for i in lang_inv]

        return lang_inv

    def compare_phonemes(self, lang1, lang2):
        """
        given two languages, compare their phoneme & allophone inventory

        Parameters
        ----------
        lang1 - (str) name of the first language in English
        lang2 - (str) name of the second language in English

        Return
        ------
        stats
        """

        # grab inventory of both
        inv1 = self.get_phonemes(lang1)
        inv2 = self.get_phonemes(lang2)
        # just phonemes of both
        inv1_phonemes = [i[0] for i in inv1]
        inv2_phonemes = [i[0] for i in inv2]
        # get intersection and differences
        intersect = list(set(inv1_phonemes).intersection(inv2_phonemes))
        lang1_unique = [x for x in inv1_phonemes if x not in set(inv2_phonemes)]
        lang2_unique = [x for x in inv2_phonemes if x not in set(inv1_phonemes)]

        stats = [intersect, lang1_unique, lang2_unique]

        return stats

    def plot_Venn(self, stats, lang1, lang2):
        """
        Given the stats of two languages, plot the Venn diagram of 
        phonemic overlap

        Parameters
        ----------
        stats - (list) return from self.compare_phonemes()
        lang1 - (str) first language
        lang2 - (str) second language

        return
        ------
        plt - the matplotlib plt to show
        """
        intersect, lang1_unique, lang2_unique = stats
        venn2(subsets = (len(lang1_unique), len(lang2_unique), len(intersect)), 
              set_labels = (lang1, lang2))
        plt.title('Phonemic Comparison of '+lang1+' and '+lang2)
        plt.show()
        
        #return plt