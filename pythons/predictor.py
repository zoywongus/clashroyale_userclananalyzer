from sklearn import svm
import requests
import json
import sys
import operator

playertag = '%23' + sys.argv[1].replace('#','')
clantag = '%23' + sys.argv[2].replace('#','')
headers = {
    'authorization': sys.argv[3],
    'content-type': "application/json",
    'cache-control': "no-cache",
    }

url = "https://api.clashroyale.com/v1/players/" + playertag + "/battlelog"
r = requests.request("GET", url, headers=headers)
r = r.json()
arr = []
x_arr = []
crown_arr = []
try:
    for item in r:
        crown_arr.append(item['team'][0]['crowns'])
        arr.append(item['team'][0]['startingTrophies'])
    arr = list(reversed(arr))
    crown_arr = list(reversed(crown_arr))
    lenarr = len(arr)
    for count in arr:
        x_arr.append([len(x_arr) + 1])

    #get best card
    countdict = {}
    opponentdict = {}
    ilose = {}
    opponentwin={}
    for battle in r:
        if (battle['team'][0]['crowns'] > battle['opponent'][0]['crowns']):
            for card in battle['team'][0]['cards']:
                if (card['name'] in countdict):
                    countdict[card['name']] += 1
                else:
                    countdict[card['name']] = 1

            for card in battle['opponent'][0]['cards']:
                if (card['name'] in opponentdict):
                    opponentdict[card['name']] += 1
                else:
                    opponentdict[card['name']] = 1
        elif (battle['team'][0]['crowns'] < battle['opponent'][0]['crowns']):
            for card in battle['team'][0]['cards']:
                if (card['name'] in ilose):
                    ilose[card['name']] += 1
                else:
                    ilose[card['name']] = 1

            for card in battle['opponent'][0]['cards']:
                if (card['name'] in opponentwin):
                    opponentwin[card['name']] += 1
                else:
                    opponentwin[card['name']] = 1
except:
    return {}

#prediction for trophy
svm_regression_model = svm.SVR(kernel='rbf')
svm_regression_model.fit(x_arr,arr)

predict_short = svm_regression_model.predict([[len(arr) * 2]])[0]
predict_long = svm_regression_model.predict([[len(arr) * 50]])[0]
strongest_use = max(countdict.iteritems(), key=operator.itemgetter(1))[0]
strongest_opponent = max(opponentwin.iteritems(), key=operator.itemgetter(1))[0]
weakest_use = max(ilose.iteritems(), key=operator.itemgetter(1))[0]
weakest_opponent = max(countdict.iteritems(), key=operator.itemgetter(1))[0]

#prediction for crownstotal
svm_regression_model.fit(x_arr,crown_arr)
battlesahead = 10
crown_short = svm_regression_model.predict([[len(arr) * battlesahead]])[0]
while (crown_short < 2.5 or battlesahead > 300):
    battlesahead += 5
    crown_short = svm_regression_model.predict([[len(arr) * battlesahead]])[0]

predict_3_crown = battlesahead

x = [[1],[4],[7],[13],[10]]
y1 = [16, 34, 52, 88, 70]
y2 = [1, 16, 49, 169, 100]

returnjson = {
    'crownshort': predict_short,
    'crownlong': predict_long,
    'mestrong': strongest_use,
    'oppstrong': strongest_opponent,
    'meweak': weakest_use,
    'oppweak': weakest_opponent,
    'next3crown': predict_3_crown - 10
}

#TODO add scikit learn stuff for clan predictions

print(json.dumps({returnjson}))
sys.stdout.flush()
