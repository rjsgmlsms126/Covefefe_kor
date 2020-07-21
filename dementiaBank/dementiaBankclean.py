import re



def clean_str(text):
    pattern = 'PAR'
    text = re.sub(pattern=pattern, repl='', string=text)
    pattern = 'INV'
    text = re.sub(pattern=pattern, repl='', string=text)
    pattern = 'exc'
    text = re.sub(pattern=pattern, repl='', string=text)
    pattern = 'End'
    text = re.sub(pattern=pattern, repl='', string=text)
    pattern = '\t'
    text = re.sub(pattern=pattern, repl='', string=text)
    pattern = '([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)' # E-mail제거
    text = re.sub(pattern=pattern, repl='', string=text)
    pattern = '(http|ftp|https)://(?:[-\w.]|(?:%[\da-fA-F]{2}))+' # URL제거
    text = re.sub(pattern=pattern, repl='', string=text)
    pattern = '([ㄱ-ㅎㅏ-ㅣ]+)'  # 한글 자음, 모음 제거
    text = re.sub(pattern=pattern, repl='', string=text)
    pattern = '<[^>]*>'         # HTML 태그 제거
    text = re.sub(pattern=pattern, repl='', string=text)
    pattern='[-‘·.=+,■#/\?▶:^$@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]'
    text=re.sub(pattern=pattern,repl='',string=text)
    pattern ='[\d,]*'
    text=re.sub(pattern=pattern,repl='',string=text)
    #text=re.sub('\s+', ' ', string=text)
    return text

for i in range(100,310):
    cName = str(i)
    mp4Dir = '/Users/rjsgm/PycharmProjects/Covefefe_kor/dementiaBank/dementia/' + cName
    mp4Dir1 = '/Users/rjsgm/PycharmProjects/Covefefe_kor/dementiaBank/dementia_clean/' + cName
    with open(mp4Dir+'.txt','r',encoding='UTF-8') as file_object:
        contents = file_object.read()
    cleanControl = clean_str(contents)
    f_pos = open(mp4Dir1+'.txt', 'w', encoding='UTF-8')
    f_pos.write(cleanControl)






