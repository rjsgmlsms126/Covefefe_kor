# Covefefe_kor
한국어의 feature를 추출하기위한 feature extractor

## Installation

## USAGE
cvsSplitter.py --> 40만문장의 aimerge.csv 한-영번역문을  aihub_split 폴더에 50개씩 20000개의 csv로 쪼개줌

extract_postoken.py --> aihub_split 폴더의 각각 20000개의 corpus에 대해서 클렌징

extract_all.py -->  extract_postoken.py에서 클렌징한 데이터를 pos, token 추출

feature.py --> feature 추출

feature_all.py --> output_folder에  token.txt 를 extract_feature.csv에 feature.py의 함수에서 추출된 피처들을 한줄씩 입력

function_all.py --> get_frequency_norms, get_mpqa_lexicon, get_ksenticnet 함수호출

functiontable_all.py --> function_tags 태그

ksenticnet.py --> 감정분석 테이블

stopwords.py --> 불용어 테이블

## Known Bugs
