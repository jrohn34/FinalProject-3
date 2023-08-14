import random
from wordCurator import *
from datetime import datetime

printMode = True # determines whether or not we print out all of the steps. I set this to "false" to mass-run since print takes time.
getUserInput = True # determines whether or not we ask for user input. if not, default to below values.
wordSize_global = 5 # how big the word we care about is
wordCount_global = 0 # how many word choices we have [set in the init, don't change this]
runCount = 1 # this is how many times we want the AI to play wordle when we hit "run"
kb_global = "FinalProject/kb_botWords.txt"

# https://github.com/dwyl/english-words -- source for the list of ~500,000 "english words", including proper names and archaic language
# https://raw.githubusercontent.com/sujithps/Dictionary/master/Oxford%20English%20Dictionary.txt - the oxford dictionary, which I may switch to
# https://www.rockpapershotgun.com/wordle-past-answers - source of wordle words
# https://gist.github.com/StevenClontz/4445774#file-mobydick-txt - source of moby dick
frequencyDictionary = {}


def determineLetterFrequency(wordBankFile):  # this just prints to console so i can copy+paste it into a variable in another file
    wordFile = open(wordBankFile, 'r')
    totalChars = 0
    while True:
        curLine = (wordFile.readline()).upper()  # we don't care about the size
        for char in curLine:
            totalChars += 1
            if char == '\n':
                continue
            if char in frequencyDictionary.keys():
                frequencyDictionary[char] += 1
            else:
                frequencyDictionary[char] = 1
        if not curLine:
            break
    for key in frequencyDictionary.keys():
        frequencyDictionary[key] = round((frequencyDictionary[key] / totalChars), 3)
        #print(key, frequencyDictionary[key])


def pickWord(): # the code just picks a random word from the Scrabble Dictionary words of correct size
    wordChoices = open("FinalProject/curatedWords.txt", 'r')
    wordChosen = random.randint(0,wordCount_global-1)  # number comes from a print statement counting the possible 5-letter alphabetic words.
    word = wordChoices.readlines()[wordChosen]
    if printMode:
        print("Chose the word: ", word)
    return word.upper()


def isWord(word): # checks to see if input is a word - only used for manual.
    curLine = ""
    wordChoices = open("FinalProject/curatedWords.txt", 'r')
    while True:
        curLine = wordChoices.readline()
        if curLine.upper()[0:-1] == word:
            return True
        if not curLine:
            return False


def playWordle_manual(boardSize): # allows a human to play wordle with instructions
    word = pickWord(boardSize)
    guesses = 6
    print("----------------------------------------------------------------------")
    print("                          Welcome to Wordle!                          ")
    print("                    We have picked a {} letter word                    ".format(boardSize))
    print(" Guess words and we will tell you if the letters are are in the word  ")
    print("         'G' means that the letter is in the correct location         ")
    print("   'Y' means that the letter is in the wrong spot, but is in the word ")
    print("              'R' means that the letter is not in the word            ")
    print("----------------------------------------------------------------------")
    print("                    You have {} guesses remaining                     ".format(guesses))
    print("                        The word is _ _ _ _ _                         ")
    while guesses > 0:
        # get player input
        validInput = False
        while not validInput:
            playerGuess = input().upper()
            # validate player input; don't count typos / wrong letter counts against the guesses
            if len(playerGuess) != boardSize:
                print("Your word must be of size", boardSize)
                continue
            if not isWord(playerGuess):
                print("We do not recognize that as a word, sorry! Make another guess!")
                continue
            else:
                validInput = True
                guesses -= 1
        # see if the player was correct
        correctString = ""
        iter = 0
        while (iter < len(playerGuess)):
            if playerGuess[iter] == word[iter]:
                correctString += "G"
            elif word.find(playerGuess[iter]) > 0:
                correctString += "Y"
                print(playerGuess[iter], word[iter])
            else:
                correctString += "R"
            iter += 1
        print("----------------------------------------------------------------------")
        print("                    You have {} guesses remaining                     ".format(guesses))
        print("                     You guessed {} {} {} {} {}                       ".format(playerGuess[0],
                                                                                              playerGuess[1],
                                                                                              playerGuess[2],
                                                                                              playerGuess[3],
                                                                                              playerGuess[4]))
        print("                                 {} {} {} {} {}                       ".format(
            correctString[0], correctString[1], correctString[2], correctString[3], correctString[4]))
        if correctString == "GGGGG":
            print("----------------------------------------------------------------------")
            print("                           The word was {}                             ".format(word))
            print("                            Congratulations!                           ")
            print("                          You have won Wordle!                         ")
            return True
    print("You are out of guesses, the word was {}".format(word))
    return False

