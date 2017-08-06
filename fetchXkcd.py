import requests
import json

xkcdJsonFile = "xkcd.json"


def getAllXKCDJson():
    i = 1
    rCode = 200
    result = []
    while rCode != 404 or i < 410:
        try:
            print i
            r = requests.get("https://xkcd.com/"+str(i)+"/info.0.json")
            rCode = r.status_code
            result.append(r.json())

        except Exception as e:
            if i != 404:
                rcode = 404
            else:
                rcode = 200

        i += 1
    return result

def storeXKCDJson(xkcdJson):
    json.dump(xkcdJson, open(xkcdJsonFile, 'w+'))


if __name__ == "__main__":
    storeXKCDJson(getAllXKCDJson())
