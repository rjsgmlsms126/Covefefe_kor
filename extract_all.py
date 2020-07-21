import extract_postoken
import time
import pandas as pd
import os


def pos_token_extract(sentences):
    for i, sent in enumerate(sentences):
        #print("===== Sentence #$i =====")
        sentenceswrite=sent.surfaceString()
        #f_pos.write(sentenceswrite)
        #f_pos.write("\n")
        #f_token.write(sentenceswrite)
        #f_token.write("\n")

        #print(sentenceswrite)
        #print("# Analysis Result")

        for word in sent:
            wordId=word.getId()
            wordSurf=word.getSurface()
            wordSum=str(wordId) + wordSurf
            f_token.write(wordSurf + ' ')
            if str(wordSurf) == '.':
                f_token.write('\n')

            for morph in word:

                morphSurf=morph.getSurface()
                morphTag=morph.getTag()
                morphSum=str(morphSurf) + str(morphTag)+"\n"
                #f.write("\t"+str(morphSurf)+"/"+str(morphTag)+"\n")
                f_pos.write(str(morphTag)+',')
                f_pos.write(str(morphSurf) + '\n')
                if str(morphSurf) =='.':

                    f_pos.write('\n')


    f_pos.close()
    f_token.close()



for i in range(10000 ,20001):
    cName="ai_merge0"+str(i)
    mp4Dir = '/Users/rjsgm/PycharmProjects/Covefefe_kor/ubuntu'
    contents1 = pd.read_csv("C:/Users/rjsgm/PycharmProjects/Covefefe_kor/aihub_data/aihub_split/" + cName + '.csv',
                            encoding='CP949', names=['SID', '원문', '번역문'], header=None)
    contents2 = contents1["번역문"]

    if not os.path.isdir(mp4Dir):
        os.mkdir(mp4Dir)
    f_pos = open(mp4Dir + '/pos.txt', 'w', encoding='UTF-8')
    f_token = open(mp4Dir + '/'+cName+'.txt', 'w', encoding='UTF-8')

    #f_token = open(mp4Dir + '/token.txt', 'w', encoding='UTF-8')

    extract_postoken.makeSentence(contents2)

    sentences=extract_postoken.sentences

    pos_token_extract(sentences[-1])
    print(i)



