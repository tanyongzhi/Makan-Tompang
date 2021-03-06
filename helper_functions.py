import googlemaps
import json
from operator import itemgetter
import math

def find_min_dist(latlon1, latlon2, point):

    # if same x (vertical line)
    if latlon1[0] == latlon2[0]:
        return abs(point[0] - latlon1[0])
    else:
        slope = (latlon2[1] - latlon1[1]) / (latlon2[0] - latlon1[0])
        intercept = latlon1[1]- slope* (latlon1[0])
        if slope == 0:
            return abs(point[1] - latlon1[1])

    inv_slope = 1/(-slope)
    inv_intercept = point[1]-inv_slope*point[0]
    x_line = (inv_intercept-intercept)/(slope-inv_slope)
    y_line = inv_slope*x_line + inv_intercept
    min_dist = math.sqrt(((point[0]-x_line)**2.0)+((point[1]-y_line)**2.0))

    return min_dist

def get_optimized_slacker_list(all_slackers, dabaoer):
    limited_slacker_list = []

    for slacker in all_slackers:
        if tuple(slacker["restaurant_latlon"]) == dabaoer.restaurant_latlon:
            min_distance = find_min_dist(dabaoer.address_latlon, dabaoer.restaurant_latlon,
                                         slacker['address_latlon'])
            if min_distance < 0.004:
                slacker['dist'] = find_min_dist(dabaoer.address_latlon,
                                    dabaoer.restaurant_latlon,
                                    tuple(slacker["address_latlon"]))

                limited_slacker_list.append(slacker)

    optimized_slacker_list = sorted(limited_slacker_list, key=itemgetter('dist'))
    return optimized_slacker_list

# def get_optimized_slacker_list(all_slackers, dabaoer):
#
#     limited_slacker_list= []
#
#     # get bounding box
#     x1 = dabaoer.address_latlon[0]
#     x2 = dabaoer.restaurant_latlon[0]
#     y1 = dabaoer.address_latlon[1]
#     y2 = dabaoer.restaurant_latlon[1]
#
#     # get eligible slackers and get min dist value
#     for slacker in all_slackers:
#         if tuple(slacker["restaurant_latlon"]) == dabaoer.restaurant_latlon:
#             if (slacker["address_latlon"][0] <= max(x1,x2)) and (slacker["address_latlon"][0] >= min(x1,x2)) and\
#                     (slacker["address_latlon"][1] <= max(y1,y2)) and (slacker["address_latlon"][1] >= min(y1,y2)):
#
#                 # if slacker is within bounding box
#                 slacker['dist'] = find_min_dist(dabaoer.address_latlon,
#                                                             dabaoer.restaurant_latlon,
#                                                             tuple(slacker["address_latlon"]))
#
#                 # print(slacker)
#                 limited_slacker_list.append(slacker)
#
#
#
#     optimized_slacker_list = sorted(limited_slacker_list, key=itemgetter('dist'))
#
#     return optimized_slacker_list

def get_latlon(address):

    gmaps_key = googlemaps.Client(key="AIzaSyB0bPOg9jEX3s8c0QOcSDo3xN88L1HaKd8")

    geocode_result = gmaps_key.geocode(address)

    lat = geocode_result[0]["geometry"]["location"]["lat"]
    lng = geocode_result[0]["geometry"]["location"]["lng"]
    # print("lat: " + str(lat))
    # print("lng: " + str(lng))
    return(lat, lng)
#
# # given a file, returns an array of json objects
# def file_to_object (filename):
#     data = []
#     for line in open(filename, 'r'):
#         data.append(json.loads(line))
#
# a = file_to_object('data1.json')

def json_to_object_list(filename):
    f = open("data.json", "r")
    contents = f.read()
    indiv_dict_str = (contents.split('}'))
    object_list = []
    for i in indiv_dict_str[:-1]:
       object_list += [json.loads(i + '}')]
    return object_list


# given a file, returns an array of json objects 
def file_to_object (filename):
    return json.load(filename)

# given an array of python objects, output a json string that can be passed to the 
# js frontend
def beautify_json(objs):
    json_string = json.dumps([ob for ob in objs])
    return json_string
