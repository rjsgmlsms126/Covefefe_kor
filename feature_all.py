import collections
from funtiontable import FunctionTable
import functions as f
import pandas as pd
import nltk
import numpy as np
import scipy
import math
import feature as feat
import csv


####피처 하나 쓰는것 까지 ok extract_all처럼 feature_all파일 만들어서 20000개 피쳐 한번에 추출할수있도록
for i in range(1 ,10):

    cName="ai_merge00000"+str(i)
    mp4Dir = '/Users/rjsgm/PycharmProjects/Covefefe_kor/output_folder/' + cName+'/'

    list_file = pd.read_csv(mp4Dir+'pos.txt',names=['pos', 'token'])
    list_file = list_file.fillna(value='NA')
    sentence_file = pd.read_csv(mp4Dir+'token.txt',names=['sentence'])


    featureSum={**feat.get_pos_features(list_file)[1],**feat.get_mpqa_norm_features(list_file)[1],
                **feat.get_vocab_richness_measures(list_file)[1],**feat.get_cosine_distance(list_file)[1]
                ,**feat.get_ksenticnet_synset_feature(list_file)[1]}

    print(featureSum)
    feat.get_pos_features(list_file)[1].clear()
    feat.get_mpqa_norm_features(list_file)[1].clear()
    feat.get_vocab_richness_measures(list_file)[1].clear()
    feat.get_cosine_distance(list_file)[1].clear()
    feat.get_ksenticnet_synset_feature(list_file)[1].clear()

    with open('/Users/rjsgm/PycharmProjects/Covefefe_kor/extrat_feature.csv', 'a+',newline='') as f:
        fieldnames = ['word_length', 'prop_density', 'content_density', 'pronouns',
                      'function', 'adverbs', 'nouns', 'noun_frequency', 'noun_freq_num',
                      'verbs', 'prepositions', 'adjectives', 'determiners', 'verb_frequency',
                      'verb_freq_num', 'frequency', 'freq_num', 'nvratio', 'prp_ratio', 'noun_ratio',
                      'coordinate', 'subordinate', 'sub_coord_ratio', 'mpqa_num', 'mpqa_strong_positive',
                      'mpqa_strong_negative', 'mpqa_weak_positive', 'mpqa_weak_negative', 'MATTR_10',
                      'MATTR_20', 'MATTR_30', 'MATTR_40', 'MATTR_50', 'TTR', 'brunet', 'honore', 'ave_cos_dist',
                      'min_cos_dist', 'cos_cutoff_00', 'cos_cutoff_03', 'cos_cutoff_05', 'synset_number',
                      'synset_len_sum', 'noun_synset_number', 'noun_synset_len_sum', 'verb_synset_number',
                      'verb_synset_len_sum',
                      'avg_ksent_ambig_nn', 'sd_ksent_ambig_nn', 'kurt_ksent_ambig_nn', 'skew_ksent_ambig_nn',
                      'avg_ksent_ambig_vb', 'sd_ksent_ambig_vb', 'kurt_ksent_ambig_vb', 'skew_ksent_ambig_vb',
                      'avg_ksent_ambig', 'sd_ksent_ambig', 'kurt_ksent_ambig', 'skew_ksent_ambig', '']

        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerow(featureSum)
