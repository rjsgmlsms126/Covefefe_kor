import collections
from funtiontable import FunctionTable
import functions as f
import pandas as pd
import nltk
import numpy as np
import scipy
import math
import ksenticnet as k





feature_dict = collections.defaultdict(int)
pos_features = collections.defaultdict(int)
mpqa_features = collections.defaultdict(int)
vocab_features= collections.defaultdict(int)
cosine_features_dict= collections.defaultdict(int)
ksenticnet_features=collections.defaultdict(int)

#기존의 파일 불러오기
#list_file = open('/Users/rjsgm/PycharmProjects/Covefefe_kor/output_folder/pos.txt', 'r',encoding='UTF-8').read().split('\n')

#새로운 pandas 형식의 txt pos,token 있는 txt파일 불러오기
list_file=pd.read_csv('/Users/rjsgm/PycharmProjects/Covefefe_kor/output_folder/pos.txt',names=['pos','token'])
sentence_file=pd.read_csv('/Users/rjsgm/PycharmProjects/Covefefe_kor/input_folder/a.txt',names=['sentence'])




# freq 가져오기
get_frequency_norms =True
get_pos_ratios=True
get_density=True
norms_freq =f.get_frequency_norms()
norms_word=list(norms_freq.keys())
norms_log10wf=list(norms_freq.values())



mpqa_list = f.get_mpqa_lexicon()
mpqa_words = mpqa_list[0]
mpqa_types = mpqa_list[1]
mpqa_polarities = mpqa_list[2]


total_tk=len(list_file.index)
pos_features['word_length'] =total_tk


inf_value=10^10
nan_value=-1



list_string_file=' '.join(list_file['pos'])
total_words=len(list_file['pos'])


def get_pos_features(data):
    # 데이터 [형태소,단어] 각각 pos , token으로 분리해서 따로 데이터 다루게만듬
    pos = data.loc[:, ['pos']]
    token = data.loc[:, ['token']]
    pos_list = pos.to_dict('list')
    token_list = token.to_dict('list')


    #기본 피처 추가
    pos_keys = ['word_length']
    pos_keys += ['nouns', 'verbs', 'inflected_verbs', 'light', 'function', 'pronouns', 'determiners', 'adverbs',
                 'adjectives', 'prepositions',
                 'coordinate', 'subordinate', 'demonstratives']
    if get_frequency_norms:
        pos_keys += ['frequency', 'noun_frequency', 'verb_frequency']
    if get_pos_ratios:
        pos_keys += ['nvratio', 'prp_ratio', 'noun_ratio', 'sub_coord_ratio']
    if get_density:
        pos_keys += ['prop_density', 'content_density']

    if get_density:
        pos_features['prop_density'] = 0
        pos_features['content_density'] =0

    ########################################################## 여기까지 해결

    for p_value in pos_list.values():
        for i in range(len(p_value)):
            #형태소 txt에서 순번
            pos_num=i

            if get_density:
                if ("NNG" or "VV" or "VA" or "MAG" or "SF" or "SE" or "SSO" or "SSC" or "SC" or "SY") in p_value[i]:
                    pos_features['content_density'] += 1
                if ("VV" or "VA" or "MAG" or "MAJ") in p_value[i]:
                    pos_features['prop_density'] += 1


            if "NN" in p_value[i]:
                pos_features['nouns']=pos_features['nouns']+1

                ##여기서부터 다시 하기 freq
                for t_value in token_list.values():

                   # if t_value[pos_num] in token_list.values():
                        if get_frequency_norms and t_value[pos_num] in norms_word:
                             freq_loc=norms_word.index(t_value[pos_num])
                             pos_features["noun_frequency"] += float(norms_log10wf[freq_loc][1])  # use log10WF
                             pos_features["noun_freq_num"] += 1
                             pos_num=0


            elif "VV" in p_value[i]:
                pos_features['verbs']=pos_features['verbs']+1

                for t_value in token_list.values():

                   # if t_value[pos_num] in token_list.values():
                        if get_frequency_norms and t_value[pos_num] in norms_word:
                             freq_loc=norms_word.index(t_value[pos_num])
                             pos_features["verb_frequency"] += float(norms_log10wf[freq_loc][1])  # use log10WF
                             pos_features["verb_freq_num"] += 1
                             pos_num=0

            else:
                if "NP" in p_value[i]:
                    pos_features['pronouns'] = pos_features['pronouns'] + 1
                elif "MM" in p_value[i]:
                    pos_features['determiners'] = pos_features['determiners'] + 1
                elif "MAG" in p_value[i]:
                    pos_features['adverbs'] = pos_features['adverbs'] + 1
                elif "VA" in p_value[i]:
                    pos_features['adjectives'] = pos_features['adjectives'] + 1
                elif "MAJ" in p_value[i]:
                    pos_features['coordinate'] = pos_features['coordinate'] + 1
                elif ("JKS"or"JKC"or"JKG"or"JKO"or"JKV"or"JKQ") in p_value[i]:
                    pos_features['prepositions'] = pos_features['prepositions'] + 1



            if p_value[i] in FunctionTable.function_tags:
                pos_features['function'] += 1

            if get_frequency_norms and t_value[pos_num] in norms_word:
                freq_loc = norms_word.index(t_value[pos_num])
                pos_features["frequency"] += float(norms_log10wf[freq_loc][1])  # use log10WF
                pos_features["freq_num"] += 1



    if pos_features['verbs']>0:
        pos_features["nvratio"] = 1.0 * pos_features["nouns"] / pos_features["verbs"]
    else:
        if pos_features["nouns"] > 0:
            pos_features["nvratio"] = inf_value


    # Compute noun ratios (pronouns to pronoun+nouns, and nouns to noun+verb)
    if pos_features["nouns"] > 0:
        pos_features["prp_ratio"] = 1.0 * pos_features["pronouns"] / (pos_features["pronouns"] + pos_features["nouns"])
        pos_features["noun_ratio"] = 1.0 * pos_features["nouns"] / (pos_features["verbs"] + pos_features["nouns"])
    else:
        if pos_features["pronouns"] > 0:
            pos_features["prp_ratio"] = 1.0 * pos_features["pronouns"] / (
                        pos_features["pronouns"] + pos_features["nouns"])
        else:
            pos_features["prp_ratio"] = nan_value  # NaN? 0/0 - no nouns and no pronouns

        if pos_features["verbs"] > 0:
            pos_features["noun_ratio"] = 1.0 * pos_features["nouns"] / (pos_features["verbs"] + pos_features["nouns"])
        else:
            pos_features["noun_ratio"] = nan_value  # NaN? 0/0 - no nouns and no verbs

    if pos_features["verbs"] > 0:
        pos_features["noun_ratio"] = 1.0 * pos_features["nouns"] / (pos_features["verbs"] + pos_features["nouns"])
    else:
        pos_features["noun_ratio"] = nan_value  # NaN? 0/0 - no nouns and no verbs

