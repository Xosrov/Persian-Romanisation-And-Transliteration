#define constants:
_File = 'output.txt' #output file after words are found
_MAX_GUESS = 4 #number of similar words to check; doesn't necessarily mean it will produce this number of results
import requests
import json
import re
#WEB-BASED( fastdic dictionary -- best source found for now.. )
def Fa2PhinWeb(word):
    #get suggestions first:
    headers = {"referer": "https://fastdic.com"}
    suggestions = requests.post(url = 'https://fastdic.com/suggestions', 
                                json = {"word":word}, 
                                headers=headers)
    suggestionsJson = json.loads(suggestions.text)
    Counter = 0
    with open(_File, 'w') as f:
        PhinRegex = re.compile("phonetics.*?<strong>(.*?)<", re.DOTALL)
        ReplaceShitRegex = re.compile("[\d#&@;:]")
        for i in suggestionsJson:
            if(Counter == _MAX_GUESS):
                break
            webpage = requests.post(url = 'https://fastdic.com/getresult', 
                                    json = {"word":i["word"]}, 
                                    headers=headers)
            try:
                f.write(re.sub(ReplaceShitRegex, '',re.search(PhinRegex, webpage.text).group(1)) + '\n')
            except AttributeError:
                continue
            else:
                Counter += 1
#WEB-BASED(google transliterator , works with other languages as well):
def Phin2FaWeb(word, lang = "fa"): # "lang" is your language code 
    webpage = requests.get('https://inputtools.google.com/request?text='
                            + word
                            + '&itc='
                            + lang
                            + '-t-i0-und&num='
                            + str(_MAX_GUESS)
                            + '&cp=0&cs=1&ie=utf-8&oe=utf-8'
                            + '&app=transliterate')
    all = json.loads(webpage.content)
    with open(_File, 'w') as f:
        for i in all[1][0][1]:
            f.write(i + '\n')

word = input("Enter a word: ")
# uses a try except to detect non ascii characters, determines which function is needed
try:
    word.encode('ascii')  
except UnicodeEncodeError:
    Fa2PhinWeb(word)
else:
    Phin2FaWeb(word)

#deprecated, reason: no efficient way to get information as whole webpage needed to be downloaded
'''
    webpage = requests.get("https://www.vajehyab.com/ajax/suggest?q=" + word)
    SuggestionJson = json.loads(webpage.content)
    print(SuggestionJson)
    numOfGuess = 0
    with open(file, 'w') as f:
        webpage = requests.get("https://www.vajehyab.com/?q=" + word + "&t=like")
        soup = BeautifulSoup(webpage.content, 'html.parser')
        phoneticMain = soup.find("div", {"id": "wordbox"}).section.header.h3.text.replace('/','')
        if(phoneticMain != ''):
                f.write(phoneticMain)
                numOfGuess += 1
                f.write('\n')
        for i in SuggestionJson['suggestions']:
            if(numOfGuess == _MAX_GUESS):
                break
            webpage = requests.get("https://www.vajehyab.com" + i['link'] + "&t=like")
            soup = BeautifulSoup(webpage.content, 'html.parser')
            phonetic = soup.find("div", {"id": "wordbox"}).section.header.h3.text.replace('/','')
            if(phonetic != '' and phonetic != phoneticMain):
                f.write(phonetic)
                numOfGuess += 1
                f.write('\n')
'''