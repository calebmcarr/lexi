from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib_venn import venn2
import nltk
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
import numpy as np
import seaborn as sns

from phoible import PHOIBLEDATA
from evaluate import Text, ngramCatplot, transitionMap

if __name__ == "__main__":
    p = PHOIBLEDATA()
    """
    print('Simple phoneme inventory test')
    lang_inv = p.get_phonemes('Spanish')
    print(lang_inv, len(lang_inv))
    """

    
    lang1, lang2 = 'English', 'Spanish'
    print('comparing '+lang1+' and '+lang2)
    stats = p.compare_phonemes(lang1, lang2)
    print('Intersection: '+str(stats[0]))
    print('Unique to '+lang1+': '+str(stats[1]))
    print('Unique to '+lang2+': '+str(stats[2]))

    print('Venn diagram')
    p.plot_Venn(stats, lang1, lang2)
    

    """
    T = Text('../data/texts/English/Declaration/ipa.txt', mode='ipa')
    tProbs = transitionMap(T, True)
    """