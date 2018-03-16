import urllib.request
import json
import datetime, time
import pickle

#List of cities for which data is required
location = ['manchester','liverpool','glasgow','london','milan','turin']
#APIXU API Key details
api_key = '' #insert your API Key inside the ' '


def Producer():

    xuList = []#build the list to be serialized

    for i in location: #iterate through the location
        urlData = "http://api.apixu.com/v1/forecast.json?key="+api_key+"&q="+i+"&days=5" #forecast lat/lon
        #urlData = "http://api.apixu.com/v1/search.json?key="+api_key+"&q=London&days=5" #autocomplete
        #urlData = "http://api.apixu.com/v1/current.json?key="+api_key+"&q=London"
        webURL = urllib.request.urlopen(urlData)
        data = webURL.read()
        encoding = webURL.info().get_content_charset('utf-8')
        jsondoc = json.loads(data.decode(encoding))

        # 5 day weather for city
        tempDict = {}
        for j in jsondoc['forecast']['forecastday']: #iterate through the days
            forecasttimestamp = datetime.datetime.fromtimestamp(j['date_epoch'])
            itemp = {forecasttimestamp: {'temp': j['day']['avgtemp_c'],
                                     'ftemp': '',
                                     'weathertype': j['day']['condition']['text'],
                                     'gwind': '', 'swind': j['day']['maxwind_mph'],
                                     'precip_prob': '', 'rain': j['day']['totalprecip_in'], 'location': i}}

            tempDict.update(itemp)
        xuList.append(tempDict)#Dictionary list from a single API request

    return xuList


def main():
    xuList = Producer()
    timestr = str(time.strftime("%Y%m%d_%H%M%S")) #build file name by source type and timestamp
    with open('xu_' + str(timestr) + '.pkl','wb') as f:
        pickle.dump(xuList, f, pickle.HIGHEST_PROTOCOL) # serialize as binary file and output to a folder 'data'
        print('New file created: ', 'xu_' + str(timestr) + '.pkl')

    with open('data/xu_' + str(timestr) + '.pkl','wb') as f:
        pickle.dump(xuList, f, pickle.HIGHEST_PROTOCOL) # serialize as binary file and output to a folder 'data'
        print('New file created: ', 'xu_' + str(timestr) + '.pkl')
    with open('data/xu_' + str(timestr) + '.pkl','rb') as f:  # output to a JSON file in the output_dir
        pick = (pickle.load(f))
        print('pick = ',pick)
if __name__ == '__main__':

    while True:
        try:
            main()
        except:
            time.sleep(300) #sleep 5 minutes if API call fails
            continue
        time.sleep(300) #288 API calls per day:  XU limit is 10000 API calls per mth, or approx 300 per day