# Compute conjunction ratios
    if pos_features["coordinate"] > 0:
        pos_features["sub_coord_ratio"] = 1.0 * pos_features["subordinate"] / pos_features["coordinate"]
    else:
        if pos_features['subordinate'] > 0:
            pos_features["sub_coord_ratio"] = inf_value
        else:
            pos_features['sub_coord_ratio'] = nan_value  # NaN? 0/0 - no subord and no coord conjunctions

    if pos_features['prop_density'] > 0:
        pos_features['prop_density'] /= total_words
    else:
        pos_features['prop_density'] = nan_value

    if pos_features['content_density'] > 0:
        pos_features['content_density'] /= total_words
    else:
        pos_features['content_density'] = nan_value
# Compute conjunction ratios
    if pos_features["coordinate"] > 0:
        pos_features["sub_coord_ratio"] = 1.0 * pos_features["subordinate"] / pos_features["coordinate"]
    else:
        if pos_features['subordinate'] > 0:
            pos_features["sub_coord_ratio"] = inf_value
        else:
            pos_features['sub_coord_ratio'] = nan_value  # NaN? 0/0 - no subord and no coord conjunctions

    if pos_features['prop_density'] > 0:
        pos_features['prop_density'] /= total_words
    else:
        pos_features['prop_density'] = nan_value

    if pos_features['content_density'] > 0:
        pos_features['content_density'] /= total_words
    else:
        pos_features['content_density'] = nan_value


# Normalize frequency norms
    if pos_features["freq_num"] > 0:
        pos_features["frequency"] = 1.0 * pos_features["frequency"] / pos_features["freq_num"]
    else:
        pos_features["frequency"] = nan_value

    # Normalize frequency norms for nouns
    if pos_features["noun_freq_num"] > 0:
        pos_features["noun_frequency"] = 1.0 * pos_features["noun_frequency"] / pos_features["noun_freq_num"]
    else:
        pos_features["noun_frequency"] = nan_value

    # Normalize frequency norms for verbs
    if pos_features["verb_freq_num"] > 0:
        pos_features["verb_frequency"] = 1.0 * pos_features["verb_frequency"] / pos_features["verb_freq_num"]
    else:
        pos_features["verb_frequency"] = nan_value

    return pos_keys,pos_features

