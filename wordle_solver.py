import pandas as pd
import random

def inclTheseLetters(currWords: pd.DataFrame, inclLetters: list) -> pd.DataFrame:
    for letter in inclLetters:
        currWords = currWords[currWords.apply(lambda row: letter in row['WORD'], axis = 1)]
    
    return currWords

def getFilteredWords(currWords: pd.DataFrame, currGuess: str, colorClue: str) -> pd.DataFrame:
    currGuess = currGuess.lower()
    colorClue = colorClue.lower()
    inclLetters = []

    for ind, i in enumerate(colorClue):
        if i == 'g':
            currWords = currWords[currWords[f'L{ind + 1}'] == currGuess[ind]]
    
    for ind, i in enumerate(colorClue):
        if i == 'x':
            if currGuess.count(currGuess[ind]) > 1:
                currWords = currWords[currWords.apply(lambda row: currGuess[ind] != row['WORD'][ind], axis = 1)]
            
            else:
                currWords = currWords[currWords.apply(lambda row: currGuess[ind] not in row['WORD'], axis = 1)]
    
    for ind, i in enumerate(colorClue):
        if i == 'o':
            currWords = currWords[currWords[f'L{ind + 1}'] != currGuess[ind]]
            inclLetters.append(currGuess[ind])
    
    currWords = inclTheseLetters(currWords, inclLetters)

    return currWords

def getRandomWord(currWords: pd.DataFrame) -> str:
    return currWords.loc[random.choice(currWords.index)]['WORD']

def main():
    roundNum = 1
    currClue = '____'
    
    currWords = pd.read_csv('wordle_words.csv')
    currWords['WORD'] = currWords['L1'] + currWords['L2'] + currWords['L3'] + currWords['L4'] + currWords['L5']

    print(f'{"-" * 30}Welcome{"-" * 30}')
    print(
        '''
        Letter not present - 'X',
        Letter present, wrong Pos - 'O',
        Letter present, right Pos - 'G'
        '''
    )
    print('Please follow the above format')
    
    nextWord = 'SLATE'

    while True:
        if roundNum > 6:
            print('We are sorry for letting you down! We will do better next time!')
            break
        
        if roundNum == 1:
            print(f'Enter the First Word of your choice in Wordle! We suggest SLATE')
        
        print(f'\nSuggested Word: {nextWord.upper()}')

        if len(currWords) == 1:
            print("Voila!! We got our Word! Congratulations!!")
            print('Excellent!!')

            break
        
        print(f'Total Possible Words: {len(currWords)}')
        currGuess = input('Enter either your Word or "1" to suggest another or "2" if the suggested Word is Correct: ').strip().lower()

        if currGuess == '1':
            nextWord = getRandomWord(currWords)
            continue

        if currGuess == '2':
            print('Excellent!!')
            break
        
        currClue = input('Enter your Clue: ').strip().lower()

        if currClue == 'ggggg':
            print('Excellent!!')
            break

        currWords = getFilteredWords(currWords, currGuess, currClue)
        nextWord = getRandomWord(currWords)
        
        roundNum += 1

if __name__ == '__main__':
    main()