Hello grader(s)!
"wordleBoard.py" is what you want to look at. I (Alec Blanton, aleblant@iu.edu) have added further explanation below:

I designed this bot to store information about how it runs in two files: 
botTimeHistory.txt (which records the seconds between first and last guess of each run)
botWinHistory.txt (which records the guesses each run takes)

On the slides, I put a lot of information about information gain from different results. Sadly the only way to verify that information
is to run the data again. I could not devise a good data storage system in the time I had to work on this + all of the other assignments,
so to compare run times of 4 vs. 5 letter words I had to delete the 5 letter word data. If you are interested to verify, you should get 
similar results if you let the program run. Guessing is very fast, but curating all 10,000 words takes about a few seconds. 
Running it 100 times took me about 5 minutes.

If a file begins with "kb_", then it is a choice for a knowledge base. Using scrabbleWords is ill advised, as that is the word bank for
word guesses.
curatedWords is the list of words of the correct letter size after user input.
wordsByVowel.txt is a sorting system that I did not have time to implement before the presentation.
The rest of the files store information about bot runs.