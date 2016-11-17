# Gerard Dobbs
# November 2016
# Word Game Project

import random
import collections
import operator
from collections import Counter
from datetime import datetime
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
def getWord():
    with open('/home/gerdobbs/mysite/sourceWords.txt') as file:
        listOfWords = list(file)
        randomWord = random.choice(listOfWords).strip()
        session['randomWord'] = randomWord
        session['randomWord1'] = randomWord.lower()
        return session['randomWord1']


def isWordLongEnough(userWord):
    if len(session['randomWord1']) > 2:
        return True
    else:
        return False
#Check if users word is in Dictionary


def existsInDict(userWord):
    with open('/home/gerdobbs/mysite/smallWords.txt') as file:
        for word in file:
            word = word.strip()
            if word == userWord:
                return True
        return False
#Check if all Letters in Users Word are in Source Word
def checkLettersInWord(randomWord, userWord):
	wordToCheck = randomWord
	#Loop through the letters in the users word
	for letter in userWord:
		#Check if letter is in the Source Word
		if letter in wordToCheck:
			#Take letter out of Source Word
			wordToCheck = wordToCheck.replace(letter,'',1)
			result = True
		else:
			#As soon as a letter is not found in Source Word then finish Dearch
			result = False
			return result
	return result
#Is users word different to Source Word
def diffFromSource(randomWord, userWord):
	if randomWord == userWord:
		return False
	else:
		return True
#Is there 7 words entered
def noOfWords(data):
	if len(data)>6:
		return True
	else:
		return False
#is there any duplicates
def duplicates(data):
    dup=[]
    for item, count in collections.Counter(data).items():
        if count >1:
           dup.append(item)
    return dup


#---------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/')
def start_game() -> 'html':
    session.clear()
    session.setdefault('checker',False)
    session['startTime'] = datetime.now()
    return render_template('/startGame.html', title='WordGame', word = getWord())
@app.route('/display_game', methods=['POST'])
def display_game() -> 'html':
    session['startTime'] = datetime.now()
    return render_template('/displayForm.html', title='WordGame', word = getWord())
@app.route('/processGame', methods=['POST'])
def process_the_data() -> str:
    session['finishTime'] = datetime.now()
    timeTaken = session['finishTime'] - session['startTime']
    data = []
    phrase = []
    for k, v in request.form.items():
        if v != '':
            data.append(v.strip().lower())
    for v in data:
        if existsInDict(v) != True:
            word = v+" does not exist"
            phrase.append(word)
        if checkLettersInWord(session['randomWord1'], v)!= True:
            word = v+"'s letters are not in " + session['randomWord1']
            phrase.append(word)
        if diffFromSource(session['randomWord1'],v) !=True:
            word= v+" Is same as "+ session['randomWord1']
            phrase.append(word)
        if isWordLongEnough(v) != True:
            word = v+" is not 3 letter's or more"
            phrase.append(word)
    for w in duplicates(data):
        phrase.append(w + ' is duplicated.')
    #if duplicates(data):
        #phrase.append(str(session['dup']))
        #phrase.append("Is a duplicate")
    if noOfWords(data) != True:
        phrase.append( "You have not entered 7 words")
    session['phrase']=phrase
    phrase2=''
    if len(phrase)>0:
        for w in phrase:
            phrase2=phrase2+' '+w+'\n'
            dis ='none'
    else:
        phrase2 ="WELL DONE YOU"
        dis='block'
    data3 = ''
    for w in data:
        data3 = data3+' '+w
    return render_template('displayForm2.html', title='WordGame', word1 = session['phrase'],word=session['randomWord'],
        word2=data3,display=dis,displayText=dis,time=timeTaken)
@app.route('/leaderBoardAction', methods=['POST'])
def sendLeadres() -> str:
    if session['checker'] == True:
        return redirect(url_for('start_game'))
    winners = open('/home/gerdobbs/mysite/winners.txt', 'a')
    print(request.form['inputTime'],request.form['inputName'].strip(),sep=',',file = winners)
    winners = open('/home/gerdobbs/mysite/winners.txt', 'r')
    print(''.join(sorted(winners)).strip(),file=open('/home/gerdobbs/mysite/winners.txt', 'w'))
    dic = {}
    position=0
    count=1
    leaderboard=[]
    with open('/home/gerdobbs/mysite/winners.txt') as content:
        for line in content:
            line=line.strip()
            time,name= line.split(',')
            if time == request.form['inputTime']:
                position=count
            count=count+1
            leaderboard.append((time,name))
        if len(line) > 9:
            number=10
        else:
            number=len(line)
        session['checker'] = True
        print(session['checker'])
    return render_template('/displayLeaderBoard.html', title='WordGame', word = getWord(),number=number,list=leaderboard,position=position)
app.config['SECRET_KEY'] = "YES"
