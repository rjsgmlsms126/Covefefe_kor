
import os

nDivCnt= 20

filepath= "C:/Users/rjsgm/PycharmProjects/Covefefe_kor/aihub_data/"
fileNme= "ai_merge"
fileExe= '.csv'

fileFolder="aihub_split/"

dirname=filepath+fileFolder
if not os.path.isdir(dirname):
    os.mkdir(dirname)

nLineCnt=0
nFileIdx=0

f=open("%s" %(filepath+fileNme+fileExe),'r',encoding='UTF8' )

fDivName=open("%s%06d%s" % (filepath+fileFolder+fileNme,nFileIdx,fileExe), 'w',encoding='UTF8')

while True:
    line=f.readline()
    if not line: break

    if nLineCnt ==nDivCnt:
        fDivName.close()
        nFileIdx+=1
        nLineCnt=0
        strPat="%s%06d%s" % (filepath+fileFolder+fileNme,nFileIdx,fileExe)
        fDivName=open(strPat,'w')
        print("생성완료 %s" % strPat)
    nLineCnt+=1
    fDivName.write(line)

fDivName.close()
f.close()