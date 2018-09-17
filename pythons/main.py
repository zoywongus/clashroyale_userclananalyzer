import requests
import json
import sys
playertag = '%23' + sys.argv[1].replace('#','')
clantag = '%23' + sys.argv[2].replace('#','')
url = "https://api.clashroyale.com/v1/players/" + playertag
urlbattle = "https://api.clashroyale.com/v1/players/"+ playertag+"/battlelog"

headers = {
    'authorization': sys.argv[3],
    'content-type': "application/json",
    'cache-control': "no-cache",
    }
r = requests.request("GET", url, headers=headers)
r = r.json()
totalcards = 0
upgradecosts = 0
try:
    for i in r['cards']:
        maxlevel = i['maxlevel']
        level = i['level']
        totalcards += i['count']
        if (maxlevel - level == 12):
            upgradecosts += 185625
        elif (maxlevel - level == 11):
            upgradecosts += 185620
        elif (maxlevel - level == 10):
            upgradecosts += 185600
        elif (maxlevel - level == 9):
            upgradecosts += 185450
        elif (maxlevel - level == 8):
            upgradecosts += 185400
        elif (maxlevel - level == 7):
            upgradecosts += 185000
        elif (maxlevel - level == 6):
            upgradecosts += 184000
        elif (maxlevel - level == 5):
            upgradecosts += 182000
        elif (maxlevel - level == 4):
            upgradecosts += 178000
        elif (maxlevel - level == 3):
            upgradecosts += 170000
        elif (maxlevel - level == 2):
            upgradecosts += 150000
        elif (maxlevel - level == 1):
            upgradecosts += 100000
except:
    return {}


rb = requests.request("GET", urlbattle, headers=headers)
rb = rb.json()

def gettotallevel(cardslst):
    ###LEVELS AWAY FROM MAXXING OUT TO CALC!
    lvl = 0
    for item in cardslst:
        lvl += item['maxLevel'] - item['level']
    return lvl

totalcrowns = 0
opponentcrowns = 0
leveladvantage = 0
starttrophyadvantage = 0
count = 0
try:
    for item in rb:
        count += 1
        totalcrowns += item['team'][0]['crowns']
        opponentcrowns += item['opponent'][0]['crowns']
        starttrophyadvantage = starttrophyadvantage + item['team'][0]['startingTrophies'] - item['opponent'][0]['startingTrophies']
        leveladvantage = leveladvantage + gettotallevel(item['opponent'][0]['cards']) - gettotallevel(item['team'][0]['cards'])

    returnjson = {
                    'name': r['name'],
                    'winpercent':r['wins']/(r['battlecount']),
                    'donateratio':r['donations']/r['donationsReceived'],
                    'favecard': r['currentFavouriteCard']['name'],
                    'cardsleft':totalcards,
                    'costsforupgrades':upgradecosts
                    'crownspergame': totalcrowns/count,
                    'opponentcrownspergame': opponentcrowns/count,
                    'trophyadvantage': starttrophyadvantage/count,
                    'lvladvantagepercard': leveladvantage/count
                }
except:
    return {}
# Takes first name and last name via command
# line arguments and then display them
print(json.dumps({returnjson}))
sys.stdout.flush()
