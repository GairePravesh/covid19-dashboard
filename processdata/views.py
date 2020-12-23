from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader

import json
import requests
from . import getdata, maps


def index(request): 
    return render(request, template_name='index.html')

def trends(request):
    df = getdata.percentage_trends()

    data = {
        'confirmed_trend': int(round(df.Confirmed)),
        'deaths_trend': int(round(df.Deaths)),
        'recovered_trend': int(round(df.Recovered)),
        'death_rate_trend': float(df.Death_rate),

        'n_confirmed_trend': int(round(df.n_Confirmed)),
        'n_deaths_trend': int(round(df.n_Deaths)),
        'n_recovered_trend': int(round(df.n_Recovered)),
        'n_death_rate_trend': float(df.n_Death_rate)
    }

    data = json.dumps(data)
    return HttpResponse(data, content_type='application/json')

def report(request):
    df = getdata.daily_report(date_string=None)
    
    n_df = df[(df.Country_Region=='Nepal')]
    n_df = n_df[['Deaths','Active','Confirmed','Recovered']].sum()

    df = df[['Confirmed', 'Deaths', 'Recovered']].sum()
    death_rate = f'{(df.Deaths / df.Confirmed)*100:.02f}%'
    
    n_death_rate = f'{(n_df.Deaths / n_df.Confirmed)*100:.02f}%'

    r = requests.get('https://covid19.mohp.gov.np/covid/api/confirmedcases')
    present_data = r.json()

    data = {
        # worldwide
        'num_confirmed': int(df.Confirmed),
        'num_recovered': int(df.Recovered),
        'num_deaths': int(df.Deaths),
        'death_rate': death_rate,
        # nepal only specific 
        'n_num_confirmed': int(n_df.Confirmed),
        'n_num_recovered': int(n_df.Recovered),
        'n_num_deaths': int(n_df.Deaths),
        'n_death_rate': n_death_rate,
         # last 24 hours
        'p_num_new': int(present_data['nepal']['today_newcase']),
        'p_num_recovered': int(present_data['nepal']['today_recovered']),
        'p_num_deaths': int(present_data['nepal']['today_death']),
        'p_num_pcr': int(present_data['nepal']['today_pcr']),
        'p_num_rdt': int(present_data['nepal']['today_rdt'])
    }

    data = json.dumps(data)
    # print(data)
    return HttpResponse(data, content_type='application/json')


def global_cases(request):
    df = getdata.global_cases()
    return HttpResponse(df.to_json(orient='records'), content_type='application/json')


def world_map():
    plot_div = maps.world_map()
    return {'world_map': plot_div}


def realtime_growth(request):
    import pandas as pd
    df = getdata.realtime_growth();

    df.index = pd.to_datetime(df.index)
    df.index = df.index.strftime('%Y-%m-%d')

    return HttpResponse(df.to_json(orient='columns'), content_type='application/json')


def daily_report(request):
    df = getdata.daily_report()

    df.drop(['FIPS', 'Admin2', 'Province_State', 'Country_Region', 'Last_Update', 'Deaths', 'Recovered', 'Active', 'Incident_Rate', 'Case_Fatality_Ratio'], axis=1, inplace=True)

    return HttpResponse(df.to_json(orient='columns'), content_type='application/json')


def mapspage(request):
    plot_div = maps.nep_states_map()
    return render(request, template_name='pages/maps.html', context={'nep_states_map': plot_div})

