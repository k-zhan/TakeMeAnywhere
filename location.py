import datetime as dt

a = dt.datetime(1969,12,31,17,00,00)
b = dt.datetime(2019,1,21,17,00,00)

later = (b-a).total_seconds()

from yelpapi import YelpAPI

api_key = "rjiw4tkx0VX6AlHGyQouQ7O6iGg200JYpV42Ta__XVKm-swEPcZMrgs-Ut1PCUj7zJyj2LmrmbCMdYeY0rglz0_hZCj9bfak7FHWCNaO4OdLpun1_R3MtFxaU1I6XHYx"
yelp_api = YelpAPI(api_key)
response1 = yelp_api.search_query(term='food', location='waterloo, ON', limit=2)
response2 = yelp_api.search_query(term='attractions', location='toronto', limit=2)


import googlemaps
from datetime import datetime

gmaps = googlemaps.Client(key='AIzaSyD4E6MEwHgTLqIuYvhnenmMxpAVXM2Rzds')


now = datetime.now()

directions_result = gmaps.directions((response1['businesses'][0]['coordinates']),
                                     (response2['businesses'][0]['coordinates']),
                                     mode="driving",
                                     avoid="ferries",
                                     departure_time=later
                                    )

print(directions_result[0]['legs'][0]['distance']['text'])
print(directions_result[0]['legs'][0]['duration']['text'])