#coisne distance

def get_cosine_distance(data):
    pos = data.loc[:, ['pos']]
    token = data.loc[:, ['token']]
    pos_list = pos.to_dict('list')
    token_list = token.to_dict('list')

    cosine_keys = ["ave_cos_dist", "min_cos_dist", "cos_cutoff_00", "cos_cutoff_03", "cos_cutoff_05"]
    cosine_features_dict = {}

    #fdist_vocab = nltk.probability.FreqDist([for word in norms_word])
    vocab_words = list(fdist_vocab.keys())

    num_utterances = len(norms_word)

    word_vectors = []


def get_mpqa_norm_features(data):



    token = data.loc[:, ['token']]
    token_list = token.to_dict('list')



    mpqa_keys = ['mpqa_strong_positive', 'mpqa_strong_negative', 'mpqa_weak_positive', 'mpqa_weak_negative',
                 'mpqa_num']


    for t_value in token_list.values():
        for i in range(len(t_value)):
            if t_value[i] in mpqa_words:
                mpqa_features["mpqa_num"] += 1
                mpqa_idx = mpqa_words.index(t_value[i])
                mpqa_type = mpqa_types[mpqa_idx]
                mpqa_polarity = mpqa_polarities[mpqa_idx]

                if mpqa_type == 'strong' and mpqa_polarity == 'positive':
                    mpqa_features["mpqa_strong_positive"] += 1
                elif mpqa_type == 'strong' and mpqa_polarity == 'negative':
                    mpqa_features["mpqa_strong_negative"] += 1
                elif mpqa_type == 'weak' and mpqa_polarity == 'positive':
                    mpqa_features["mpqa_weak_positive"] += 1
                elif mpqa_type == 'weak' and mpqa_polarity == 'negative':
                    mpqa_features["mpqa_weak_negative"] += 1

    if mpqa_features["mpqa_num"] > 0:
        mpqa_features["mpqa_strong_positive"] /= 1.0 * mpqa_features["mpqa_num"]
        mpqa_features["mpqa_strong_negative"] /= 1.0 * mpqa_features["mpqa_num"]
        mpqa_features["mpqa_weak_positive"] /= 1.0 * mpqa_features["mpqa_num"]
        mpqa_features["mpqa_weak_negative"] /= 1.0 * mpqa_features["mpqa_num"]
    else:
        mpqa_features["mpqa_strong_positive"] = nan_value
        mpqa_features["mpqa_strong_negative"] = nan_value
        mpqa_features["mpqa_weak_positive"] = nan_value
        mpqa_features["mpqa_weak_negative"] = nan_value

    return mpqa_keys, mpqa_features



def get_vocab_richness_measures(data):
    ''' This function extracts vocabulary richness measures:
    Honore statistic, Brunet index, type-token ratio (TTR), moving average type-token ratio (MATTR)
    Parameters:
    pos_tokens: list of tuples of strings, (token, POS_tag) of non-punctuation tokens.
    lemmatized_tokens: list of strings, lemmatized non-punctuation tokens.
    total_words: int, total number of words.
    inf_value: int, infinity value.
    Returns:
    vocab_keys: list of strings, names of extracted features.
    vocab_features: dictionary, mapping feature name to feature value.
    '''
    pos = data.loc[:, ['pos']]
    token = data.loc[:, ['token']]
    pos_list = pos.to_dict('list')
    token_list = token.to_dict('list')

    vocab_keys = ['TTR', 'brunet', 'honore']
    vocab_features = {}

    pos_tokens = []  # list of tuples of (token, POStag) of non-punctuation tokens
    lemmatized_tokens = []  # list of lemmatized non-punctuation tokens
    for p_value in pos_list.values():
        pos_tokens=p_value
    for t_value in token_list.values():
        lemmatized_tokens=t_value
    # moving average TTR over each window, then average over all windows
    for window_size in [10, 20, 30, 40, 50]:
        start = 0
        end = window_size
        MATTR = 0

        vocab_features['MATTR_%d' % (window_size)] = 0
        vocab_keys += ['MATTR_%d' % (window_size)]
        while end < len(lemmatized_tokens):
            lem_types = len(set(lemmatized_tokens[start:end]))
            MATTR += 1.0 * lem_types / window_size
            start += 1 # shift window one word at a time
            end += 1
        if start > 0:
            vocab_features['MATTR_%d' % (window_size)] = 1.0 * MATTR / start

    word_types = len(set(pos_tokens)) # same word with different POS = different tokens (confirm with Katie)
    fd_tokens = nltk.probability.FreqDist(pos_tokens)

    # Count number of tokens that occur only once in transcript
    once_words = 0
    for num in fd_tokens.values():
        if num == 1:
            once_words += 1

    try:
        vocab_features["TTR"] = 1.0 * word_types / total_words
        vocab_features["brunet"] = 1.0 * total_words**(word_types**(-0.165)) # Brunet's index - Vlado
    except:
        vocab_features["TTR"] = 0
        vocab_features["brunet"] = 0
    try:
        vocab_features["honore"] = 100.0 * math.log(total_words)/(1.0-1.0*once_words/word_types) # Honore's statistic-Vlado
    except:
        vocab_features["honore"] = inf_value #or infinity ...? (If all words are used only once)

    return vocab_keys, vocab_features


