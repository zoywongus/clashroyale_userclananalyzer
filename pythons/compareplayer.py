import requests
import json
import sys
player1 = '%23' + sys.argv[1].replace('#','')
player2 = '%23' + sys.argv[2].replace('#','')
url1 = "https://api.clashroyale.com/v1/players/" + playertag
url2 = "https://api.clashroyale.com/v1/players/"+ player2tag


headers = {
    'authorization': sys.argv[3],
    'content-type': "application/json",
    'cache-control': "no-cache",
    }
r1 = requests.request("GET", url1, headers=headers)
r1 = r1.json()
r2 = requests.request("GET", url1, headers=headers)
r2 = r2.json()


#TODO UPDATE THIS JSON AND ANALYZE Data
returnjson = {'jsons':[r1,r2]}
print(json.dumps({returnjson}))
sys.stdout.flush()
#####update this!!!!

#
