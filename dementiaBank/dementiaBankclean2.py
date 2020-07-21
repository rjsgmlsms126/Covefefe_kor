import fileinput
import re

with open('/Users/rjsgm/PycharmProjects/Covefefe_kor/dementiaBank/control/1.txt','r',encoding='UTF-8') as file_object:
    contents = file_object.read()

path_to_file = 'data/nicknames.txt'
text = open('/Users/rjsgm/PycharmProjects/Covefefe_kor/dementiaBank/control/1.txt', 'rb').read().decode(encoding='utf-8')
print(text)
# Define unwanted nicknames and substitute them
unwanted_nickname_list = ['INV']
text = re.sub("|".join(unwanted_nickname_list), "", text)

print(text)

""""""
def clean_str(text):
    pattern = '([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)' # E-mail제거
    text = re.sub(pattern=pattern, repl='', string=text)
    pattern = '(http|ftp|https)://(?:[-\w.]|(?:%[\da-fA-F]{2}))+' # URL제거
    text = re.sub(pattern=pattern, repl='', string=text)
    pattern = '([ㄱ-ㅎㅏ-ㅣ]+)'  # 한글 자음, 모음 제거
    text = re.sub(pattern=pattern, repl='', string=text)
    pattern = '<[^>]*>'         # HTML 태그 제거
    text = re.sub(pattern=pattern, repl='', string=text)
    pattern='[-‘·=+,#/\?▶:^$@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]'
    text=re.sub(pattern=pattern,repl='',string=text)
    pattern ='[\d,]*'
    text=re.sub(pattern=pattern,repl='',string=text)
    #pattern = 'PAR'
    #text = re.sub(pattern=pattern, repl='', string=text)
    return text





cleanControl=clean_str(contents)
print(cleanControl)

