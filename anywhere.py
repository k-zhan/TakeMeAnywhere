from yelpapi import YelpAPI
api_key = "rjiw4tkx0VX6AlHGyQouQ7O6iGg200JYpV42Ta__XVKm-swEPcZMrgs-Ut1PCUj7zJyj2LmrmbCMdYeY0rglz0_hZCj9bfak7FHWCNaO4OdLpun1_R3MtFxaU1I6XHYx"

import math
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

#''' @app.route("/", methods=['GET', 'POST'])
#def home():
#    #if request.method == 'POST':
    #    return 'Submitted form.' '''

#'''   return ''' '''<form method="POST">
 #                Search: <input type="text" name="search"><br>
 #                Location: <input type="text" name="location"><br>
 #                <input type="submit" value="Submit"><br>
 #           </form>'''

@app.route("/")
def home():
    return render_template("home.html")

@app.route('/', methods=['POST']) #allow both GET and POST requests
def submit():
    #loc = request.form['loc']
    #query = request.form['query']
    #query_res = yelp_api.search_query(term = query, location = loc, limit=5)

    if request.method == 'POST':  #this block is only entered when the form is submitted
        loc = request.form.get('loc')
        num_hrs = int(request.form.get('num_hrs'))
        tot_num_hrs = num_hrs
        #query = request.form['query']
        #year = request.form['year']
        #month = request.form['month']
        #day = request.form['day']
        #hour = request.form['hour']
        #minute = request.form['minute']
        num_meals = math.floor(tot_num_hrs / 4.0 )
        #num_rest = request.form['num_rest']
        #num_act = int(request.form['num_act'])
        num_act = (abs(tot_num_hrs - num_meals) / 2.5)
        query_res = yelp_api.search_query(term = "activities", location = loc, limit=50) # max value for limit
        food_query = yelp_api.search_query(term = "food", location = loc, limit=50)

        #print(query_res['businesses'])# [20]) #['coordinates'])
        result_string = ''
        html = ''
        i = 1
        #gap = 0
        #permgap = 0
        time_counter = datetime.now()

        # Set counters for attraction and food:
        food_counter = 0
        attr_counter = 0

        # Start with one attraction:
        directions_result = gmaps.directions(g.latlng,
                                             query_res['businesses'][attr_counter]['coordinates'],
                                             mode="driving",
                                             departure_time=time_counter
                                             )
        if (len(directions_result) == 0):
                #print("bad: ", query_res['businesses'][i]['name'])
                num_act += 1
                attr_counter += 1

        prev_coords = query_res['businesses'][attr_counter]['coordinates']
        num_hrs = num_hrs - (directions_result[0]['legs'][0]['duration']['value'] / 3600.0)

        # html += "<p style='background-color:DodgerBlue;font-size:30px'> "
        # html += str(i) + "." + query_res['businesses'][attr_counter]['name'] + " " #['location']['display_address'])
        # html += "</p>"
        # html += "Location: <br>"
        # for j in range(len(query_res['businesses'][attr_counter]['location']['display_address'])):
        #     html += (query_res['businesses'][attr_counter]['location']['display_address'][j]) + "<br>"
        # # html += query_res['businesses'][i]['location']['display_address']
        # html += "<br>"
                        
        # html += "Travel Time: " + str(directions_result[0]['legs'][0]['duration']['text']) + " "
        # html += "Distance: " + str(directions_result[0]['legs'][0]['distance']['text'])
        # html += "<br>"
        # html += "<br>"

        w = str(query_res['businesses'][attr_counter]["url"])
        html += "<div style='background-color:Black;color:white;font-size:30px'> "
        html += "<a href=" + "'"+ w + "'" + "style='color:white;'" + ">"  + str(i) + ". " + query_res['businesses'][attr_counter]['name'] + " " #['location']['display_address'])
        html += "</a><br>"
        html += "<h2>"+"<img src=" + "'" + str(query_res['businesses'][attr_counter]["image_url"]) + "'" + "align='left'" + "width='280'" + "height='280'>" + "</h2>" 
        html += "Location: <br>"
        for j in range(len(query_res['businesses'][attr_counter]['location']['display_address'])):
            html += (query_res['businesses'][attr_counter]['location']['display_address'][j]) + "<br>"
        # html += query_res['businesses'][i]['location']['display_address']
        html += "<br>"
        html += "Travel Time: " + "<span style='color:#FF0000'>" + str(directions_result[0]['legs'][0]['duration']['text']) + "</span>"+ "<br>"
        html += "Distance: " + "<span style='color:#FF0000'>" + str(directions_result[0]['legs'][0]['distance']['text']) + "</span>"
        html += "<br>"
        html += "<br>" + "</div>" + "<br>"

        res1 = False
        res2 = False
        res3 = False

        attr_counter += 1
        i += 1

        while (num_hrs > 0):
                res1 = False
                res2 = False
                res3 = False
                #print("hrs:", num_hrs)
                #print("i:", i)


                #print("food ctr: ", food_counter)
                #print("num meals: ", num_meals)
                if (food_counter < num_meals):
                        res1 = True
                        print("case1")
                        directions_result = gmaps.directions(prev_coords,
                            food_query['businesses'][food_counter]['coordinates'],
                            mode="driving",
                            departure_time=time_counter
                            )
                        prev_coords = food_query['businesses'][food_counter]['coordinates']
                
                        if (len(directions_result) == 0):
                            #print("bad: ", query_res['businesses'][i]['name'])
                            num_meals += 1
                            food_counter += 1
                            continue

                        # Now print to output:

                        w = str(food_query['businesses'][food_counter]["url"])
                        html += "<div style='background-color:Black;color:white;font-size:30px'> "
                        html += "<a href=" + "'"+ w + "'" + "style='color:white;'" + ">"  + str(i) + ". " + food_query['businesses'][food_counter]['name'] + " " #['location']['display_address'])
                        html += "</a><br>"
                        html += "<h2>"+"<img src=" + "'" + str(food_query['businesses'][food_counter]["image_url"]) + "'" + "align='left'" + "width='280'" + "height='280'>" + "</h2>" 
                        html += "Location: <br>"
                        for j in range(len(food_query['businesses'][food_counter]['location']['display_address'])):
                            html += (food_query['businesses'][food_counter]['location']['display_address'][j]) + "<br>"
                        # html += query_res['businesses'][i]['location']['display_address']
                        html += "<br>"
                        html += "Travel Time: " + "<span style='color:#FF0000'>" + str(directions_result[0]['legs'][0]['duration']['text']) + "</span>"+ "<br>"
                        html += "Distance: " + "<span style='color:#FF0000'>" + str(directions_result[0]['legs'][0]['distance']['text']) + "</span>"
                        html += "<br>"
                        html += "<br>" + "</div>" + "<br>"

                        # Update counter
                        i += 1
                        food_counter += 1
                        num_hrs = num_hrs - (directions_result[0]['legs'][0]['duration']['value'] / 3600.0)

                print("attr ctr: ", attr_counter)
                print("num act: ", num_act)

                if (attr_counter < num_act):
                        res2 = True
                        print("case2")
                        directions_result = gmaps.directions(prev_coords,
                                                                                         query_res['businesses'][attr_counter]['coordinates'],
                                                     mode="driving",
                                                     departure_time=time_counter
                                                    )
                        prev_coords = query_res['businesses'][attr_counter]['coordinates']
                
                        if (len(directions_result) == 0):
                            #print("bad: ", query_res['businesses'][i]['name'])
                            num_act += 1
                            attr_counter += 1
                            continue

                        # Now print to output:

                        w = str(query_res['businesses'][attr_counter]["url"])
                        html += "<div style='background-color:Black;color:white;font-size:30px'> "
                        html += "<a href=" + "'"+ w + "'" + "style='color:white;'" + ">"  + str(i) + ". "+ query_res['businesses'][attr_counter]['name'] + " " #['location']['display_address'])
                        html += "</a><br>"
                        html += "<h2>"+"<img src=" + "'" + str(query_res['businesses'][attr_counter]["image_url"]) + "'" + "align='left'" + "width='280'" + "height='280'>" + "</h2>" 
                        html += "Location: <br>"
                        for j in range(len(query_res['businesses'][attr_counter]['location']['display_address'])):
                            html += (query_res['businesses'][attr_counter]['location']['display_address'][j]) + "<br>"
                        # html += query_res['businesses'][i]['location']['display_address']
                        html += "<br>"
                        html += "Travel Time: " + "<span style='color:#FF0000'>" + str(directions_result[0]['legs'][0]['duration']['text']) + "</span>"+ "<br>"
                        html += "Distance: " + "<span style='color:#FF0000'>" + str(directions_result[0]['legs'][0]['distance']['text']) + "</span>"
                        html += "<br>"
                        html += "<br>" + "</div>" + "<br>"

                        # Update counter
                        i += 1
                        attr_counter += 1
                        num_hrs = num_hrs - (directions_result[0]['legs'][0]['duration']['value'] / 3600.0)

                print("attr ctr: ", attr_counter)
                print("num act: ", num_act)

                if (attr_counter < num_act):
                        res3 = True
                        print("case3")
                        directions_result = gmaps.directions(prev_coords,
                                                             query_res['businesses'][attr_counter]['coordinates'],
                                                     mode="driving",
                                                     departure_time=time_counter
                                                    )

                        prev_coords = query_res['businesses'][attr_counter]['coordinates']
                
                        if (len(directions_result) == 0):
                            #print("bad: ", query_res['businesses'][i]['name'])
                            num_act += 1
                            attr_counter += 1
                            continue

                        # Now print to output:

                        w = str(query_res['businesses'][attr_counter]["url"])
                        html += "<div style='background-color:Black;color:white;font-size:30px'> "
                        html += "<a href=" + "'"+ w + "'" + "style='color:white;'" + ">"+ str(i) + ". " + query_res['businesses'][attr_counter]['name'] + " " #['location']['display_address'])
                        html += "</a><br>"
                        html += "<h2>"+"<img src=" + "'" + str(query_res['businesses'][attr_counter]["image_url"]) + "'" + "align='left'" + "width='280'" + "height='280'>" + "</h2>" 
                        html += "Location: <br>"
                        for j in range(len(query_res['businesses'][attr_counter]['location']['display_address'])):
                            html += (query_res['businesses'][attr_counter]['location']['display_address'][j]) + "<br>"
                        # html += query_res['businesses'][i]['location']['display_address']
                        html += "<br>"
                        html += "Travel Time: " + "<span style='color:#FF0000'>" + str(directions_result[0]['legs'][0]['duration']['text']) + "</span>"+ "<br>"
                        html += "Distance: " + "<span style='color:#FF0000'>" + str(directions_result[0]['legs'][0]['distance']['text']) + "</span>"
                        html += "<br>"
                        html += "<br>" + "</div>" + "<br>"

                        # Update counter
                        i += 1
                        attr_counter += 1
                        num_hrs = num_hrs - (directions_result[0]['legs'][0]['duration']['value'] / 3600.0)
                if (not(res1) and not(res2) and not(res3)):
                    break


        # while (i <= num_act):
        # # Now compute the distances:
        #     if (i == num_act):
        #         #print("last:", i-1 - gap)
        #         directions_result = gmaps.directions(query_res['businesses'][i-1-gap]['coordinates'],
                                    #                                  g.latlng,
        #                                             mode="driving",
        #                                             departure_time=time_counter
        #                                             )
        #     elif (i == 1):
        #         directions_result = gmaps.directions(g.latlng,
        #                                              query_res['businesses'][i - 1]['coordinates'],
        #                                              mode="driving",
        #                                              departure_time=time_counter
        #                                              )
        #     else:
        #         #print("prev:", i - 1 - gap)
        #         #print("cur:", i)
        #         directions_result = gmaps.directions(query_res['businesses'][i - 1 - gap]['coordinates'],
                                                                #                        query_res['businesses'][i]['coordinates'],
        #                                              mode="driving",
        #                                              departure_time=time_counter
        #                                             )
        #     if (len(directions_result) == 0):
        #       #print("bad: ", query_res['businesses'][i]['name'])
        #       gap += 1
        #       permgap += 1
        #       i += 1
        #       num_act += 1
        #       continue

            # gap = 0
            # i += 1
