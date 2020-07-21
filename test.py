from koalanlp.Util import initialize
from koalanlp.proc import Tagger
from koalanlp import API
from nltk.tokenize import word_tokenize
import pandas as pd
import re
initialize(EUNJEON='LATEST')
tagger = Tagger(API.EUNJEON)




contents1= pd.read_csv("C:/Users/rjsgm/PycharmProjects/Covefefe_kor/aihub_data/aihub_split/ai_merge000000.csv")
contents2=contents1["원문"]

word_tokens2=[]
cleanResult=[]
sentences=[]

for row in contents2:
    word_tokens2.append(word_tokenize(row))

#print(word_tokens2)
#print(len(word_tokens2))



with open('/Users/rjsgm/PycharmProjects/Covefefe_kor/input_folder/a.txt','r',encoding='UTF-8') as file_object:
    contents = file_object.read()

f_pos = open('/Users/rjsgm/PycharmProjects/Covefefe_kor/output_folder/pos.txt', 'w',encoding='UTF-8')
f_token = open('/Users/rjsgm/PycharmProjects/Covefefe_kor/output_folder/token.txt', 'w',encoding='UTF-8')


word_tokens=word_tokenize(contents)


def clean_str(text):
    pattern = '([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)' # E-mail제거
    text = re.sub(pattern=pattern, repl='', string=text)
    pattern = '(http|ftp|https)://(?:[-\w.]|(?:%[\da-fA-F]{2}))+' # URL제거
    text = re.sub(pattern=pattern, repl='', string=text)
    pattern = '([ㄱ-ㅎㅏ-ㅣ]+)'  # 한글 자음, 모음 제거
    text = re.sub(pattern=pattern, repl='', string=text)
    pattern = '<[^>]*>'         # HTML 태그 제거
    text = re.sub(pattern=pattern, repl='', string=text)
    pattern='[-‘·=+,#/\?:^$@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]'
    text=re.sub(pattern=pattern,repl='',string=text)
    pattern ='[\d,]*'
    text=re.sub(pattern=pattern,repl='',string=text)
    return text




def pos_token_extract(sentences):
    for i, sent in enumerate(sentences):
        print("===== Sentence #$i =====")
        sentenceswrite=sent.surfaceString()
        #f_pos.write(sentenceswrite)
        #f_pos.write("\n")
        #f_token.write(sentenceswrite)
        #f_token.write("\n")

        print(sentenceswrite)
        print("# Analysis Result")

        for word in sent:
            wordId=word.getId()
            wordSurf=word.getSurface()
            wordSum=str(wordId) + wordSurf
            f_token.write(wordSurf + ' ')

            for morph in word:
                morphSurf=morph.getSurface()
                morphTag=morph.getTag()
                morphSum=str(morphSurf) + str(morphTag)+"\n"
                #f.write("\t"+str(morphSurf)+"/"+str(morphTag)+"\n")
                f_pos.write(str(morphTag)+',')
                f_pos.write(str(morphSurf) + '\n')


    f_pos.close()
    f_token.close()

def cleandata(data):
    cleanResult.append(clean_str(data))

    sentences.append(tagger(cleanResult))
    #for sent in sentences[-1]:
    #    pos_token_extract(sent)
   # pos_token_extract(sentences[-1])

def Nocleandata(data):
    sentences=list(tagger(data))
    pos_token_extract(sentences)

def makeSentence(contents2):
    for sent in contents2:
        cleandata(sent)

makeSentence(contents2)
pos_token_extract(sentences[-1])

