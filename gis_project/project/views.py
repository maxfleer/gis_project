from django.shortcuts import render
from django.http import HttpResponse
import folium

# Create your views here.
def index (request):
    m = folium.Map([52.408421, 12.562490], zoom_start=12)
    folium.TileLayer('stamenterrain').add_to(m)

    folium.Marker(
        location=[52.408421, 12.562490],
        tooltip="Click me!",
        popup="<button>Hello</button>Brandenburg an der Havel",
        icon=folium.Icon(icon="cloud"),
    ).add_to(m)

    context = {'map': m._repr_html_()}
    return render(request,"index.html", context)

