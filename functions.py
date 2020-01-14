import nltk
import os
import re
import csv
import ksenticnet as k



def get_frequency_norms():
    """Parameters:
    path_to_norms : optional, string. Full path, including filename, of the frequency norms.

    Return dictionary of SUBTL frequencies, keys = words, values = list of norms."""



    with open('C:/Users/rjsgm/PycharmProjects/Covefefe_kor/dic/freq_kor.txt', "r") as fin:
        f = fin.readlines()
        f = f[1:]  # skip header

        freq = {}
        for line in f:
            l = line.strip().split()
            if len(l) == 0:
                continue
            freq[l[0].lower()] = l[1:]  # returns whole line -- usually just use Log10WF

        return freq
    return None


def get_mpqa_lexicon():

    with open('C:/Users/rjsgm/PycharmProjects/Covefefe_kor/dic/mpqa_kor_final.csv', "r",encoding='utf-8') as f:
        reader = csv.reader(f)
        mpqa_list = list(reader)
        words =[word[1] for word in mpqa_list]
        types = [type[0] for type in mpqa_list]
        polarities = [polar[3] for polar in mpqa_list]

    return [words, types, polarities]

def get_ksenticnet():
    ksentKeys = k.ksenticnet.keys()
    ksentValues = k.ksenticnet.values()
    ksentValuesKeys = list(ksentKeys)
    ksentValuesList=list(ksentValues)

    words=[word for word in ksentValuesKeys]
    type1 = [type[4] for type in ksentValuesList]
    type2 = [type[5] for type in ksentValuesList]
    synlen= [len(type[8:]) for type in ksentValuesList]
    return [words,type1,type2,synlen]


#print(get_ksenticnet()[0])
#print(get_ksenticnet()[1])
#print(get_ksenticnet()[2])
#print(get_ksenticnet()[3])
