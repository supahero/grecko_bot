import parser, re, json
import Levenshtein

def pusher(variab):

    url = 'http://tgftp.nws.noaa.gov/data/observations/metar/decoded/'

    icao = ''
    with open('ICAO.json') as json_data:
        data = json.load(json_data)
        for field in data:
            word = field['city']
            try:
                if Levenshtein.ratio(word, variab) >= 0.8:
                    icao = field['icao']
                    break
                elif icao == None:
                    icao = ''
            except TypeError:
                icao = ''
    if len(icao) == 0:
        result = "No Data"
        return result

    ext = icao + '.TXT'

    names, readydict, namedlist = parser.listFD(url, ext)
    # = parser.readydict
    # = parser.namedlist

    #data = request.json
    data = names

    idx = 0
    if len(names) != 0:
    #if 0 <= idx < 30:
        result = readydict[names[idx]] + tempchecker(namedlist, idx) + windchecker(namedlist, idx) \
                 + presschecker(namedlist, idx)
    else:
        result = "No Data"

    #result = jsonify(result)

    return listToString(result)

# searching temp for namedlist
def tempchecker(array, index):
    celcresult = re.search(r"(F\s[(])(.*)(\sC[)])", array[index])
    if celcresult == None:
        return ["No data about temperature"]
    elif float(celcresult.group(2)) <= 0:
        return ['==WARNING:==', 'cold weather']
    else:
        return ["Typical temperature"]


# searching wind for namedlist
def windchecker(array, index):
    mphresult = re.search(r"(at\s)(.*)(\sMPH)", array[index])
    if mphresult == None:
        return ["No data about wind"]
    else:
        try:
            float(mphresult.group(2))
        except ValueError:
            anothermphresult = re.search(r"(at\s)(.*)(\s............g)", array[index])
            if float(anothermphresult.group(2)) >= 20:
                return ['==WARNING:==', 'Storm']
            else:
                return ["Sight wind"]
        else:
            if float(mphresult.group(2)) >= 20:
                return ['==WARNING:==', 'Storm']
            else:
                return ["Sight wind"]


# searching pressure
def presschecker(array, index):
    hparesult = re.search(r"(Hg\s[(])(.*)(\shPa[)])", array[index])
    if hparesult == None:
        return ["No data about atmosphere pressure"]
    elif float(hparesult.group(2)) >= 1016:
        return ['==WARNING:==', 'high atmosphere pressure']
    else:
        return ["Normal atmosphere pressure"]


def listToString(array):
    textblock = ""
    for element in array:
        element = element+'\n'
        textblock += element
    return textblock