# we look at letter frequencies to get the "score" of each word; choosing the best one
# readline is a very fast operation. this program runs in less than half of a second despite combing through thousands of words.
# NOTE: originally, "ESSES" was the best word. since wordle is interested in diverse words, we're going to add a weight (+.05) to new letters
def guessFirstWord_ai(): # AI makes its first guess based off of letter frequency
    wordBank = open("FinalProject/curatedWords.txt", 'r')
    guessWordScore = 0
    guessWord = ""
    while True:
        curLine = wordBank.readline()
        lettersfound = []
        curLineScore = 0
        if not curLine:
            break
        elif len(curLine) != wordSize_global + 1:  # recall: \n
            continue
        else:
            for char in curLine:
                if char != '\n':
                    curLineScore += frequencyDictionary[char]
                if char not in lettersfound:
                    curLineScore += .05
                    lettersfound.append(char)

            curLineScore /= wordSize_global
            if curLineScore > guessWordScore:
                guessWordScore = curLineScore
                guessWord = curLine[:-1]
    #print(guessWord)
    return guessWord

def pruneList(answerString, guessWord): # rewrite the word bank file with only the valid words
    wordBank = open("FinalProject/curatedWords.txt", 'r')
    # We want to prune the list of possible words by deleting the invalid options
    requiredLetters = []
    invalidLetters = []
    newFile = []
    # first thing we do is 
    for i in range(len(answerString)):
        if answerString[i] == 'R':
            invalidLetters.append(guessWord[i])
            if printMode:
                print(guessWord[i] + " is not a valid letter")
        if answerString[i] == 'G':
            requiredLetters.append(guessWord[i])
            if printMode:
                print(guessWord[i] + " is a required letter")
        if answerString[i] == 'Y':
            requiredLetters.append(guessWord[i])
            if printMode:
                print(guessWord[i] + " is a required letter")
    while True:
        valid = True
        curLine = wordBank.readline()
        if not curLine:
            break
        for letter in requiredLetters:
            if letter not in curLine:
                valid = False
                break
        for letter in invalidLetters:
            if letter in curLine:
                valid = False
                break
        for i in range(len(answerString)):
            if answerString[i] == 'Y' and curLine[i] == guessWord[i]: # If we know that the current letter is yellow:
                valid = False # this means it will not be re-written to the file
        if valid:
            newFile.append(curLine)
    wordBank = open("FinalProject/curatedWords.txt", 'w')
    for line in newFile:
        wordBank.write(line)
    if printMode:
        print("Pruned to " + str(len(newFile)) + " words")

def guessWord_ai(redWords, yellowWords, greenWords): # ai guesses a word based off of letter frequency
    wordBank = open("FinalProject/curatedWords.txt", 'r')
    guessWordScore = -99
    guessWord = ""
    while True:
        curLine = wordBank.readline()
        lettersfound = []
        curLineScore = 0
        if not curLine:
            break
        #elif len(curLine) != boardSize + 1:  # recall: \n
        #    continue
        else:
            i = 0
            for char in curLine:
                if char in redWords:
                    curLineScore -= 99
                if curLine[i] in greenWords[i]:
                    curLineScore += 1
                if char in yellowWords:
                    curLineScore += 0
                if char != '\n':
                    curLineScore += frequencyDictionary[char]
                if char not in lettersfound:
                    curLineScore += .05
                    lettersfound.append(char)
                    if char in ['a', 'e', 'i', 'o','u','y']: # weight vowels higher
                        curLine+=.03
                if i < len(greenWords) - 1:
                    i += 1
            curLineScore /= wordSize_global
            if curLineScore > guessWordScore:
                guessWordScore = curLineScore
                guessWord = curLine[:-1]
    return guessWord

