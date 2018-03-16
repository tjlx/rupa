#met office data Producer

import metoffer #wrapper around the Met Office API
from reference import club_location
import time
import pickle
from threading import Thread

#List of specific locations for which data is required
location = ['mancity','manunited','liverpoolfc','everton','rangers','partik','celtic',
                    'chelsea','arsenal','tottenham','westham','crystalpalace']

#Dictionary of WeatherTypes description given in MetOffice Data Point
weathertype = {'0':'Clear Night','1':'Sunny day','2':'Partly cloudy (night)','3':'Partly cloudy (day)',
               '5':'Mist','6':'Fog','7':'Cloudy','8':'Overcast','9':'Light rain shower (night)',
               '10':'Light rain shower (day)','11':'Drizzle','12':'Light rain','13':'Heavy rain shower (night)',
               '14':'Heavy rain shower (day)','15':'Heavy rain','16':'Sleet shower (night)',
               '17':'Sleet shower (day)','18':'Sleet','19':'Hail shower (night)','20':'Hail shower (day)',
               '21':'Hail','22':'Light snow shower (night)','23':'Light snow shower (day)','24':'Light snow',
               '25':'Heavy snow shower (night)','26':'Heavy snow shower (day)','27':'Heavy snow',
               '28':'Thunder shower (night)','29':'Thunder shower (day)','30':'Thunder'}

#Met Office API Key details
api_key = '' #insert your API Key inside the ' '
M = metoffer.MetOffer(api_key)

#Data Producer function
def Producer():

    moList = [] #build the list to be serialized

    for i in location: #iterate through all the locations
        city, postcode, lat, lon = club_location(i) # import location details from 'reference.py'
        x = M.nearest_loc_forecast(float(lat), float(lon), metoffer.THREE_HOURLY) #location specific, 3 hourly forecast
        y = metoffer.parse_val(x)
        myDict = y.data #data retrieved from MetOffice
        tempDict = {}
        for m in myDict: #iterate through all the days

            itemp = {m['timestamp'][0]: {'temp': m['Temperature'][0], 'ftemp': m['Feels Like Temperature'][0],
                                     'weathertype':weathertype[str(m['Weather Type'][0])],
                                     'gwind': m['Wind Gust'][0], 'swind': m['Wind Speed'][0],
                                     'precip_prob':m['Precipitation Probability'][0],'rain':'','location':i}}

            tempDict.update(itemp)
        moList.append(tempDict) #list of dictionaries from a single API request

    return moList

def main():
    moList = Producer()
    timestr = str(time.strftime("%Y%m%d_%H%M%S")) #build file name by source type and timestamp

    with open('mo_' + str(timestr) + '.pkl','wb') as f:
        pickle.dump(moList, f, pickle.HIGHEST_PROTOCOL) # serialize as binary file and output to a folder 'data'
        print('New file created: ', 'mo_' + str(timestr) + '.pkl')



    with open('data/mo_' + str(timestr) + '.pkl','wb') as f:
        pickle.dump(moList, f, pickle.HIGHEST_PROTOCOL) # serialize as binary file and output to a folder 'data'
        print('New file created: ', 'mo_' + str(timestr) + '.pkl')
    with open('data/mo_' + str(timestr) + '.pkl','rb') as f:  # output to a JSON file in the output_dir
        pick = (pickle.load(f))
        print('pick = ',pick)

if __name__ == '__main__':

    while True:
        try:
            main()
        except:
            time.sleep(300) #sleep 5 minutes if API call fails
            continue
        time.sleep(300) #288 API calls per day: Limit 5000 per day, 100 per minute if required

