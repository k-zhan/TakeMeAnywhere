from yelpapi import YelpAPI
api_key = "rjiw4tkx0VX6AlHGyQouQ7O6iGg200JYpV42Ta__XVKm-swEPcZMrgs-Ut1PCUj7zJyj2LmrmbCMdYeY0rglz0_hZCj9bfak7FHWCNaO4OdLpun1_R3MtFxaU1I6XHYx"

import time
import datetime

yelp_api = YelpAPI(api_key)

from flask import Flask,request,render_template

import geocoder
g = geocoder.ip('me')

import googlemaps
from datetime import datetime
gmaps = googlemaps.Client(key='AIzaSyD4E6MEwHgTLqIuYvhnenmMxpAVXM2Rzds')

app = Flask(__name__)

''' @app.route("/", methods=['GET', 'POST'])
def home():
    #if request.method == 'POST':
    #    return 'Submitted form.' '''

'''   return ''' '''<form method="POST">
                 Search: <input type="text" name="search"><br>
                 Location: <input type="text" name="location"><br>
                 <input type="submit" value="Submit"><br>
            </form>'''

@app.route("/")
def home():
    return render_template("home.html")
@app.route('/',methods=['POST']) #allow both GET and POST requests
def submit():
    #loc = request.form['loc']
    #query = request.form['query']
    #query_res = yelp_api.search_query(term = query, location = loc, limit=5)

    if request.method == 'POST':  #this block is only entered when the form is submitted
        loc = request.form.get('loc')
        num_hrs = request.form.get('num_hrs')
        tot_num_hrs = num_hrs
        #query = request.form['query']
        #year = request.form['year']
        #month = request.form['month']
        #day = request.form['day']
        #hour = request.form['hour']
        #minute = request.form['minute']

        #num_rest = request.form['num_rest']
        num_act = int(request.form['num_act'])
        query_res = yelp_api.search_query(term = "activities", location = loc, limit= num_act)
        result_string = ''
        html = ''
		
        for i in range(num_act):
            html += "<p style='background-color:DodgerBlue;font-size:30px'> "
            html += query_res['businesses'][i]['name'] + "" #['location']['display_address'])
            html += "</p>"
            html += "Location: <br>"
            for j in range(len(query_res['businesses'][i]['location']['display_address'])):
                html += (query_res['businesses'][i]['location']['display_address'][j]) + "<br>"
            # html += query_res['businesses'][i]['location']['display_address']
            html += "<br>"
            time_counter = datetime.now()
			
            # Now compute the distances:
            if (i == num_act - 1):
               directions_result = gmaps.directions(query_res['businesses'][i]['coordinates'],
				                                     g.latlng,
                                                    mode="driving",
                                                    avoid="ferries",
                                                    departure_time=time_counter
                                                    )
            elif (i == 0):
                directions_result = gmaps.directions(g.latlng,
                                                     query_res['businesses'][i]['coordinates'],
                                                     mode="driving",
                                                     avoid="ferries",
                                                     departure_time=time_counter
                                                     )
            else:
                directions_result = gmaps.directions(query_res['businesses'][i]['coordinates'],
									                 query_res['businesses'][i+1]['coordinates'],
                                                     mode="driving",
                                                     avoid="ferries",
                                                     departure_time=time_counter
                                                    )
            print(directions_result[0]['legs'][0]['duration']['text'])
            print(directions_result[0]['legs'][0]['distance']['text'])
            html += "Travel Time: " + str(directions_result[0]['legs'][0]['duration']['text']) + " "
            html += "Distance: " + str(directions_result[0]['legs'][0]['distance']['text'])
            html += "<br>"
            html += "<br>"
            # for k in range(len(directions_result)):
                # html += directions_result[i]
                # print(directions_result[k])


        return html 

if __name__ == "__main__":
    app.run(debug=True)

# Get current location
import geocoder
g = geocoder.ip('me')
print(g.latlng)

# Search from current location
response_cur = yelp_api.search_query(term='attraction', latitude = g.latlng[0],
        longitude = g.latlng[1], limit=2)
print(response_cur['businesses'][0]['location']['display_address'])
print(response_cur['businesses'][0])

response1 = yelp_api.search_query(term='ice cream', location='m1s 4h8', limit=2)
print(response1['businesses'][0]['location']['display_address'])