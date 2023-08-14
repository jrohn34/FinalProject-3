import json

def getWordsByLetterCount(letterCount):
    wordFile = open("FinalProject/kb_scrabbleWords.txt", 'r')
    newFile = open("FinalProject/curatedWords.txt", 'w')
    curLine = ""
    count = 0
    lineCount = 0
    wordsFound = [] # we need to keep track of words, because the dictionary calls "Black", "Black and Blue", and "Black Heart" as 'words' that break our rules
    while True:
        try:
            curLine = wordFile.readline() # we don't care about the size
        except:
            continue
        lineCount += 1
        # we do only want the word up to the first space
        pos = 0
        trueWord = ""
        while pos < len(curLine):
            if curLine[pos] == ' ':
                break
            else:
                trueWord += curLine[pos]
                pos+=1
        if len(trueWord) == letterCount+1: # account for newLines
            # account for garbage "words"
            if ',' in trueWord or '.' in trueWord or '/' in trueWord or '0'  in trueWord or '1' in trueWord or '2' in trueWord or '3' in trueWord or '4' in trueWord or '5' in trueWord or '6' in trueWord or '7' in trueWord or '8' in trueWord or '9' in trueWord or '-' in trueWord:
                continue
            elif trueWord in wordsFound:
                continue
            else:
                newFile.write(trueWord)
                wordsFound.append(trueWord)
                count += 1
        if not curLine:
            break
    newFile.close()
    wordFile.close()
    #print("There are ", count, " words")
    return count

def sortByVowelCount():
    wordFile = open("FinalProject/curatedWords.txt", 'r')
    vowelFile = open("FinalProject/wordsByVowel.txt", 'w')
    gigaDictionary = {}
    while True:
        curLine = (wordFile.readline()).upper() # we don't care about the size
        identifier = ""
        for char in curLine:
            if char == 'A' or char == 'E' or char == 'I' or char == 'O' or char == 'U' or char == 'Y':
                identifier += char
        wordList = gigaDictionary.get(identifier) or []
        wordList.append(curLine[0:-1]) # we don't want \n in our dictionary
        gigaDictionary[identifier] = wordList
        if not curLine:
            break
    for key,value in gigaDictionary.items():
        vowelFile.write("%s: %s \n" % (key, value))