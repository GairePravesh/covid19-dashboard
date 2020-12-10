# File for creation of plotly maps(figs).
# You can use the plotly builtin fig.show() method to map locally.
import json
from urllib.request import urlopen

import plotly.graph_objs as go
from plotly.offline import plot

from . import getdata

import os

from django.conf import settings

def nep_states_map():
    # reference: https://github.com/mesaugat/geoJSON-Nepal
    with open(os.path.join(settings.STATICFILES_DIRS[0],'assets/geo-data/province.geojson')) as response:
        states = json.load(response)
    df = getdata.nep_state_counties()
    df.STATE = df.STATE.astype('str')
    # print(states)
    fig = go.Figure(
        go.Choroplethmapbox(
            geojson = states, 
            locations = df.STATE,
            featureidkey = "properties.id",
            z = df['cases/state'],
            marker_opacity = 0.75,
            marker_line_width = 0,
            colorscale = [[0, '#FFE3AA'], [.005, '#FFE4CC'], [.030, '#DC654F'], [.060, '#CA3328'], [.080, '#B80000'], [.100, '#7C100C'], [.150, '#580000'], [.175, '#300000'], [1, '#170707']]
        )
    )

    fig.update_layout(
        mapbox_style = 'carto-positron', 
        paper_bgcolor='rgba(0,0,0,0)', 
        mapbox_zoom=5.75, 
        mapbox_center = {'lat': 28.2096, 'lon': 83.9856}, 
        margin = dict(t=0, l=0, r=0, b=0)
    )
    plot_div = plot(fig, include_plotlyjs=False, output_type='div', config={'displayModeBar': False})

    return plot_div


# def nep_districts_map():
#     # reference: https://github.com/mesaugat/geoJSON-Nepal
#     with open(os.path.join(settings.STATICFILES_DIRS[0],'assets/geo-data/districts.geojson')) as response:
#         districts = json.load(response)
#     df = getdata.nep_districts_counties()
#     # df.DIST_EN = df.DIST_EN
#     # print(states)
#     fig = go.Figure(
#         go.Choroplethmapbox(
#             geojson = districts, 
#             locations = df.DIST_EN,
#             featureidkey = "properties.DIST_EN",
#             z = df['cases/districts'],
#             marker_opacity = 0.75,
#             marker_line_width = 0,
#             colorscale = [[0, '#FFE3AA'], [.005, '#FFE4CC'], [.030, '#DC654F'], [.060, '#CA3328'], [.080, '#B80000'], [.100, '#7C100C'], [.150, '#580000'], [.175, '#300000'], [1, '#170707']]
#         )
#     )

#     fig.update_layout(
#         mapbox_style = 'carto-positron', 
#         paper_bgcolor='rgba(0,0,0,0)', 
#         mapbox_zoom=5.75, 
#         mapbox_center = {'lat': 28.2096, 'lon': 83.9856}, 
#         margin = dict(t=0, l=0, r=0, b=0)
#     )
#     plot_div = plot(fig, include_plotlyjs=False, output_type='div', config={'displayModeBar': False})

#     return plot_div