# =======
#             if (len(directions_result) == 0):
#             	#print("bad: ", query_res['businesses'][i]['name'])
#             	gap += 1
#             	permgap += 1
#             	i += 1
#             	num_act += 1
#             	continue

#             html += "<div style='background-color:Black;color:white;font-size:30px'> "
#             html += str(i - permgap) + ". " + query_res['businesses'][i-1-gap]['name'] + " " #['location']['display_address'])
#             html += "</p>"
#             html += "Location: <br>"
#             for j in range(len(query_res['businesses'][i-1-gap]['location']['display_address'])):
#                 html += (query_res['businesses'][i-1-gap]['location']['display_address'][j]) + "<br>"
#             # html += query_res['businesses'][i]['location']['display_address']
#             html += "<br>"
            
			
#             html += "Travel Time: " + str(directions_result[0]['legs'][0]['duration']['text']) + " "
#             html += "Distance: " + str(directions_result[0]['legs'][0]['distance']['text'])
#             html += "<br>"
#             html += "<br>" + "</div>" + "<br>"

#             gap = 0
#             i += 1
# >>>>>>> 1cde57a5e8d39620a3f9e5e3271c7a3c81c50fc8
            # for k in range(len(directions_result)):
                # html += directions_result[i]
                # print(directions_result[k])

        return html 

if __name__ == "__main__":
    app.run(debug=True)

# Get current location
#import geocoder
#g = geocoder.ip('me')
#print(g.latlng)

# Search from current location
#response_cur = yelp_api.search_query(term='activities', location= loctemp)
#print(response_cur['businesses'][20]['coordinates'])
#print(response_cur['businesses'][0])

#response1 = yelp_api.search_query(term='ice cream', location='m1s 4h8', limit=2)
#print(response1['businesses'][0]['location']['display_address'])
