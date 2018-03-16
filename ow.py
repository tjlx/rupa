import urllib.request
import json
from reference import club_location
import datetime, time
import pickle
import pprint


#List of specific locations for which data is required
location = ['mancity','manunited','liverpoolfc','everton','rangers','partik','celtic',
            'chelsea','arsenal','tottenham','westham','crystalpalace',
            'acmilan','intermilan','juventus','torino']

#Open Weather API Key details
api_key = '' #insert your API Key inside the ' '



def Producer():

    owList = []#build the list to be serialized

    for i in location:#iterate through all the locations
        city, postcode, lat, lon = club_location(i)
        #print(i,city,lat,lon)
        urlData = "http://api.openweathermap.org/data/2.5/forecast?lat="+str(lat)+\
                  "&lon="+str(lon)+"&units=metric&appid="+api_key
        webURL = urllib.request.urlopen(urlData)#API call
        data = webURL.read()
        encoding = webURL.info().get_content_charset('utf-8')
        jsondoc = json.loads(data.decode(encoding))
        #print(jsondoc)
        #pprint.pprint(jsondoc)
        tempDict = {}
        for j in jsondoc:#iterate through the days
            for k in jsondoc['list']:
                timestamp = datetime.datetime.fromtimestamp(k.get('dt'))
                swind = round((k.get('wind').get('speed'))/0.621371,2) #convert kph to mph

                if k.get('3h') == None:
                    rain = None
                else:
                    rain = round((k.get('3h'))/0.0393701) # convert mm to in


                itemp = {timestamp: {'temp': k.get('main').get('temp'), 'ftemp': '',
                                         'weathertype': k.get('weather')[0].get('description'),
                                         'gwind': '', 'swind': swind,
                                         'precip_prob': '', 'rain': rain,'location':i}}

                tempDict.update(itemp)
        owList.append(tempDict)#Dictionary list from a single API request
    return owList

def main():
    owList = Producer()
    timestr = str(time.strftime("%Y%m%d_%H%M%S")) #build file name by source type and timestamp

    with open('ow_' + str(timestr) + '.pkl','wb') as f:
        pickle.dump(owList, f, pickle.HIGHEST_PROTOCOL) # serialize as binary file and output to a folder 'data'
        print('New file created: ', 'ow_' + str(timestr) + '.pkl')

    with open('data/ow_' + str(timestr) + '.pkl','wb') as f:
        pickle.dump(owList, f, pickle.HIGHEST_PROTOCOL) # serialize as binary file and output to a folder 'data'
        print('New file created: ', 'ow_' + str(timestr) + '.pkl')
    with open('data/ow_' + str(timestr) + '.pkl','rb') as f:  # output to a JSON file in the output_dir
        pick = (pickle.load(f))
        print('pick = ',pick)
if __name__ == '__main__':

    while True:
        try:
            main()
        except:
            time.sleep(300) #sleep 5 minutes if API call fails
            continue
        time.sleep(300) #288 API calls per day: OW limit is 60 API calls per minute