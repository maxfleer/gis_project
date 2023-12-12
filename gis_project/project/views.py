from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.urls import reverse_lazy
from .forms import RegisterForm
from .models import *
from bs4 import BeautifulSoup
import xyzservices.providers as xyz
import folium
# Create your views here.

def find_popup_slice(html):
    '''
    Find the starting and edning index of popup function
    '''

    pattern = "function latLngPop(e)"

    # startinf index
    starting_index = html.find(pattern)

    #
    tmp_html = html[starting_index:]

    #
    found = 0
    index = 0
    opening_found = False
    while not opening_found or found > 0:
        if tmp_html[index] == "{":
            found += 1
            opening_found = True
        elif tmp_html[index] == "}":
            found -= 1

        index += 1

    # determine the edning index of popup function
    ending_index = starting_index + index

    return starting_index, ending_index

def find_variable_name(html, name_start):
    variable_pattern = "var "
    pattern = variable_pattern + name_start

    starting_index = html.find(pattern) + len(variable_pattern)
    tmp_html = html[starting_index:]
    ending_index = tmp_html.find(" =") + starting_index

    return html[starting_index:ending_index]

def custom_code(popup_variable_name, map_variable_name, folium_port):
    return '''
            // custom code
            function latLngPop(e) {
                %s
                    .setLatLng(e.latlng)
                    .setContent(`
                        Confirm location ?
                        <br>
                        <button onClick="
                            var popup = document.getElementsByClassName('leaflet-popup')[0];
                            popup.style.display = 'block';
                            //where you send the data
                            fetch('http://localhost:%s', {
                                method: 'POST',
                                mode: 'no-cors',
                                headers: {
                                    'Accept': 'application/json',
                                    'Content-Type': 'application/json'
                                },
                                body: JSON.stringify({
                                    latitude: ${e.latlng.lat},
                                    longitude: ${e.latlng.lng}
                                })
                            });
                            L.marker([${e.latlng.lat}, ${e.latlng.lng}],{}).addTo(%s);
                        "> Yes </button>
                    `)
                    .openOn(%s);
            }
            // end custom code
    ''' % (popup_variable_name, folium_port, map_variable_name, map_variable_name)

def create_folium_map(map_filepath, center_coord, folium_port):
    # create folium map
    vmap = folium.Map(center_coord, zoom_start=12)

    # add popup
    folium.LatLngPopup().add_to(vmap)

    tile_provider = xyz.Stadia.StamenWatercolor

    #Update the URL to include the API key placeholder
    tile_provider["url"] = tile_provider["url"] + "?api_key=3dd06860-7f01-4788-84c7-e0e74854b30d"

    #Create the folium TileLayer, specifying the API key
    folium.TileLayer(
        tiles=tile_provider.build_url(api_key='3dd06860-7f01-4788-84c7-e0e74854b30d'),
        attr=tile_provider.attribution,
        name=tile_provider.name,
        max_zoom=tile_provider.max_zoom,
        detect_retina=True
    ).add_to(vmap)

    folium.LayerControl().add_to(vmap)

    # store the map to a file
    vmap.save(map_filepath)

    # read ing the folium file
    html = None
    with open(map_filepath, 'r') as mapfile:
        html = mapfile.read()

    # find variable names
    map_variable_name = find_variable_name(html, "map_")
    popup_variable_name = find_variable_name(html, "lat_lng_popup_")

    # determine popup function indicies
    pstart, pend = find_popup_slice(html)

    # inject code
    with open(map_filepath, 'w') as mapfile:
        mapfile.write(
            html[:pstart] + \
            custom_code(popup_variable_name, map_variable_name, folium_port) + \
            html[pend:]
        )
    
    html = None
    with open(map_filepath, 'r') as mapfile:
        html = mapfile.read()

    with open("./templates/gamepage.html") as inf:
        txt = inf.read()
        soup = BeautifulSoup(txt)
        gametag = soup.find('p', id='gamemap')
        gametag.append(html)

def homepage (request):
    return render(request, 'homepage.html')

@login_required
def gamepage (request):
    folium_port = 3001
    map_filepath = "./templates/folium-map.html"
    center_coord = [52.408421, 12.562490]

    # create folium map
    create_folium_map(map_filepath, center_coord, folium_port)
    return render(request, "gamepage.html")

def leaderboard (request):
    users = UserData.objects.all()
    return render(request, "leaderboard.html", {"users":users})

@login_required
def logout (request):
    return render(request, "logged_out.html")

@login_required
def profile (request):
    return render(request, "profile.html")


class RegisterView (generic.CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'