def get_cosine_distance(data):


    pos = data.loc[:, ['pos']]
    token = data.loc[:, ['token']]
    pos_list = pos.to_dict('list')
    token_list = token.to_dict('list')

    cosine_keys = ["ave_cos_dist", "min_cos_dist", "cos_cutoff_00", "cos_cutoff_03", "cos_cutoff_05"]
    cosine_features_dict = {}

    words=[]
    for t_value in token_list.values():
        words=t_value
    # REPETITION
    # Build a vocab for the transcript

    fdist_vocab = nltk.probability.FreqDist([word for word in words])
    vocab_words = list(fdist_vocab.keys())


###########################################################################
    #sentence의 수 or num_utterances가 무엇인지?????
    num_utterances = len(sentence_file)

    word_vectors = []
    for i,t_value in enumerate(list(token_list.values())[0]):
        word_vectors.append(len(vocab_words)*[0]) # init
        for j in range(len(vocab_words)):
            if str(vocab_words[j]) in str(t_value):
                word_vectors[i][j] += 1

    average_dist = 0.0
    min_dist = 1.0
    num_similar_00 = 0.0
    num_similar_03 = 0.0
    num_similar_05 = 0.0
    num_pairs = 0
    for i in range(num_utterances):
        for j in range(i):
            norm_i, norm_j = np.linalg.norm(word_vectors[i]), np.linalg.norm(word_vectors[j])
            if norm_i > 0 and norm_j > 0:
                cosine_dist = scipy.spatial.distance.cosine(word_vectors[i], word_vectors[j])
                if math.isnan(cosine_dist):
                    continue
                average_dist += cosine_dist
                num_pairs += 1
                if cosine_dist < min_dist:
                    min_dist = cosine_dist

                if cosine_dist < 0.001: #similarity threshold
                    num_similar_00 += 1
                if cosine_dist <= 0.3: #similarity threshold
                    num_similar_03 += 1
                if cosine_dist <= 0.5: #similarity threshold
                    num_similar_05 += 1


    denom = num_pairs

    if denom >= 1:
        cosine_features = [average_dist * 1.0 / denom,
                           min_dist,
                           num_similar_00 * 1.0 / denom,
                           num_similar_03 * 1.0 / denom,
                           num_similar_05 * 1.0 / denom]
    else:
        # There are either no utterances or a single utterance -- no repetition occurs
        cosine_features = [inf_value, inf_value, 0, 0, 0]

    for ind_feat, feat_name in enumerate(cosine_keys):
        cosine_features_dict[feat_name] = cosine_features[ind_feat]

    return cosine_keys, cosine_features_dict



def get_ksenticnet_feature(data):
    pos = data.loc[:, ['pos']]
    token = data.loc[:, ['token']]
    pos_list = pos.to_dict('list')
    token_list = token.to_dict('list')

    ksenticnet_keys=[]
    ksenticnet_features={}



















get_pos_features(list_file)
get_mpqa_norm_features(list_file)
get_vocab_richness_measures(list_file)
get_cosine_distance(list_file)

print(get_pos_features(list_file)[1])
print(get_mpqa_norm_features(list_file)[1])
print(get_vocab_richness_measures(list_file)[1])
print(get_cosine_distance(list_file)[1])



#print(list_file)
#print(mpqa_features.keys())
#print(collections.Counter(pos_features))
#print(collections.Counter(mpqa_features))
#print(collections.Counter(vocab_features))

