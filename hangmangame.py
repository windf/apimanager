import urllib2
import json
import random
import time
import traceback
import os



playerId = 'ketanjani21@gmail.com'
url = 'https://strikingly-hangman.herokuapp.com/game/on'
headers = {'Content-Type' : 'application/json'}
cacheFile = "cache.txt"

def startGame(playerId):
    if os.path.exists(cacheFile): 
        f = open(cacheFile)
        tmp = f.read()
        f.close()
        data = tmp.split(":")
        print "start game from cache"
        return {'data': {'numberOfGuessAllowedForEachWord': data[2], 'numberOfWordsToGuess': data[3]}, 'sessionId': data[0], 'wordIndex': data[1]} 
    else:
        action = 'startGame'
        post_data = {'playerId': playerId, 'action': action}


        req = urllib2.Request(url = url, data = json.dumps(post_data), headers = headers)
        res = urllib2.urlopen(req)

        if res.getcode() == 200:
            print "start game ok"
            data =  json.loads(res.read())
            return data
        else:
            print "start game error code " + str(res.getcode())
            return None


def getWord(sessionId):
    action = "nextWord"
    post_data = {'sessionId': sessionId, 'action': action}
   
    req = urllib2.Request(url = url, data = json.dumps(post_data), headers = headers)
    res = urllib2.urlopen(req)

    if res.getcode() == 200:
        print "get word ok"
        data =  json.loads(res.read())
        return data
    else:
        print "get word error code " + str(res.getcode())
        return None 


def guessWord(sessionId):
    #guessWord = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    action = "guessWord"
    rand = random.randint(0, len(wordList) - 1) 
    post_data = {'sessionId': sessionId, 'action': action, 'guess': wordList[rand]} 
    wordList.remove(wordList[rand])

    print post_data

    req = urllib2.Request(url = url, data = json.dumps(post_data), headers = headers)
    res = urllib2.urlopen(req)

    if res.getcode() == 200:
        print "guess word ok"
        data =  json.loads(res.read())
        return data
    else:
        print "guess word error code " + str(res.getcode())
        return None

def writeFile(fileName, content):
    try:
        f = open(fileName, "w")
        f.write(content)
        f.close()
    except:
        print traceback.print_exec()

def getResult(sessionId):
    action = "getResult"
    post_data = {'sessionId': sessionId, 'action': action}

    req = urllib2.Request(url = url, data = json.dumps(post_data), headers = headers)
    res = urllib2.urlopen(req)

    if res.getcode() == 200:
        print "get result ok"
        data =  json.loads(res.read())
        return data
    else:
        print "get result error code " + str(res.getcode())
        return None  


def submitResult(sessionId):
    action = "submitResult"
    post_data = {'sessionId': sessionId, 'action': action}

    req = urllib2.Request(url = url, data = json.dumps(post_data), headers = headers)
    res = urllib2.urlopen(req)

    if res.getcode() == 200:
        print "submit result ok"
        data =  json.loads(res.read())
        return data
    else:
        print "submit result error code " + str(res.getcode())
        return None

try:
    for j in range(0, 1000):
        result = startGame(playerId)

        #result = {'message': 'THE GAME IS ON', 'data': {'numberOfGuessAllowedForEachWord': 10, 'numberOfWordsToGuess': 80}, 'sessionId': 'b943a8e2f79b1e2b52925376e700997d'}
        if result is not None:
            if 'wordIndex' in result:
                wordIndex = int(result["wordIndex"])
            else:
                wordIndex = 1

            guessLimit = result['data']['numberOfGuessAllowedForEachWord']

            for i in range(wordIndex, int(result['data']['numberOfWordsToGuess'])+1):
                writeFile(cacheFile, result["sessionId"] + ":" + str(i+1) + ":" + str(guessLimit) + ":" + str(result['data']['numberOfWordsToGuess']))            
     
                wordData = getWord(result['sessionId'])
                print "wordData " + str(i)
                print wordData


                wordList = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
                if wordData is not None:
                    guessResult = guessWord(result['sessionId'])
                    print "first"
                    print guessResult
                    while (guessLimit > guessResult["data"]["wrongGuessCountOfCurrentWord"]):
                        guessResult = guessWord(result['sessionId'])
                        #time.sleep(1) 
                        print "while"
                        print guessResult
                        if guessResult is not None:
                            if guessResult["data"]["word"].count("*") == 0:
                                print "guess success"
                                print guessResult["data"]["word"]
                                break;

        else:
            print "start game error"

        scoreResult = getResult(result['sessionId'])
        print scoreResult
        os.remove(cacheFile) 
        if scoreResult["data"]["score"] >= 1000:
            print "score success " + str(scoreResult["data"]["score"])
            writeFile("success.txt", result['sessionId'])
            print submitResult(result['sessionId'])
            break; 

except:
    traceback.print_exc()