def playWordle_ai(): # start the sequence for the ai to make guesses, and then write information
    global correctString, ai_guess
    currentTime = datetime.now()
    guesses = 6
    validInput = False
    word = pickWord()
    if printMode:
        print(guessFirstWord_ai())
    redWords = []
    yellowWords = []
    greenWords = ['*', '*', '*', '*', '*', '*']
    while guesses > 0:
        validInput = False
        while validInput == False:
            ai_guess = ""
            if guesses == 6:
                ai_guess = guessFirstWord_ai()
            if guesses <= 5:
                ai_guess = guessWord_ai(redWords, yellowWords, greenWords)
            if len(ai_guess) != wordSize_global:
                print("Your word must be of size", wordSize_global)
                continue
            if not isWord(ai_guess):
                print("We do not recognize that as a word, sorry! Make another guess!")
                continue
            else:
                validInput = True
        if guesses < 6:
            if printMode:
                print(guessWord_ai(redWords, yellowWords, greenWords))
            else:
                guessWord_ai(redWords, yellowWords, greenWords)
        # see if the player was correct
        iter = 0
        correctString = ""
        while iter < len(ai_guess):
            if ai_guess[iter] == word[iter]:
                correctString += "G"
                greenWords[iter] = ai_guess[iter]
            elif ai_guess[iter] in word:
                correctString += "Y"
                yellowWords += ai_guess[iter]
            else:
                correctString += "R"
                redWords += ai_guess[iter]
            iter += 1
        if printMode:
            print(correctString)
        #print(greenWords)
        # see if we're correct
        correct = True
        guesses -= 1
        for char in correctString:
            if char != 'G':
                correct = False
                break
        if correct: # Announce success, and then record in the bot bank
            if printMode:
                print("Success after this many guesses: " + str(6-guesses))
            botBank = open("FinalProject/kb_botWords.txt", "r")
            botLines = []
            while True:
                curLine = botBank.readline()
                if not curLine:
                    break
                elif curLine not in botLines: # We do not want repeated words. We care about uniques only.
                    botLines.append(curLine)
            botBank.close() # apparently you cannot open a file as wr in python...
            botBank = open("FinalProject/kb_botWords.txt", "w")
            for line in botLines:
                botBank.write(line)
            botBank.write(ai_guess+"\n")
            botBank.close()
            # We're also recording the total amount of guesses the bot has
            historyLines = []
            botWinHistory = open("FinalProject/botWinHistory.txt", "r")
            while True:
                curLine = botWinHistory.readline()
                if not curLine:
                    break
                historyLines.append(curLine)
            botWinHistory.close()
            botWinHistory = open("FinalProject/botWinHistory.txt", "w")
            for line in historyLines:
                botWinHistory.write(line)
            botWinHistory.write(str(6-guesses) + "\n")
            botWinHistory.close()
            timeLines = []
            botTimeHistory = open("FinalProject/botTimeHistory.txt", "r")
            while True:
                curLine = botTimeHistory.readline()
                if not curLine:
                    break
                timeLines.append(curLine)
            botTimeHistory.close()
            botTimeHistory = open("FinalProject/botTimeHistory.txt", "w")
            for line in timeLines:
                botTimeHistory.write(line)
            #print("dateTime was: " + str(currentTime))
            #print("dateTime is:" + str(datetime.now()))
            botTimeHistory.write(str((datetime.now()-currentTime).total_seconds()) + "\n")
            botTimeHistory.close()
            break
        else:
            pruneList(correctString, ai_guess)
        if guesses == 0:
            print("No guesses remaining, the word was " + word.upper())
            break

def getAverageGuessCount(): # get the average of the lines in botWinHistory.txt
    total = 0
    count = 0
    botWinHistory = open("FinalProject/botWinHistory.txt", "r")
    while True:
        curLine = botWinHistory.readline()
        if not curLine:
            break
        count += 1
        total += int(curLine)
    return round(total/count, (1+1)) # my two key does not work

def getAverageTime(): # get the average of the lines in botTimeHistory.txt
    total = 0
    count = 0
    botTimeTaken = open("FinalProject/botTimeHistory.txt", "r")
    while True:
        curLine = botTimeTaken.readline()
        if not curLine:
            break
        count += 1
        total += float(curLine)
    return round(total/count, (1+1)) # my two key does not work

if getUserInput: # this is for the purposes of the demo
    print("How many letters is your word?")
    wordSize_global = int(input())
    print("What knowledge base would you like to use?\n 1: Official Scrabble Dictionary\n2: List of official Wordle Words\n3: Moby Dick")
    choice = int(input())
    if choice == 1:
        kb_global = "FinalProject/kb_scrabbleWords.txt"
    if choice == 2:
        kb_global = "FinalProject/kb_wordleWords.txt"
    if choice == 3:
        kb_global = "FinalProject/kb_mobyDick.txt"
    if choice == 4:
        kb_global = "FinalProject/kb_botWords.txt"

# ths is the run initialization for the bot
i = 0

while (i < runCount):
    wordCount_global = getWordsByLetterCount(wordSize_global)
    determineLetterFrequency(kb_global)
    playWordle_ai()
    i+=1
    
    

# playWordle_manual(5) # - only unmark this if you want to play wordle by hand
# print(getAverageGuessCount()) # - this will print the average guesses of the bot so far
# print(getAverageTime()) # - this will print the average times of the bot so far