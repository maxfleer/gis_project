from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.urls import reverse_lazy
from .forms import RegisterForm
from .models import *
from geopy import distance
import random
import xyzservices.providers as xyz
import folium
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def find_variable_name(html, name_start):
    variable_pattern = "var "
    pattern = variable_pattern + name_start

    starting_index = html.find(pattern) + len(variable_pattern)
    tmp_html = html[starting_index:]
    ending_index = tmp_html.find(" =") + starting_index

    return html[starting_index:ending_index]

def create_folium_map(map_filepath, center_coord, location_id, user_id):
    # create folium map
    map = folium.Map(center_coord, zoom_start=12)

    # add popup
    folium.LatLngPopup().add_to(map)

    #tile_provider = xyz.Stadia.StamenWatercolor

    # Update the URL to include the API key placeholder
    #tile_provider["url"] = tile_provider["url"] + \
    #    "?api_key=3dd06860-7f01-4788-84c7-e0e74854b30d"

    # Create the folium TileLayer, specifying the API key
    #folium.TileLayer(
    #    tiles=tile_provider.build_url(
    #        api_key='3dd06860-7f01-4788-84c7-e0e74854b30d'),
    #    attr=tile_provider.attribution,
    #    name=tile_provider.name,
    #    max_zoom=tile_provider.max_zoom,
    #    detect_retina=True
    #).add_to(map)

    folium.LayerControl().add_to(map)

    # store the map to a file
    map.save(map_filepath)

    # read ing the folium file
    html = None
    with open(map_filepath, 'r') as mapfile:
        html = mapfile.read()

    # find variable names
    map_variable_name = find_variable_name(html, "map_")
    popup_variable_name = find_variable_name(html, "lat_lng_popup_")

    root = map.get_root()

    # add to `<head>` before folium elements
    #root.header.add_child(folium.Element("<style> ... </style>"))

    # add to `<body>` before folium elements
    # root.html.add_child(folium.Element("<h1>STACKOVERFLOW EXAMPLE</h1>"))

    # add to `<script>` before folium elements
    #root.script.add_child(folium.Element("alert('My JavaScript Code');"))

    # add folium elements
    # root.render()  # used by `save()`
    map.render()      # used by `save()`

    # add to `<head>` after folium elements
    #root.header.add_child(folium.Element("<style> ... </style>"))

    # add to `<body>` after folium elements
    #root.html.add_child(folium.Element("<h1>STACKOVERFLOW EXAMPLE</h1>"))

    # add to `<script>` after folium elements
    root.script.add_child(folium.Element('''
        // custom code
            function latLngPop(e) {
                '''+popup_variable_name+'''
                    .setLatLng(e.latlng)
                    .setContent(`
                        Confirm location ?
                        <br>

                        <form target="_top" action="/gamestart/'''+str(user_id)+'''/'''+str(location_id)+'''/${e.latlng.lat}/${e.latlng.lng}/" method="POST">
                        </form>

                        <button onClick="
                            var popup = document.getElementsByClassName('leaflet-popup')[0];
                            popup.style.display = 'block';
                            L.marker([${e.latlng.lat}, ${e.latlng.lng}],{}).addTo('''+map_variable_name+''');
                            document.forms[0].submit();
                        "> Yes </button>
                    `)
                    .openOn('''+map_variable_name+''');
            }
            // end custom code
        '''))

    return map._repr_html_()

def homepage (request):
    return render(request, 'homepage.html')

@login_required
def gamepreview (request):
    return render(request, "gamepreview.html")

@csrf_exempt
@login_required
def gamestart (request, user_id = 0, location_id = 1, latitude_player = 0, longitude_player = 0):
    if (request.method == "POST"):
        user = UserData.objects.get(id = user_id)
        game_location = Location.objects.get(id = location_id)


        if user and game_location:

            location_name = game_location.location_name
            longitude_db = game_location.longitude
            latitude_db = game_location.latitude

            points = calcPoints(latitude_db, longitude_db, latitude_player, longitude_player)
            distance_from_location = distance.distance((latitude_db, longitude_db), (latitude_player, longitude_player)).km
            user.sum_of_points += points
            user.number_of_games_played += 1
            user.save()

        return render(request, "result.html", {"points":points, "location_name":location_name, "distance_from_location":distance_from_location})
    
    else:    
        user = UserData.objects.get(id = user_id)
        locations = list(Location.objects.all())
        number = random.randint(0, len(locations) - 1)
        game_location = locations[number]

        map_filepath = "./gis_project/resources/folium-map.html"
        center_coord = [52.408421, 12.562490]

        location_id = game_location.id
        user_id = user.id

        # create folium map
        map = create_folium_map(map_filepath, center_coord, location_id, user_id)

        return render(request, "gamestart.html", {"game_location":game_location, "map":map})


def leaderboard (request):
    users = list(UserData.objects.all())

    users_filtered = [obj for obj in users if obj.sum_of_points > 0]
    users = [obj for obj in users_filtered if obj.number_of_games_played > 0]

    users.sort(key = lambda x: (x.sum_of_points / x.number_of_games_played), reverse=True)

    return render(request, "leaderboard.html", {"users":users})

@login_required
def logout (request):
    return render(request, "logged_out.html")

@login_required
def profile (request):
    return render(request, "profile.html")


def calcPoints (latitude_db, longitude_db, latitude_player, longitude_player):
    dist = distance.distance((latitude_db, longitude_db), (latitude_player, longitude_player)).km
    if (dist < 25): return 1000

    dist = dist - 25
    if (dist - 1000 >= 0): return 0
    else: return 1000 - dist


class RegisterView (generic.CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'