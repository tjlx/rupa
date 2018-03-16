

def club_location(club):

    location_data = [

        {'club': 'mancity', 'city': 'manchester', 'postcode': 'm160ra',
            'coord': {'lat': '53.463091', 'lon': '-2.291335'}},
        {'club': 'manunited', 'city': 'manchester', 'postcode': 'm113ff',
            'coord': {'lat': '53.483171', 'lon': '-2.200388'}},
        {'club': 'liverpoolfc', 'city': 'liverpool', 'postcode': 'l40th',
            'coord': {'lat': '53.430934', 'lon': '-2.960803'}},
        {'club': 'everton', 'city': 'liverpool', 'postcode': 'l44el',
            'coord': {'lat': '53.439174', 'lon': '-2.966199'}},
        {'club': 'rangers', 'city': 'glasgow', 'postcode': 'g512xd',
            'coord': {'lat': '55.853295', 'lon': '-4.309212'}},
        {'club': 'partik', 'city': 'glasgow', 'postcode': 'g207al',
            'coord': {'lat': '55.881493', 'lon': '-4.269352'}},
        {'club': 'celtic', 'city': 'glasgow', 'postcode': 'g403re',
            'coord': {'lat': '55.849731', 'lon': '-4.205554'}},
        {'club': 'chelsea', 'city': 'london', 'postcode': 'sw61hs',
            'coord': {'lat': '51.482315', 'lon': '-0.191312'}},
        {'club': 'arsenal', 'city': 'london', 'postcode': 'n77aj',
            'coord': {'lat': '51.554928', 'lon': '-0.109066'}},
        {'club': 'tottenham', 'city': 'london', 'postcode': 'n170ap',
            'coord': {'lat': '51.603472', 'lon': '-0.066155'}},
        {'club': 'westham', 'city': 'london', 'postcode': 'e202st',
            'coord': {'lat': '51.539080', 'lon': '-0.016378'}},
        {'club': 'crystalpalace', 'city': 'london', 'postcode': 'se256pu',
            'coord': {'lat': '51.399783', 'lon': '-0.085007'}},
        {'club': 'acmilan', 'city': 'milan', 'postcode': '20151 MI',
            'coord': {'lat': '45.478319', 'lon': '9.124016'}},
        {'club': 'intermilan', 'city': 'milan', 'postcode': '20151 MI',
            'coord': {'lat': '45.478319', 'lon': '9.124016'}},
        {'club': 'juventus', 'city': 'turin', 'postcode': '10151 TO',
            'coord': {'lat': '45.109719', 'lon': '7.641290'}},
        {'club': 'torino', 'city': 'turin', 'postcode': '10134 TO',
            'coord': {'lat': '45.042096', 'lon': '7.650106'}}

        ]

    for i in location_data:
        if i['club'] == club:
            city = (i['city'])
            postcode = (i['postcode'])
            lat = (i['coord']['lat'])
            lon = (i['coord']['lon'])



    return city,postcode,lat,lon
